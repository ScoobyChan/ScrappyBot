import asyncio
import logging
import os
from collections import OrderedDict
from typing import Any

import discord
import requests
from discord.ext import commands


logger = logging.getLogger(__name__)

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3.5:4b")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_TIMEOUT = 120
MAX_CHAT_SESSIONS = 100
MAX_CHAT_MESSAGES = 10
MAX_MESSAGE_SCAN = 500
MAX_MESSAGE_RESULTS = 5


class OllamaModel(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.chat_sessions: OrderedDict[
            tuple[int | None, int, int], list[dict[str, str]]
        ] = OrderedDict()

    async def _post_json(
        self,
        url: str,
        payload: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        response = await asyncio.to_thread(
            requests.post,
            url,
            json=payload,
            headers=headers,
            timeout=OLLAMA_TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("Ollama returned an unexpected response.")
        return data

    @staticmethod
    def _truncate(text: str, limit: int) -> str:
        if len(text) <= limit:
            return text
        return text[: limit - 3] + "..."

    async def _send_text(self, ctx: commands.Context, text: str) -> None:
        for start in range(0, len(text), 2000):
            await ctx.send(
                text[start : start + 2000],
                allowed_mentions=discord.AllowedMentions.none(),
            )

    @commands.command(name="chat", aliases=["ollama"])
    async def chat(self, ctx: commands.Context, *, prompt: str) -> None:
        """Chat with the configured Ollama model. Use 'clear' to reset your chat."""
        if not prompt.strip():
            await ctx.send("Please provide a message to chat about.")
            return

        session_key = (
            ctx.guild.id if ctx.guild else None,
            ctx.channel.id,
            ctx.author.id,
        )

        if prompt.strip().casefold() == "clear":
            self.chat_sessions.pop(session_key, None)
            await ctx.send("Your Ollama chat history has been cleared.")
            return

        history = self.chat_sessions.get(session_key, [])
        messages = [
            {"role": "system", "content": "You are a helpful assistant in a Discord server."},
            *history,
            {"role": "user", "content": prompt},
        ]

        try:
            async with ctx.typing():
                data = await self._post_json(
                    f"{OLLAMA_HOST}/api/chat",
                    {
                        "model": OLLAMA_MODEL,
                        "messages": messages,
                        "stream": False,
                    },
                )
        except (requests.RequestException, ValueError):
            logger.exception("Ollama chat request failed")
            await ctx.send(
                "I couldn't get a response from Ollama. Check the Ollama server, "
                "model, and OLLAMA_HOST configuration."
            )
            return

        message = data.get("message")
        answer = message.get("content") if isinstance(message, dict) else None
        if not isinstance(answer, str) or not answer.strip():
            logger.error("Ollama chat response did not contain message content")
            await ctx.send("Ollama returned an empty or invalid chat response.")
            return

        history = [
            *history,
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": answer},
        ][-MAX_CHAT_MESSAGES:]
        self.chat_sessions[session_key] = history
        self.chat_sessions.move_to_end(session_key)
        if len(self.chat_sessions) > MAX_CHAT_SESSIONS:
            self.chat_sessions.popitem(last=False)

        await self._send_text(ctx, answer)

    @commands.command(name="websearch")
    async def web_search(self, ctx: commands.Context, *, query: str) -> None:
        """Search the web using Ollama's web-search API."""
        if not query.strip():
            await ctx.send("Please provide a web-search query.")
            return

        if not OLLAMA_API_KEY:
            await ctx.send(
                "Web search needs an Ollama API key. Set OLLAMA_API_KEY in your "
                "environment and restart the bot."
            )
            return

        try:
            async with ctx.typing():
                data = await self._post_json(
                    "https://ollama.com/api/web_search",
                    {"query": query, "max_results": MAX_MESSAGE_RESULTS},
                    {"Authorization": f"Bearer {OLLAMA_API_KEY}"},
                )
        except (requests.RequestException, ValueError):
            logger.exception("Ollama web search request failed")
            await ctx.send("Ollama web search failed. Check the API key and try again.")
            return

        results = data.get("results")
        if not isinstance(results, list):
            logger.error("Ollama web search response did not contain results")
            await ctx.send("Ollama returned an invalid web-search response.")
            return
        if not results:
            await ctx.send("No web results found.")
            return

        embed = discord.Embed(
            title=self._truncate(f"Web results for: {query}", 256),
            color=discord.Color.blurple(),
        )
        for result in results[:MAX_MESSAGE_RESULTS]:
            if not isinstance(result, dict):
                continue
            title = result.get("title")
            url = result.get("url")
            content = result.get("content")
            if not isinstance(title, str):
                title = "Untitled result"
            if not isinstance(content, str):
                content = ""
            if isinstance(url, str) and url.startswith(("https://", "http://")):
                value = f"{url}\n{content}"
            else:
                value = content or "No preview available."
            embed.add_field(
                name=self._truncate(title, 200),
                value=self._truncate(value, 850),
                inline=False,
            )

        if not embed.fields:
            await ctx.send("Ollama returned no usable web results.")
            return
        await ctx.send(embed=embed, allowed_mentions=discord.AllowedMentions.none())

    @commands.command(name="messagesearch", aliases=["msgsearch"])
    async def message_search(self, ctx: commands.Context, *, query: str) -> None:
        """Search up to the latest 500 messages in this channel."""
        terms = query.casefold().split()
        if not terms:
            await ctx.send("Please provide a message-search query.")
            return

        matches: list[discord.Message] = []
        try:
            async with ctx.typing():
                async for message in ctx.channel.history(
                    limit=MAX_MESSAGE_SCAN,
                    oldest_first=False,
                ):
                    if message.id == ctx.message.id or not message.content:
                        continue
                    content = message.content.casefold()
                    if all(term in content for term in terms):
                        matches.append(message)
                        if len(matches) >= MAX_MESSAGE_RESULTS:
                            break
        except discord.Forbidden:
            await ctx.send(
                "I need permission to read message history in this channel to search it."
            )
            return

        if not matches:
            await ctx.send("No matching messages found in the latest 500 messages.")
            return

        embed = discord.Embed(
            title=self._truncate(f"Message search: {query}", 256),
            color=discord.Color.blurple(),
        )
        for message in matches:
            author = self._truncate(message.author.display_name, 150)
            timestamp = message.created_at.strftime("%Y-%m-%d %H:%M UTC")
            content = self._truncate(message.content.replace("\n", " "), 700)
            embed.add_field(
                name=f"{author} - {timestamp}",
                value=f"{content}\n{message.jump_url}",
                inline=False,
            )
        await ctx.send(embed=embed, allowed_mentions=discord.AllowedMentions.none())


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OllamaModel(bot))

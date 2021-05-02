import os, time, urllib, sys, json, shutil, tempfile

try:
	import requests
	from clint.textui import progress
except ModuleNotFoundError:
	os.system('pip3 install --user clint requests')
	import requests
	from clint.textui import progress

if sys.version_info >= (3,0):
	import zipfile
	from urllib.parse import urlparse
	from urllib.request import urlopen, Request
else:
	import urllib2
	from urllib2 import urlopen, Request
	from urlparse import urlparse


class Downloader:
	def __init__(self, **kwargs):
		self.ua = kwargs.get('useragent',{'User-Agent':'Mozilla'})

	def openUrl(self, url, headers=None):
		headers = self.ua if headers == None else headers
		try:
			response = urlopen(Request(url, headers=headers))
		except Exception as e:
			print(e)
			return
		return response

	def OpenAsJSON(self, u):
		# ssl cert issue: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
		try:	
			with self.openUrl(u) as url:
				data = json.loads(url.read().decode())
				return data
		except AttributeError:
			return print(f'Cannot load {u}')

	def Download(self, url, path, output=None, Unzip=False):
		if not url.startswith('http'): return print('Url is not Valid')
		if not os.path.exists(path): 
			os.mkdir(path)
		response = self.openUrl(url)

		a = urlparse(url)
		name = a.path
		if not output:
			FILE = name.replace('/','_')
			FILE = FILE.split('_')[len(FILE.split('_'))-1]
		else:
			FILE = output


		time.sleep(0.05)
		_path = f'{path}/{FILE}'
		if os.path.exists(_path):
			try:
				shutil.rmtree(_path)
			except NotADirectoryError:
				os.remove(_path)
		
		try:
			if Unzip == False:
				r = requests.get(url, stream=True)
				with open(_path, 'wb') as f:
					print(f'Downloading {FILE}')
					total_length = int(r.headers.get('content-length'))
					for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
						if chunk:
							f.write(chunk)
							f.flush()
			else:
				r = requests.get(url, stream=True)
				with tempfile.TemporaryDirectory() as tmpdirname:
					_path = f"{tmpdirname}/{FILE}"
					with open(_path, 'wb') as f:
						print(f'Downloading {FILE}')
						total_length = int(r.headers.get('content-length'))
						for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
							if chunk:
								f.write(chunk)
								f.flush()
					self.unzip(str(_path), path)

		except Exception as e:
			print('Downloader:', e)

	def GitClone(self, url, path):
		if not os.path.exists(path): os.mkdir(path)
		os.chdir(path)
		os.system(f'git clone {url}')
		os.chdir('../')
		print('Cloned')


	def GitDL(self, url, path, Unzip=False):
		if not 'https://api.github.com' in url and not 'https://api.github.com' in url: return print('Not a valid API Link')
		ocu = self.OpenAsJSON(url)
		try:	
			for k in ocu[0]['assets']:
				if "RELEASE" in k['browser_download_url']:
					self.Download(url=k['browser_download_url'], path=path, Unzip=Unzip)
		except TypeError:
			# print("I can not access Link's API")
			exit(0)

	def unzip(self, path, output):
		if not os.path.exists(path): return print('Path doesn\'t exist')
		if not os.path.exists(output): os.mkdir(output)
		
		p = path.split('.')
		Type = p[len(p)-1]
		o = path.replace('.'+Type, '')
		if o.startswith('/tmp') or o.startswith('/var'):
			op = o.split('/')
			op = op[len(op)-1]
			o = f'{output}/{op}'
		else:
			o = f'{output}'
		try:
			shutil.unpack_archive(path, o, Type)
			os.remove(path)
		except shutil.ReadError:
			print(f'File: {path} isnt a zip')

	def zip(self, pathtosave, zipType, DirWithFile, FileNFolder):
		ext = ['zip', 'rar']
		if not zipType in ext: return print('Invalid type')
		if not os.path.exists(pathtosave): os.mkdir(pathtosave)
		if not os.path.exists(DirWithFile): return print('Dir does not exist')
		if not os.path.exists(DirWithFile+FileNFolder): return print('I can not find that location')
		
		shutil.make_archive(pathtosave, zipType, DirWithFile, FileNFolder)
		

# Downloader().OpenAsJSON('https://api.github.com/repos/Acidanthera/VirtualSMC/releases')
# os.system('clear')
# Downloader().download('https://github.com/acidanthera/AppleSupportPkg/releases/download/2.1.5/AppleSupport-2.1.5-RELEASE.zip', 'AppleSupportPkg', Unzip=True)
# Downloader().unzip('AppleSupportPkg/AppleSupport-2.1.5-RELEASE.zip', 'AppleSupportPkg')

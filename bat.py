# import os
# print(os.path.abspath(os.getcwd()))

# import subprocess
# subprocess.call([r'C:\Users\Scooby\OneDrive\BotArchieve\MusicPlayer\LavaLink\start.bat'])


import time
import datetime
import re
import time


def time_convert(_time):
    yr = wk = day = hrs = mins = secs = year = week = days = 0
    _time_ = ""

    secs = _time

    if not isinstance(_time, int):
        _list = re.split('\s', _time)
        
        for x in _list:
            if re.search('y|year|yr|yrs|years', x, flags=re.IGNORECASE):
                yr = int(re.sub('[years]', "",  x)) * 52
    
            if re.search('w|wk|wks|week|weeks', x, flags=re.IGNORECASE):
                wk = int(re.sub('[weeks]', "",  x))

            if re.search('day|d|days', x, flags=re.IGNORECASE):
                day = int(re.sub('[days]', "",  x))
    
            if re.search('h|hr|hrs|hour|hours', x, flags=re.IGNORECASE):
                hrs = int(re.sub('[hours]', "",  x))
    
            if re.search('m|min|minutes|minute', x, flags=re.IGNORECASE):
                mins = int(re.sub('[minutes]', "",  x))
    
            if re.search('s|sec|secs|second|seconds', x, flags=re.IGNORECASE):
                secs = int(re.sub('[seconds]', "",  x))
    
        # print(yr, wk, day, hrs, mins, secs)

    _time = datetime.timedelta(days=day, seconds=secs, minutes=mins, hours=hrs, weeks=wk)
    _secs = int(_time.total_seconds())
    if re.search('.*days.*', str(_time)): 
        
        days = int(re.split(" days, ", str(_time))[0])
    
        year = int(days/365)
        week = int((days%365)/7)
        days = int((days%365)%7)

        _time_ = re.split(" days, ", str(_time))

        # print(_time_[1])

    end_format = "{}{}{}{}".format("{} Years ".format(year) if year != 0 else "", "{} Weeks ".format(week) if week != 0 else "", "{} Days ".format(days) if days != 0 else "", _time if isinstance(_time_, str) else _time_[1])
    return(end_format, _secs)

from Media.Media import Media
from Schedule.Program import Priority, Program
from datetime import datetime, date
from prayertimes import PrayTimes
import requests
from pytz import timezone

media = Media('https://archive.org/download/dr_abohabiba_yahoo/%D8%A7%D9%84%D8%B4%D9%8A%D8%AE%20%D8%A3%D8%A8%D9%88%20%D8%A7%D9%84%D8%B9%D9%8A%D9%86%D9%8A%D9%86%20%D8%B4%D8%B9%D9%8A%D8%B4%D8%B9%20-%20%D8%A7%D9%84%D8%A3%D8%B0%D8%A7%D9%86.mp3')
geolocation = requests.get('https://ipinfo.io/').json()
lat, long = [float(i) for i in geolocation['loc'].split(',')]
tzone = timezone(geolocation['timezone'])
today = datetime.today()
prayer = PrayTimes('Egypt').get_times(today, (lat, long), tzone.utcoffset(today).total_seconds()/60/60)
program = Program(media, datetime.now(), Priority.CRITICAL)

# print(prayer['isha'])
# print(datetime.fromisoformat(f"{date.today().isoformat()} {prayer['isha'].strip()}"))

print(program.idx)

print(prayer)
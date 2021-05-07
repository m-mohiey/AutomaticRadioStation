from Media.Media import Media
from Schedule.Program import Priority, Program
from Schedule.Schedule import Schedule
from Schedule import ProgramScheduleConflictException
from datetime import datetime, date, timedelta
from prayertimes import PrayTimes
import requests, os, random, time
from pytz import timezone
import subprocess, pickle
from itertools import cycle
from Player.VLCPlayer import VLCPlayer

azan_path = r"C:\Users\Mohamed\Desktop\Work Automation Scripts\Python\AutomaticRadioStation\azan"
kotof_path = r"E:\Kotof"
azans = [os.path.join(azan_path, p) for p in os.listdir(azan_path)]
kotof = [os.path.join(kotof_path, p) for p in os.listdir(kotof_path) if p.lower().endswith(('.mp3', '.wma', '.rm'))]
if os.path.exists('quran.pkl'):
    with open('quran.pkl', 'rb') as f:
        quran = pickle.load(f)
else:
    quran =  requests.get('https://archive.org/download/rabieaaa2042_gmail_2131346134613461346/rabieaaa2042_gmail_2131346134613461346_vbr.m3u').text.strip().split('\n')
    quran =  [Media(q) for q in quran]
    with open('quran.pkl', 'wb') as f:
        pickle.dump(quran, f)
    
if os.path.exists('twashee7.pkl'):
    with open('twashee7.pkl', 'rb') as f:
        twashee7 = pickle.load(f)
else:
    # twashee7 =  requests.get('https://archive.org/download/moharram1965_gmail_032/moharram1965_gmail_032_vbr.m3u').text.strip().split('\n')
    # twashee7 = [Media(t) for t in twashee7]
    twashee7_path = r"D:\Twashee7"
    twashee7 = [Media(os.path.join(twashee7_path, p)) for p in os.listdir(twashee7_path)]
    with open('twashee7.pkl', 'wb') as f:
        pickle.dump(twashee7, f)

quran_max_duration = max([q.duration for q in quran])
quran = cycle(quran)
print(random.choice(azans))

for _ in range(random.randint(0, 50)): next(quran)

# media = Media('https://archive.org/download/dr_abohabiba_yahoo/%D8%A7%D9%84%D8%B4%D9%8A%D8%AE%20%D8%A3%D8%A8%D9%88%20%D8%A7%D9%84%D8%B9%D9%8A%D9%86%D9%8A%D9%86%20%D8%B4%D8%B9%D9%8A%D8%B4%D8%B9%20-%20%D8%A7%D9%84%D8%A3%D8%B0%D8%A7%D9%86.mp3')
geolocation = requests.get('https://ipinfo.io/').json()
lat, long = [float(i) for i in geolocation['loc'].split(',')]
tzone = timezone(geolocation['timezone'])
today = datetime.today()
prayer = PrayTimes('Egypt').get_times(today, (lat, long), tzone.utcoffset(today).total_seconds()/60/60)
schedule  = Schedule()
for n, pray in prayer.items():
    if n in ['imsak', 'sunrise', 'sunset', 'midnight']:
        continue
    media = Media(random.choice(azans))
    ptime = datetime.fromisoformat(f"{date.today().isoformat()} {pray.strip()}")
    program = Program(media, ptime, Priority.CRITICAL, n)
    print(n, program.start)
    schedule.insert_at(program)
    # quran_media = Media(random.choice(quran))
    # quran_program = Program(quran_media, program.start, Priority.HIGH, 'quran')
    # schedule.insert_at(quran_program, program.start + timedelta(minutes=40))

kotof_media = Media(random.choice(kotof))
kotof_time = datetime.fromisoformat(f"{date.today().isoformat()} {prayer['midnight'].strip()}")
kotof_program = Program(kotof_media, kotof_time, Priority.MEDIUM, 'Kotof')
schedule.insert_at(kotof_program)

telawa_path = r"D:\Telawat"
telawas = [os.path.join(telawa_path, p) for p in os.listdir(telawa_path)]
telawa_media = Media(random.choice(telawas))
telawa_time = datetime.now() + timedelta(minutes=30)
telawa_program = Program(telawa_media, telawa_time, Priority.MEDIUM, 'telawa')
schedule.insert_at(telawa_program)

while True:
    gap = schedule.find_next_gap()
    if not gap:
        break
    start, end = gap
    remain = end - start
    try:
        if remain < quran_max_duration:
            raise ProgramScheduleConflictException
        quran_media = next(quran)
        quran_program = Program(quran_media, start, Priority.HIGH, 'quran')
        schedule.insert_at(quran_program, start)
    except ProgramScheduleConflictException:
        twashee7_remain = [(remain - t.duration).total_seconds() if (remain - t.duration).total_seconds() > 0 else 99999 for t in twashee7]
        twashee7_media = twashee7[twashee7_remain.index(min(twashee7_remain))]
        twashee7_program = Program(twashee7_media, start + schedule.MAX_SILENCE, Priority.LOW, 'twashee7')
        try:
            schedule.insert_at(twashee7_program)
        except ProgramScheduleConflictException:
            twashee7_program.duration = remain - timedelta(seconds=2)
            schedule.insert_at(twashee7_program)


schedule.sync()
print(schedule)
p = None
player = VLCPlayer()
for m in schedule.play_next():
    wait = (m.start - datetime.now()).total_seconds()
    if wait < 0:
        schedule.sync()
        print('schedule missed', '::', m)
        continue
    print(f'Next Program starts at {m.start}')
    time.sleep(wait)
    # if p:
    #     p.terminate()
    # p = subprocess.Popen(f'ffplay -hide_banner -autoexit -nodisp -i "{m.media.path}"', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    if m.priority in [Priority.CRITICAL, Priority.HIGH Priority.MEDIUM]:
        print('Stopping previuos program')
        player.stop()
    player.open(m)
    player.play()
    if m.priority in [Priority.CRITICAL, Priority.HIGH]:
        # p.wait()
        # time.sleep(1)
        player.wait()
        print('Waiting for Critical Program End')
    print(m.name, ' - ', m.media.title, '===', m)

# print(prayer['isha'])
# print(datetime.fromisoformat(f"{date.today().isoformat()} {prayer['isha'].strip()}"))

print(program.idx)

print(prayer)
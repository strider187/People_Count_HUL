from subprocess import check_output

file_name = "test   .mp4"

#For Windows
#a = str(check_output('ffprobe -i  "'+file_name+'" 2>&1 |findstr "Duration"',shell=True))

#For Linux
a = str(check_output('ffprobe -i  "'+file_name+'" 2>&1 |grep "Duration"',shell=True))

a = a.split(",")[0].split("Duration:")[1].strip()

h, m, s = a.split(':')
duration = int(h) * 3600 + int(m) * 60 + float(s)

print(duration)
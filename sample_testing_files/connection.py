import os

hostname = "192.168.0.250"
response = os.system("ping -n 1 " + hostname)

if response == 0:
    print(hostname, 'is up!')
else:
    print(hostname, 'is down!')











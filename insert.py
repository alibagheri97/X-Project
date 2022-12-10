from sup import sup, findElement
import os
from send import write, read


cwd = os.getcwd() + "/"
final = f"[Unit]\nDescription=My test service\nAfter=multi-user.target\n\n[Service]\nType=simple\nRestart=always\nWorkingDirectory={cwd}\nExecStart=/usr/bin/python3 {cwd}send.py\n\n[Install]\nWantedBy=multi-user.target"
file = open("test.service", "w")
file.write(final)
file.close()

ip = str(input("Your panel IP: "))
port = str(input("Your panel port:(default 8888) "))

a = read("settings.json")

loca = findElement(a, '"panelIp": "167.235.150.114"')
a = a[:loca[0]] + f'"panelIp": "{ip}"' + a[loca[1]:]

loca = findElement(a, '"panelPort": "8888"')[0]
a = a[:loca[0]] + f'"panelPort": "{port}"' + a[loca[1]:]

write("settings.json", a)

from sup import sup
import os
from send import write, read

cwd = os.getcwd() + "/"
final = f"[Unit]\nDescription=My test service\nAfter=multi-user.target\n\n[Service]\nType=simple\nRestart=always\nWorkingDirectory={cwd}\nExecStart=/usr/bin/python3 {cwd}send.py\n\n[Install]\nWantedBy=multi-user.target"
file = open("test.service", "w")
file.write(final)
file.close()

ip = str(input("Your panel IP: "))
port = str(input("Your panel port:(default 8888) "))

sett = read("settings.json")

from sup import sup
import os

cwd = os.getcwd() + "/"
final = f"[Unit]\nDescription=My test service\nAfter=multi-user.target\n\n[Service]\nType=simple\nRestart=always\nWorkingDirectory={cwd}\nExecStart=/usr/bin/python3 {cwd}send.py\n\n[Install]\nWantedBy=multi-user.target"
file = open("test.service", "w")
file.write(final)
file.close()

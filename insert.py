from sup import sup
import os
from send import write, read
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--set", type=str, help="set ip and port")
args = parser.parse_args()
sett = args.set
ip, port = sup(sett, ":")

cwd = os.getcwd() + "/"
final = f"[Unit]\nDescription=My test service\nAfter=multi-user.target\n\n[Service>
file = open("test.service", "w")
file.write(final)
file.close()

a = read("settings.json")

loca = findElement(a, '"panelIp": "167.235.150.114"')[0]

a = a[:loca[0]] + f'"panelIp": "{ip}"' + a[loca[1]:]

loca = findElement(a, '"panelPort": "8888"')[0]

a = a[:loca[0]] + f'"panelPort": "{port}"' + a[loca[1]:]

write("settings.json", a)

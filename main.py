import sqlite3
import json
import uuid
import paramiko
import os
import time
from sup import sup
import json
from datetime import datetime


def addClient(clientName, clientIpCount, expTime, ssh=False):
    dic = json.load(open("settings.json", "r"))
    host, ip, port = dic["host"], dic["ip"], dic["port"]
    
    def dateTransfer(date):
        pass

    def creatBackup(file="x-ui.db"):
        import shutil
        lst = sup(time.asctime(), " ")
        name = sup(file, ".")
        tim = sup(lst[3], ":")
        shutil.copy2(file, f"{name[0]} {lst[1]} {lst[2]} {tim[0]}{tim[1]}{tim[2]}.{name[-1]}")

    def download(file="/etc/x-ui/x-ui.db", destenation="x-ui.db"):
        # downloading
        ftp_client = ssh_client.open_sftp()
        time.sleep(1)
        ftp_client.get(file, destenation)
        ftp_client.close()

    def upload(file="x-ui.db", destenation="/etc/x-ui/x-ui.db"):
        # uploading
        ftp_client = ssh_client.open_sftp()
        ftp_client.put(file, destenation)
        ftp_client.close()

    def com(cmd):
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        print(stdout.readlines())

    def findE(data, el):
        out = []
        for i in range(len(data)):
            if data[i] == el:
                out.append(i)
        return out

    def addIp(remark, ipcount, expTime, sqls, cur, inbnd_id=1):

        if expTime != "":
            lst = sup(expTime, "-")
            dt = datetime(int(lst[0]), int(lst[1]), int(lst[-1]))
            epoch_time = datetime(1970, 1, 1)
            delta = (dt - epoch_time)
            tlst = sup(str(time.time()), ".")
            expireTime = int(str(int(delta.total_seconds())) + f"{tlst[1][0]}{tlst[1][1]}{tlst[1][2]}")
        else:
            expireTime = '""'

        if expireTime == '""':
            expireTrffic = 0
        else:
            expireTrffic = expireTime
        trffic_list = [a for a in cur.execute("SELECT * FROM client_traffics")]
        trffic = (trffic_list[-1][0] + 1, inbnd_id, 1, remark, 0, 0, expireTrffic, 0)

        inbnd_list = [a for a in cur.execute("SELECT * FROM inbounds")]
        inbnd_json = inbnd_list[0][11]
        inbnd_dict = json.loads(inbnd_json)['clients']  # for read
        lst = findE(inbnd_json, "]")[0:-1]
        cors = lst[inbnd_id - 1]
        Uuid = str(uuid.uuid1())
        jinput = ',\n    {\n      "id": "' + Uuid \
                 + '",\n      "flow": "xtls-rprx-direct",\n      "email": "' + remark + '",\n      "limitIp": ' + str(
            ipcount) \
                 + ',\n      "totalGB": 0,\n      "expiryTime": ' + str(expireTime) + '\n    }\n'
        print(jinput[1:])
        out_inbnd = inbnd_json[0:cors - 3] + jinput + inbnd_json[cors - 2:]
        inbnd = (inbnd_id, inbnd_list[inbnd_id - 1][1], inbnd_list[inbnd_id - 1][2], inbnd_list[inbnd_id - 1][3],
                 inbnd_list[inbnd_id - 1][4], inbnd_list[inbnd_id - 1][5],
                 inbnd_list[inbnd_id - 1][6], inbnd_list[inbnd_id - 1][7], inbnd_list[inbnd_id - 1][8],
                 inbnd_list[inbnd_id - 1][9],
                 inbnd_list[inbnd_id - 1][10], out_inbnd, inbnd_list[inbnd_id - 1][12], inbnd_list[inbnd_id - 1][13],
                 inbnd_list[inbnd_id - 1][14])
        inputs = [inbnd, trffic]
        outs = []
        for i in range(len(inputs)):
            outs.append([sqls[i], inputs[i]])
        return outs, Uuid, remark

    vlessK = open("vlessKeys.txt", "r").read()
    if not clientName in vlessK:
        tA = time.time()
        if ssh:
            tD = time.time()

            print("connecting to ssh server...\n")

            ssh_client = paramiko.SSHClient()
            ssh_client.load_system_host_keys()
            ssh_client.connect()  # )
            time.sleep(1)

            print("Server connected Secsussfully...\n")
            print("Start download db...\n")

            download()

            ssh_client.close()
            print("download Secsusseful!!\n")
            print(f"Donwload Time: {time.time() - tD}s\n")
            creatBackup()
            dbfile = "x-ui.db"
        else:
            # creating file path
            dbfile = "/etc/x-ui/x-ui.db"

        try:
            file_size = os.path.getsize(dbfile)
        except:
            dbfile = "x-ui.db"
            file_size = os.path.getsize(dbfile)

        if file_size != 0:
            # Create a SQL connection to our SQLite database
            print("connecting to db...\n")
            con = sqlite3.connect(dbfile)
            print("connect to db Secsusseful!!\n")

            # creating cursor
            cur = con.cursor()

            table_list = [a for a in cur.execute("SELECT * FROM sqlite_master WHERE type = 'table'")]
            tables_name = []
            for i in range(table_list.__len__()):
                tables_name.append(table_list[i][1])

            tables_name = [tables_name[1], tables_name[4]]
            t1 = ['id', 'user_id', 'up', 'down', 'total', 'remark', 'enable', 'expiry_time', 'listen', 'port', 'protocol',
                  'settings', 'stream_settings', 'tag', 'sniffing']
            t7 = ['id', 'inbound_id', 'enable', 'email', 'up', 'down', 'expiry_time', 'total']
            sql_list = []
            sql_tc = [t1, t7]
            for i in range(len(tables_name)):
                tcc = ""
                for j in range(len(sql_tc[i])):
                    tcc += str(sql_tc[i][j]) + ","
                vtc = "?," * len(sql_tc[i])
                sql_list.append(f"""INSERT OR REPLACE INTO {tables_name[i]}({tcc[:-1]}) VALUES({vtc[:-1]});""")

            print("adding Client...\n")
            outs, Uuid, remark = addIp(clientName, clientIpCount, expTime, sql_list, cur)
            for i in range(len(outs)):
                cur.execute(outs[i][0], outs[i][1])
                con.commit()
            cur.close()
            con.close()
            file_size = os.path.getsize(dbfile)
            if file_size != 0:
                if ssh:
                    print("Uploading db...\n")
                    tU = time.time()
                    ssh_client = paramiko.SSHClient()
                    ssh_client.load_system_host_keys()
                    ssh_client.connect()  # )
                    time.sleep(1)
                    ftp_client = ssh_client.open_sftp()
                    time.sleep(1)
                    file = "x-ui.db"
                    destenation = "/etc/x-ui/x-ui.db"
                    ftp_client.put(file, destenation)
                    ftp_client.close()
                    ssh_client.close()
                    print("Upload db Sucsessfull!!\n")
                    print(f"Uploading time: {time.time() - tU}s\n")
                else:
                    pass
                vlessKey = f"vless://{Uuid}@{ip}:{port}?type=ws&security=none&path=%2F&host={host}#{remark}"
                vless = open("vlessKeys.txt", "a")
                vless.write(vlessKey + "\n")
                vless.close()
                print("Everything Done!!\n")
            else:
                raise RuntimeError("File Size is 0")
            print(f"Script Time : {time.time() - tA}s")

            print("adding Client Sucsessfull!!\n")
            print("Vless Key: " + vlessKey)
        else:
            raise RuntimeError("File Size is 0")
        return vlessKey
    else:
        return ""
    

def getDetected(parts):
    dic = json.load(open("settings.json", "r"))
    ipCountDefult = dic["ipCountDefult"]
    try:
        andsup = sup(parts, "&")
        dic = dict()

        for i in andsup:
            lst = sup(i, "=")
            if lst[0] == "remark" and lst.__len__() == 1:
                raise RuntimeError("")
            elif lst[0] == "ipcount" and lst.__len__() == 1:
                lst.append(ipCountDefult)
            elif lst[0] == "date" and lst.__len__() == 1:
                lst.append("")
            dic[lst[0]] = lst[1]
        return dic
    except:
        return None

import sqlite3
import json
import uuid
import os
import time
from datetime import date
from dateutil.relativedelta import relativedelta
from sup import sup
from datetime import datetime
import shutil


def addClient(clientName, clientIpCount, expTime, tgb, inbndid, host):
    dic = json.load(open("settings.json", "r"))
    hostIp = dic["host"][0][host]
    ip, port = hostIp, getInboundsPort(int(inbndid) - 1)

    def dateTransfer(date):
        pass

    def creatBackup(file="/etc/x-ui/x-ui.db"):
        lst = sup(time.asctime(), " ")
        name = sup(file, ".")
        tim = sup(lst[4], ":")
        nameSql = sup(name[0], "/")[-1]
        shutil.copy2(file, f"/root/sqlBackup/{nameSql}-{lst[1]}-{lst[3]}-{tim[0]}{tim[1]}{tim[2]}.{name[-1]}")

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

    def addIp(remark, ipcount, expTime, sqls, cur, totalGB, inbnd_id=1):
        if totalGB != '':
            try:
                totalGB = str(int(int(totalGB) * 1.073741824 * 10 ** 9))
            except:
                pass
        else:
            totalGB = "0"
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
        trffic = (trffic_list[-1][0] + 1, inbnd_id, 1, remark, 0, 0, expireTrffic, totalGB)

        inbnd_list = [a for a in cur.execute("SELECT * FROM inbounds")]
        inbnd_json = inbnd_list[inbnd_id - 1][11]
        # inbnd_dict = json.loads(inbnd_json)['clients']  # for read
        lst = findE(inbnd_json, "]")[0:-1]
        cors = lst[0]
        Uuid = str(uuid.uuid1())
        jinput = ',\n    {\n      "id": "' + Uuid \
                 + '",\n      "flow": "xtls-rprx-direct",\n      "email": "' + remark + '",\n      "limitIp": ' + str(
            ipcount) \
                 + f',\n      "totalGB": {totalGB},\n      "expiryTime": ' + str(expireTime) + '\n    }\n'
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
            t1 = ['id', 'user_id', 'up', 'down', 'total', 'remark', 'enable', 'expiry_time', 'listen', 'port',
                  'protocol',
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
            outs, Uuid, remark = addIp(clientName, clientIpCount, expTime, sql_list, cur, tgb, inbnd_id=int(inbndid))
            creatBackup()
            for i in range(len(outs)):
                cur.execute(outs[i][0], outs[i][1])
                con.commit()
            cur.close()
            con.close()
            file_size = os.path.getsize(dbfile)
            if file_size != 0:
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
    dicJ = json.load(open("settings.json", "r"))
    try:
        andsup = sup(parts, "&")
        dic = dict()

        for i in andsup:
            lst = sup(i, "=")
            if lst[0] == "remark" and lst.__len__() == 1:
                raise RuntimeError("")
            elif lst[0] == "ipcount" and lst.__len__() == 1:
                lst.append(dicJ["ipCountDefult"])
            elif lst[0] == "date" and lst.__len__() == 1:
                dt = date.today() + relativedelta(months=+int(dicJ["dateDefult"]))
                lst.append(f"{dt.year}-{dt.month}-{dt.day}")
            elif lst.__len__() == 1:
                lst.append("")
            dic[lst[0]] = lst[1]
        return dic
    except:
        return None


def getInboundsCount():
    dbfile = "/etc/x-ui/x-ui.db"

    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    inbnd_list = [a for a in cur.execute("SELECT * FROM inbounds")]
    inbnd_count = inbnd_list.__len__()
    inbnd_count_list = []
    for i in range(inbnd_count):
        inbndType = inbnd_list[i][10]
        if inbndType == "vless":
            inbnd_count_list.append("y")
        else:
            inbnd_count_list.append("n")
    cur.close()
    con.close()
    return inbnd_count_list


def getInboundsPort(inbnd):
    dbfile = "/etc/x-ui/x-ui.db"
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    inbnd_list = [a for a in cur.execute("SELECT * FROM inbounds")]
    inbnd_port = inbnd_list[inbnd][9]
    cur.close()
    con.close()
    return inbnd_port

import sqlite3
import json
import uuid
import os
import time
from datetime import date
from dateutil.relativedelta import relativedelta
from sup import *
import datetime
import shutil
from time import strptime

def addClient(clientName, clientIpCount, expTime, tgb, inbndid, host):
    dic = json.load(open("settings.json", "r"))
    hostIp = dic["host"][0][host]
    ip, port = hostIp, getInboundsPort(int(inbndid) - 1)

    def dateTransfer(date):
        pass

    def creatBackup(file=Value.path):
        lst = sup(time.asctime(), " ")
        name = sup(file, ".")
        for i in lst:
            if i.count(":") == 2:
                tim = sup(i, ":")
                break
        for i in lst[1:]:
            if i.__len__() == 2:
                day = i
            elif i.__len__() == 3:
                month = i
        nameSql = sup(name[0], "/")[-1]
        shutil.copy2(file, f"/root/sqlBackup/{nameSql}-{month}-{day}-{tim[0]}{tim[1]}{tim[2]}.{name[-1]}")

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
            dt = datetime.datetime(int(lst[0]), int(lst[1]), int(lst[-1]))
            epoch_time = datetime.datetime(1970, 1, 1, 0, 0, 0)
            delta = (dt - epoch_time)
            tlst = sup(str(time.time()), ".")
            expireTime = int(str(int(delta.total_seconds()) - 12600) + f"{tlst[1][0]}{tlst[1][1]}{tlst[1][2]}")
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

        dbfile = Value.path
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
    dbfile = Value.path
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
    dbfile = Value.path
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    inbnd_list = [a for a in cur.execute("SELECT * FROM inbounds")]
    inbnd_port = inbnd_list[inbnd][9]
    cur.close()
    con.close()
    return inbnd_port


def tableSetup(htm):
    dbfile = Value.path
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    traffic_list = [a for a in cur.execute("SELECT * FROM client_traffics")]
    cur.close()
    con.close()
    lstOut = []
    keysLst = ["_", "id", "enable", "name", "up", "down", "exp", "total"]
    for i in traffic_list:
        dic = dict()
        for j in range(len(keysLst)):
            if keysLst[j] == "_":
                continue
            dic[keysLst[j]] = i[j]
        lstOut.append(dic)

    element = '\n<tr style="color: {5};font-weight: bold;">\n' \
              '    <td>{0}</td>\n' \
              '    <td>{1}</td>\n' \
              '    <td>{2}</td>\n' \
              '    <td>{3}</td>\n' \
              '    <td>{4}</td>\n' \
              '</tr>'
    modeLst = ["Expired", "Enable", "Disable", "Admin", "Data Exceeded", "Expire Soon"]
    modeVal = ["rgb(255,0,77)", "rgb(0,200,8)", "rgb(0,0,0)", "rgb(89,94,210)", "rgb(176,176,176)", "rgb(214,209,93)"]
    mode = dict.fromkeys(modeLst)
    for i in range(modeLst.__len__()):
        mode[modeLst[i]] = modeVal[i]
    for i in lstOut:
        id, enable, name, up, down, exp, total = list(i.values())
        totalLeft = total - (up + down)
        if totalLeft < 0:
            totalLeft = 0
        enable, exp, totalLeft = enableMode(enable, exp, totalLeft)
        htm = insert2Tag(htm, "<tbody", element.format(name, enable, id, totalLeft, exp, mode[enable]), mode="+")
    return htm


def enableMode(enable, exp, total):
    total = str(total / (1.073741824 * 10 ** 9)) + "0"
    total = sup(total, ".")
    total = f"{total[0]}.{total[1][:2]}"
    if enable == 1:
        if exp == 0:
            enable = "Admin"
            exp = "0/0/0"
        else:
            if int(str(exp)[:-3]) - int(time.time()) < 7 * (24 * 60 * 60):
                enable = "Expire Soon"
                exp = ctime(exp)
            else:
                enable = "Enable"
                exp = ctime(exp)
    elif enable == 0:
        if int(time.time()) < int(str(exp)[:-3]):
            if float(total) < 1000.0:
                enable = "Data Exceeded"
                exp = ctime(exp)
            else:
                enable = "Disable"
                exp = ctime(exp)
        else:
            enable = "Expired"
            exp = ctime(exp)

    return enable, exp, total


def ctime(t):
    tt = time.ctime(float(f"{str(t)[:-3]}.{str(t)[-3:]}"))
    tt = sup(tt, " ")
    if tt.__len__() == 6:
        day = tt[3]
    else:
        day = tt[2]
    month = month2int(tt[1])
    year = tt[-1]
    return f"{year}/{month}/{day}"


def month2int(txt):
    return strptime(f'{txt}', '%b').tm_mon

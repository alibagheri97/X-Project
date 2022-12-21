from http.server import BaseHTTPRequestHandler, HTTPServer
import copy
import datetime
import email.utils
import html
import http.client
import io
import mimetypes
import os
import posixpath
import select
import shutil
import socket
import socketserver
import sys
import time
import urllib.parse
import contextlib
from functools import partial
from http import HTTPStatus
from main import *
import json
import qrcode
from sup import *
from datetime import date
from time import strptime
import revise


def inboundSetup(htm):
    inbndDf = int(Value.dic["inbndDefult"])
    hostName = list(Value.dic["host"][0].keys())
    inbnd_count = getInboundsCount()
    htm2 = read("assets/js/themeRaw.js")
    loc = findElement(htm2, "$")[-1]
    bgA = "rgb(78,115, 223)"
    colA = "rgb(255,255, 255)"
    bgD = "rgb(234,234,234)"
    colD = "rgb(72,65,65)"
    js = ""
    for i in hostName:
        val = f'<option value="{i}" selected="">{i}</option>'
        htm = insert2Tag(htm, 'name="hosts"', val)
    for i in list(range(inbnd_count.__len__()))[::-1]:
        on = ""
        if not inbnd_count[i] == "y":
            on = "opacity: 0.30;"
        if i + 1 == inbndDf:
            val = ""
            if not i == 0:
                val = f'<button id="bt{i + 1}" class="btn btn-primary border rounded-pill" type="button" style="width: 37.6875px;box-shadow: 0px 0px 3px;margin-left: 10px;{on}background: {bgA};color: {colA};" onclick="check(' + f'{i + 1}' + f')">{i + 1}</button>'
            else:
                val = f'<button id="bt{i + 1}" class="btn btn-primary border rounded-pill" type="button" style="width: 37.6875px;box-shadow: 0px 0px 3px;{on}background: {bgA};color: {colA};" onclick="check(' + f'{i + 1}' + f')">{i + 1}</button>'
            htm = insert2Tag(htm, 'name="inbndButtons"', val)
        else:
            val2 = ""
            if not i == 0:
                val2 = f'<button id="bt{i + 1}" class="btn btn-primary border rounded-pill" type="button" style="width: 37.6875px;box-shadow: 0px 0px 3px;margin-left: 10px;{on}background: {bgD};color: {colD};" onclick="check(' + f'{i + 1}' + f')">{i + 1}</button>'
            else:
                val2 = f'<button id="bt{i + 1}" class="btn btn-primary border rounded-pill" type="button" style="width: 37.6875px;box-shadow: 0px 0px 3px;{on}background: {bgD};color: {colD};" onclick="check(' + f'{i + 1}' + f')">{i + 1}</button>'
            htm = insert2Tag(htm, 'name="inbndButtons"', val2)
    for i in range(inbnd_count.__len__()):
        if inbnd_count[i] == "y":
            js += f"\n    if (id == '{i + 1}')" + "{\n    " + f"document.getElementById('inbound').value = '{i + 1}';\n    "
            for j in range(inbnd_count.__len__()):
                if inbnd_count[i] == "y":
                    if j == i:
                        js += f"document.getElementById('bt{j + 1}').style.background = '{bgA}';\n    " + f"document.getElementById('bt{j + 1}').style.color = '{colA}';\n    "
                    else:
                        js += f"document.getElementById('bt{j + 1}').style.background = '{bgD}';\n    " + f"document.getElementById('bt{j + 1}').style.color = '{colD}';\n    "
            js += "}"
    write("assets/js/theme.js", htm2[:loc[0] + 2] + js + "\n }")
    htm = tagChange(htm, 'name="inbnd"', "value", inbndDf)
    return htm


def ipcountSetup(htm):
    htm = tagChange(htm, 'name="ipc"', "max", int(Value.dic["maxIpDefult"]))
    htm = tagChange(htm, 'name="ipc"', "value=", int(Value.dic["ipCountDefult"]))
    htm = tagChange(htm, 'name="ipcText"', "value=", int(Value.dic["ipCountDefult"]))
    return htm


def intialSetup():
    checkNone()
    Value.dic = json.load(open("settings.json", "r"))
    htm = read("indexInit.html")
    htm = ipcountSetup(htm)
    htm = inboundSetup(htm)
    write("indexRaw.html", htm)
    htm = read("rawTable.html")
    htm = tableSetup(htm)
    write("table.html", htm)


def makeQr(key):
    img = qrcode.make(key)
    img.save('qr.jpg')


def setQrcode():
    # make Qr
    makeQr(Value.key)
    # do changes
    htm = read("indexRaw.html")
    htm = tagChange(htm, 'name="qrcode"', "style", "Visibility: visible;width: 166px;")
    htm = tagChange(htm, 'name="txtQr"', "value", Value.key)
    htm = add2Tag(htm, 'name="qrcode"', "src", "qr.jpg")
    # save changes
    write("index.html", htm)


def checkIp(clientIp):
    ips = read("ip.txt")
    if clientIp in ips:
        Value.go = "index.html"
    else:
        Value.go = "login.html"


# def checkRequest(path):
#     pass


# write("indexRaw.html", read("indexInit.html"))
Value.dic = json.load(open("settings.json", "r"))

hostName = Value.dic["panelIp"]
serverPort = int(Value.dic["panelPort"])


def setIndex():
    write("index.html", read("indexRaw.html"))


class MyServer(BaseHTTPRequestHandler):
    __version__ = "0.6"
    server_version = "SimpleHTTP/" + __version__

    extensions_map = _encodings_map_default = {

        '.gz': 'application/gzip',

        '.Z': 'application/octet-stream',

        '.bz2': 'application/x-bzip2',

        '.xz': 'application/x-xz',

    }

    def __init__(self, *args, directory=None, **kwargs):

        if directory is None:
            directory = os.getcwd()

        self.directory = os.fspath(directory)
        super().__init__(*args, **kwargs)

    def do_GET(self):

        """Serve a GET request."""
        intialSetup()
        f = self.send_head()

        if f:

            try:

                self.copyfile(f, self.wfile)

            finally:

                f.close()

    def do_HEAD(self):

        """Serve a HEAD request."""
        f = self.send_head()

        if f:
            f.close()

    def send_head(self):

        path = self.path
        path = self.translate_path(path)

        f = None

        if os.path.isdir(path):

            parts = urllib.parse.urlsplit(self.path)
            new_parts = (parts[0], parts[1], parts[2] + '/', parts[3], parts[4])

            dic = getDetected(parts[3])
            if dic not in [None, dict()]:
                ips = read("ip.txt")
                clientIp = self.client_address[0]
                if Value.go == "login.html":
                    if "usr" in list(dic.keys()):
                        if "pass" in list(dic.keys()):
                            if dic["usr"] == Value.dic["panelUsr"] and dic["pass"] == Value.dic["panelPass"]:
                                write("ip.txt", clientIp + "\n")
                                intialSetup()
                                setIndex()
                            else:
                                pass

                elif Value.go == "index.html":
                    if "remark" in list(dic.keys()):
                        vlessK = open("vlessKeys.txt", "r").read()

                        if not dic["remark"] in vlessK and dic["remark"] != "":
                            print("ready\n")
                            Value.key = addClient(dic["remark"], dic["ipc"], dic["date"], dic["tgb"], dic["inbnd"],
                                                  dic["hosts"])
                            print(f"{Value.key}\n")
                        else:
                            Value.key = ""

                        if Value.key != "":
                            setQrcode()
                            revise.revise(int(dic["inbnd"]) - 1, iport=f'{Value.dic["panelIp"]}:{Value.dic["xuiPort"]}')
                            time.sleep(1)
                            # save informations
                            info = read("Info.json")
                            if info.__len__() != 4:
                                write("Info.json", info[
                                                   0:-2] + "," + "\n   " + f'"{dic["remark"]}": [\n    ' + "{\n      " + f'"Telegram ID": "{dic["tid"]}",\n      ' + f'"Phone": "{dic["phone"]}",\n      ' + f'"Note": "{dic["note"]}"\n    ' + "}\n  ]\n}")
                            else:
                                write("Info.json", info[
                                                   0:-3] + "\n   " + f'"{dic["remark"]}": [\n    ' + "{\n      " + f'"Telegram ID": "{dic["tid"]}",\n      ' + f'"Phone": "{dic["phone"]}",\n      ' + f'"Note": "{dic["note"]}"\n    ' + "}\n  ]\n}")
                            print(f"Write Done!!\n")
                        else:
                            intialSetup()
                            setIndex()
                    else:
                        intialSetup()
                        setIndex()
            else:
                intialSetup()
                setIndex()

            checkIp(self.client_address[0])
            for index in Value.go, Value.go[:-1]:

                index = os.path.join(path, index)

                if os.path.exists(index):
                    path = index
                    break
            else:
                pass
        ctype = self.guess_type(path)

        if path.endswith("/"):
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")

            return None

        try:

            f = open(path, 'rb')

        except OSError:

            self.send_error(HTTPStatus.NOT_FOUND, "File not found")

            return None

        try:

            fs = os.fstat(f.fileno())

            # Use browser cache if possible

            if ("If-Modified-Since" in self.headers

                    and "If-None-Match" not in self.headers):

                # compare If-Modified-Since and time of last file modification

                try:

                    ims = email.utils.parsedate_to_datetime(

                        self.headers["If-Modified-Since"])

                except (TypeError, IndexError, OverflowError, ValueError):

                    # ignore ill-formed values

                    pass

                else:

                    if ims.tzinfo is None:
                        # obsolete format with no timezone, cf.

                        # https://tools.ietf.org/html/rfc7231#section-7.1.1.1

                        ims = ims.replace(tzinfo=datetime.timezone.utc)

                    if ims.tzinfo is datetime.timezone.utc:

                        # compare to UTC datetime of last modification

                        last_modif = datetime.datetime.fromtimestamp(

                            fs.st_mtime, datetime.timezone.utc)

                        # remove microseconds, like in If-Modified-Since

                        last_modif = last_modif.replace(microsecond=0)

                        if last_modif <= ims:
                            self.send_response(HTTPStatus.NOT_MODIFIED)

                            self.end_headers()

                            f.close()

                            return None

            self.send_response(HTTPStatus.OK)

            self.send_header("Content-type", ctype)

            self.send_header("Content-Length", str(fs[6]))

            self.send_header("Last-Modified",

                             self.date_time_string(fs.st_mtime))

            self.end_headers()

            return f

        except:

            f.close()

            raise

    def list_directory(self, path):

        try:

            list = os.listdir(path)

        except OSError:

            self.send_error(

                HTTPStatus.NOT_FOUND,

                "No permission to list directory")

            return None

        list.sort(key=lambda a: a.lower())

        r = []

        try:

            displaypath = urllib.parse.unquote(self.path,

                                               errors='surrogatepass')

        except UnicodeDecodeError:

            displaypath = urllib.parse.unquote(path)

        displaypath = html.escape(displaypath, quote=False)

        enc = sys.getfilesystemencoding()

        title = 'Directory listing for %s' % displaypath

        r.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '

                 '"http://www.w3.org/TR/html4/strict.dtd">')

        r.append('<html>\n<head>')

        r.append('<meta http-equiv="Content-Type" '

                 'content="text/html; charset=%s">' % enc)

        r.append('<title>%s</title>\n</head>' % title)

        r.append('<body>\n<h1>%s</h1>' % title)

        r.append('<hr>\n<ul>')

        for name in list:

            fullname = os.path.join(path, name)

            displayname = linkname = name

            # Append / for directories or @ for symbolic links

            if os.path.isdir(fullname):
                displayname = name + "/"

                linkname = name + "/"

            if os.path.islink(fullname):
                displayname = name + "@"

                # Note: a link to a directory displays with @ and links with /

            r.append('<li><a href="%s">%s</a></li>'

                     % (urllib.parse.quote(linkname,

                                           errors='surrogatepass'),

                        html.escape(displayname, quote=False)))

        r.append('</ul>\n<hr>\n</body>\n</html>\n')

        encoded = '\n'.join(r).encode(enc, 'surrogateescape')

        f = io.BytesIO()

        f.write(encoded)

        f.seek(0)

        self.send_response(HTTPStatus.OK)

        self.send_header("Content-type", "text/html; charset=%s" % enc)

        self.send_header("Content-Length", str(len(encoded)))

        self.end_headers()

        return f

    def translate_path(self, path):
        cwd = os.getcwd()

        try:
            if os.path.getsize(cwd + "/" + path):
                if "table" in path:
                    return cwd + "/" + path
        except:
            path = cwd + "/"
            return path

        if not "." in path or (path.count("/") == 1 and not "jpg" in path):
            path = cwd + "/"
            return path

        path = path.split('?', 1)[0]

        path = path.split('#', 1)[0]

        trailing_slash = path.rstrip().endswith('/')

        try:

            path = urllib.parse.unquote(path, errors='surrogatepass')

        except UnicodeDecodeError:

            path = urllib.parse.unquote(path)

        path = posixpath.normpath(path)

        words = path.split('/')

        words = filter(None, words)

        path = self.directory

        for word in words:

            if os.path.dirname(word) or word in (os.curdir, os.pardir):
                continue

            path = os.path.join(path, word)

        if trailing_slash:
            path += '/'
        return path

    def copyfile(self, source, outputfile):

        shutil.copyfileobj(source, outputfile)

    def guess_type(self, path):

        base, ext = posixpath.splitext(path)

        if ext in self.extensions_map:
            return self.extensions_map[ext]

        ext = ext.lower()

        if ext in self.extensions_map:
            return self.extensions_map[ext]

        guess, _ = mimetypes.guess_type(path)

        if guess:
            return guess

        return 'application/octet-stream'


if __name__ == "__main__":
    dbfile = Value.path

    try:
        if os.path.getsize(dbfile) == 0:
            Value.path = "x-ui.db"
    except:
        Value.path = "x-ui.db"

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started http://{hostName}:{serverPort}/")

    try:

        webServer.serve_forever()

    except:
        webServer.server_close()
    webServer.server_close()
    print("server stopped.")

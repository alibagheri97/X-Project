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
import socket  # For gethostbyaddr()
import socketserver
import sys
import time
import urllib.parse
import contextlib
from functools import partial
from http import HTTPStatus
from main import addClient, getDetected, getInboundsCount
import json
import qrcode
from sup import *
from sup import pickTag


class Value:
    dic = dict()
    key = ""
    go = "login.html"


def defultPage():
    inbndDf = int(Value.dic["inbndDefult"])
    hostName = list(Value.dic["host"][0].keys())
    htm = read("indexInit.html")
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
                val = f'<button id="bt{i + 1}" class="btn btn-primary border rounded-pill" type="button" style="width: 37.6875px;box-shadow: 0px 0px 3px;margin-left: 10px;{on}background: {bgA};color: {colA};" onclick="check(' + f'{i+1}' + f')">{i + 1}</button>'
            else:
                val = f'<button id="bt{i + 1}" class="btn btn-primary border rounded-pill" type="button" style="width: 37.6875px;box-shadow: 0px 0px 3px;{on}background: {bgA};color: {colA};" onclick="check(' + f'{i+1}' + f')">{i + 1}</button>'
            htm = insert2Tag(htm, 'name="inbndButtons"', val)
        else:
            val2 = ""
            if not i == 0:
                val2 = f'<button id="bt{i + 1}" class="btn btn-primary border rounded-pill" type="button" style="width: 37.6875px;box-shadow: 0px 0px 3px;margin-left: 10px;{on}background: {bgD};color: {colD};" onclick="check(' + f'{i+1}' + f')">{i + 1}</button>'
            else:
                val2 = f'<button id="bt{i + 1}" class="btn btn-primary border rounded-pill" type="button" style="width: 37.6875px;box-shadow: 0px 0px 3px;{on}background: {bgD};color: {colD};" onclick="check(' + f'{i+1}' + f')">{i + 1}</button>'
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
    htm = tagChange(htm, 'name="ipc"', "max", int(Value.dic["maxIpDefult"]))
    htm = tagChange(htm, 'name="ipc"', "value=", int(Value.dic["ipCountDefult"]))
    write("assets/js/theme.js", htm2[:loc[0] + 2] + js + "\n }")
    write("indexRaw.html", htm)


def write(fname, content):
    file = open(fname, "w")
    byt = file.write(content)
    file.close()


def read(fname):
    file = open(fname, "r")
    f = file.read()
    file.close()
    return f


def makeQr(key):
    img = qrcode.make(key)
    img.save('qr.jpg')


write("indexRaw.html", read("indexInit.html"))
Value.dic = json.load(open("settings.json", "r"))

hostName = Value.dic["panelIp"]
serverPort = int(Value.dic["panelPort"])


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
        # file = open("indexRaw.html", "r")
        # htm = file.read()
        # file.close()
        # file = open("index.html", "w")
        # file.write(htm)
        # file.close()
        print(self.client_address[0])
        if Value.go == "index.html":
            defultPage()
            write("index.html", read("indexRaw.html"))
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

        """Common code for GET and HEAD commands.



        This sends the response code and MIME headers.



        Return value is either a file object (which has to be copied

        to the outputfile by the caller unless the command was HEAD,

        and must be closed by the caller under all circumstances), or

        None, in which case the caller has nothing further to do.



        """
        path = self.translate_path(self.path)

        f = None

        if os.path.isdir(path):

            parts = urllib.parse.urlsplit(self.path)

            if not parts.path.endswith('/'):
                # redirect browser - doing basically what apache does

                self.send_response(HTTPStatus.MOVED_PERMANENTLY)

                new_parts = (parts[0], parts[1], parts[2] + '/',

                             parts[3], parts[4])

                print(f"0: {parts[0]}")

                print(f"1: {parts[1]}")

                print(f"2: {parts[2]}")

                print(f"3: {parts[3]}")

                print(f"4: {parts[4]}")

                new_url = urllib.parse.urlunsplit(new_parts)

                self.send_header("Location", new_url)

                self.send_header("Content-Length", "0")

                self.end_headers()

                return None

            new_parts = (parts[0], parts[1], parts[2] + '/',

                         parts[3], parts[4])

            # print(f"0: {parts[0]}")
            #
            # print(f"1: {parts[1]}")
            #
            # print(f"2: {parts[2]}")
            #
            print(f"3: {parts[3]}")
            #
            # print(f"4: {parts[4]}")

            # file = open("indexRaw.html", "r")
            # htm = file.read()
            # file.close()
            # file = open("index.html", "w")
            # file.write(htm)
            # file.close()
            dic = getDetected(parts[3])
            if dic not in [None, dict()]:
                ips = read("ip.txt")
                clientIp = self.client_address[0]
                if not clientIp in ips:
                    if dic["usr"] == Value.dic["panelUsr"] and dic["pass"] == Value.dic["panelPass"]:
                        Value.go = "index.html"
                        write("ip.txt", clientIp+"\n")
                        defultPage()
                        write("index.html", read("indexRaw.html"))
                else:
                    Value.go = "index.html"
                    write("ip.txt", clientIp + "\n")
                    defultPage()
                    write("index.html", read("indexRaw.html"))

                if Value.go == "index.html" and "remark" in list(dic.keys()):
                    vlessK = open("vlessKeys.txt", "r").read()
                    if not dic["remark"] in vlessK:
                        print("ready\n")
                        Value.key = addClient(dic["remark"], dic["ipc"], dic["date"], dic["tgb"], dic["inbnd"], dic["hosts"])
                        print(f"{Value.key}\n")
                    else:
                        Value.key = ""
                # defultPage()
                # read index

                    defultPage()
                    htm = read("indexRaw.html")

                    if Value.key != "":
                        # make Qr
                        makeQr(Value.key)
                        # do changes
                        htm = tagChange(htm, 'name="qrcode"', "style", "Visibility: visible;width: 166px;")
                        htm = tagChange(htm, 'name="txtQr"', "value", Value.key)
                        htm = add2Tag(htm, 'name="qrcode"', "src", "qr.jpg")
                        # save changes
                    write("index.html", htm)

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
                defultPage()
                write("index.html", read("indexRaw.html"))
            for index in Value.go, Value.go[:-1]:

                index = os.path.join(path, index)

                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)

        # check for trailing "/" which should return 404. See Issue17324

        # The test for this was added in test_httpserver.py

        # However, some OS platforms accept a trailingSlash as a filename

        # See discussion on python-dev and Issue34711 regarding

        # parseing and rejection of filenames with a trailing slash

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

        """Helper to produce a directory listing (absent index.html).



        Return value is either a file object, or None (indicating an

        error).  In either case, the headers are sent, making the

        interface the same as for send_head().



        """

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

        """Translate a /-separated PATH to the local filename syntax.



        Components that mean special things to the local file system

        (e.g. drive or directory names) are ignored.  (XXX They should

        probably be diagnosed.)



        """

        # abandon query parameters

        path = path.split('?', 1)[0]

        print(path)

        path = path.split('#', 1)[0]

        # Don't forget explicit trailing slash when normalizing. Issue17324

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
                # Ignore components that are not a simple file/directory name

                continue

            path = os.path.join(path, word)

        if trailing_slash:
            path += '/'

        return path

    def copyfile(self, source, outputfile):

        """Copy all data between two file objects.



        The SOURCE argument is a file object open for reading

        (or anything with a read() method) and the DESTINATION

        argument is a file object open for writing (or

        anything with a write() method).



        The only reason for overriding this would be to change

        the block size or perhaps to replace newlines by CRLF

        -- note however that this the default server uses this

        to copy binary data as well.



        """

        shutil.copyfileobj(source, outputfile)

    def guess_type(self, path):

        """Guess the type of a file.



        Argument is a PATH (a filename).



        Return value is a string of the form type/subtype,

        usable for a MIME Content-type header.



        The default implementation looks the file's extension

        up in the table self.extensions_map, using application/octet-stream

        as a default; however it would be permissible (if

        slow) to look inside the data to make a better guess.



        """

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
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started http://{hostName}:{serverPort}/")

    try:

        webServer.serve_forever()

    except KeyboardInterrupt:
        # file = open("indexRaw.html", "r")
        # htm = file.read()
        # file.close()
        # file = open("index.html", "w")
        # file.write(htm)
        # file.close()
        pass

    webServer.server_close()
    # file = open("indexRaw.html", "r")
    # htm = file.read()
    # file.close()
    # file = open("index.html", "w")
    # file.write(htm)
    # file.close()
    print("server stopped.")


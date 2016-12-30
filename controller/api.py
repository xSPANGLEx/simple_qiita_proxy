#!/usr/bin/python
# -*- coding=utf-8 -*-
import urllib2
import urllib
import chardet

class api:

    def __init__(self):
        self.text = "api"

    def index(self,data):
        header = \
"""<html>
<head>
    <title>QiitaViewer</title>
</head>
<body>
    <form action=/api method="GET">
        <input type="text" name="param">
        <input type="submit" value="submit">
    </form>
<br>
<br>
<br>
<br>
<br>
</body>
</html>"""
        url = data.split("=")[1]
        url = urllib.unquote(url)
        if url.split("/")[0] != "":
            html = urllib2.urlopen("http://qiita.com/"+url).read()
        else:
            html = urllib2.urlopen("http://qiita.com"+url).read()
        html = html.replace("https://qiita-image-store.s3.amazonaws.com/","http://spangle.tk:8000/api/image?param=")
        return header + html,"text/html"

    def image(self,data):
        url = data.split("=")[1]
        url = urllib.unquote(url)
        if url.split("/")[0] != "":
            html = urllib2.urlopen("https://qiita-image-store.s3.amazonaws.com/"+url).read()
        else:
            html = urllib2.urlopen("https://qiita-image-store.s3.amazonaws.com"+url).read()
        return html,"image/png"
        

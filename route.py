#!/usr/bin/python
# -*- coding=utf-8 -*-
import os
import sys
import json

class Route:

    def __init__(self,data):
        self.data = data
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        with open("config/route.json") as configf:
            self.routeConfig = json.load(configf)
        self.url,self.param = self.checkURL()

    def checkMethod(self):
        header = self.data.split("\r\n")[0]
        method = header.split(" ")[0]
        return method

    def checkURL(self):
        header = self.data.split("\r\n")[0]
        _url = header.split(" ")[1]
        if "?" in _url:
            url = _url.split("?")[0]
            param = _url.split("?")[1]
        else:
            url = _url
            param = ""
        return url,param
        
    def getController(self):
        for key in self.routeConfig.keys():
            urls = self.url.split("/")
            if len(urls) == 2:
                if key == self.url:
                    return self.routeConfig[key],"index"
            if key+"/" == self.url:
                return self.routeConfig[key],"index"
            if key == "/".join(urls[0:len(urls)-1]):
                instanceMethod = urls[len(urls)-1].split(".html")[0]
                return (self.routeConfig[key],instanceMethod)
        return None

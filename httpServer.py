#!/usr/bin/python
# -*- coding=utf-8 -*-
import os
import sys
import socket
import json
import glob
import importlib
import route
import threading

class Server:

    def __init__(self,host,port):
        ### Reading config
        os.chdir(os.path.abspath(os.path.dirname(__file__)))
        with open("config/config.json") as configf:
            self.config = json.load(configf)
        ###
        ### Dynamic import controller class
        self.controllerClassList = {}
        controllerList = glob.glob(self.config["mvc_config"]["controller"]+"/*.py")
        for controllerFile in controllerList:
            controllerFile = controllerFile.split(".")[0]
            controllerClass = controllerFile.split("/")
            controllerBaseClass = controllerClass[len(controllerClass)-1]
            if controllerBaseClass == "__init__":
                continue
            controllerClass = ".".join(controllerClass)
            _controllerModule = importlib.import_module(controllerClass)
            self.controllerClassList[str(controllerBaseClass)] = getattr(sys.modules[controllerClass],controllerBaseClass)()
        ###
        ### Dynamic import view class
        self.viewClassList = {}
        viewList = glob.glob(self.config["mvc_config"]["view"]+"/*.py")
        for viewFile in viewList:
            viewFile = viewFile.split(".")[0]
            viewClass = viewFile.split("/")
            viewBaseClass = viewClass[len(viewClass)-1]
            if viewBaseClass == "__init__":
                continue
            viewClass = ".".join(viewClass)
            _viewModule = importlib.import_module(viewClass)
            self.viewClassList[str(viewBaseClass)] = getattr(sys.modules[viewClass],viewBaseClass)()
        ###
        ### Dynamic import model class
        self.modelClassList = {}
        modelList = glob.glob(self.config["mvc_config"]["model"]+"/*.py")
        for modelFile in modelList:
            modelFile = modelFile.split(".")[0]
            modelClass = modelFile.split("/")
            modelBaseClass = modelClass[len(modelClass)-1]
            if modelBaseClass == "__init__":
                continue
            modelClass = ".".join(modelClass)
            _modelModule = importlib.import_module(modelClass)
            self.modelClassList[str(modelBaseClass)] = getattr(sys.modules[modelClass],modelBaseClass)
        ###
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.sock.bind((self.host,self.port))
        self.sock.listen(15)
        print "Serving HTTP on "+socket.gethostbyname(host)+" port "+str(port)+" ..."

    def recv(self):
        while 1:
            clisock,cliaddr = self.sock.accept()
            th = threading.Thread(target=self.controller,args=(clisock,cliaddr))
            th.setDaemon(True)
            th.start()

    def controller(self,sock,addr):
        header = ""
        payloadBuffer = ""
        while 1:
            _recvData = sock.recv(1024)
            if _recvData.split("\n")[0] == "" or _recvData.split("\n")[0] == "\r":
                break
            if "".join(_recvData.split("\n")) == "":
                break
            _recvDatas = _recvData.split("\r\n\r\n")
            if len(_recvDatas) == 2:
                header = header + _recvDatas[0]
                payloadBuffer = _recvDatas[1]
                break
            header = header + _recvData
        _rt = route.Route(header)
        for headerLine in header.split("\r\n"):
            if "Content-Length:" in headerLine:
                contentSize = int(headerLine.split("Content-Length:")[1])
        method = _rt.checkMethod()
        url,param = _rt.checkURL()
        if method == "POST":
            while 1:
                payloadBufferSize = len(payloadBuffer)
                if payloadBufferSize == contentSize:
                    break
                else:
                    payloadBuffer += sock.recv(1024)
        if payloadBuffer == "":
            payloadBuffer = param
        controllerClass = _rt.getController()
        if controllerClass == None:
            sock.send("URL Error")
            sock.close()
            return
        if not controllerClass[1] in dir(self.controllerClassList[controllerClass[0]]):
            sock.send("URL Error")
            sock.close()
            return
        sendData,contentType = getattr(self.controllerClassList[controllerClass[0]],str(controllerClass[1]))(payloadBuffer)
        if sendData.split(":")[0] == "view":
            sendData = getattr(self.viewClassList[sendData.split(":")[1].split("/")[0]],sendData.split(":")[1].split("/")[1])()
        requestHeader = self.responseHeaderGenerator(contentType)
        sock.send(requestHeader+sendData)
        sock.close()

    def responseHeaderGenerator(self,contentType):
        header = "HTTP/1.1 200 OK\r\n"
        header += "Server:spangle-mvc\r\n"
        header += "Content-Type:"+contentType+"\r\n"
        header += "\r\n"
        return header

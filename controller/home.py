#!/usr/bin/python
# -*- coding=utf-8 -*-
import os
import sys
import socket

class home:

    def __init__(self):
        pass

    def index(self,data):
        return "view:home/view","text/html"

    def image(self,data):
        return "view:home/image","text/html"

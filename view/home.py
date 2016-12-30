#!/usr/bin/python
# -*- coding=utf-8 -*-
import os
import sys

class home:

    def __init__(self):
        self.text="homeView"

    def view(self):
        data = \
"""<html>
<head>
    <title>QiitaViewer</title>
</head>
<body>
    <form action=/api method="GET">
        <input type="text" name="param">
        <input type="submit" value="submit">
    </form>
</body>
</html>"""
        return data

    def image(self):
        data = \
"""<html>
<head>
    <title>QittaImageViewer</title>
</head>
<body>
    <form action=/api/image method="GET">
        <input type="text" name="param">
        <input type="submit" value="submit">
    </form>
</body>
</html>"""
        return data


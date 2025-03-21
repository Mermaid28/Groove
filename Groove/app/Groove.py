#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
# @Project ：Groove 
# @File    ：Groove.py.py
# @IDE     ：PyCharm 
# @Author  ：A30041699
# @Date    ：2025/3/18 16:34
# coding:utf-8

import os
import sys
from inspect import getsourcefile
from pathlib import Path

# 改变当前工作目录为脚本所在的目录
os.chdir(Path(getsourcefile(lambda: 0)).resolve().parent)

from PyQt5.QtCore import QLocale, Qt, QTranslator
from PyQt5.QtWidgets import QApplication

from common.application import SingletonApplication
from common.setting import APP_NAME
from common.dpi_manager import DPI_SCALE


# fix bug: qt.qpa.plugin: Could not load the Qt platform plugin "xcb"
if "QT_QPA_PLATFORM_PLUGIN_PATH" in os.environ:
	os.environ.pop("QT_QPA_PLATFORM_PLUGIN_PATH")

# enable high dpi scale
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
os.environ["QT_SCALE_FACTOR"] = str(DPI_SCALE)

QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

app = SingletonApplication(sys.argv, APP_NAME)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)
app.setApplicationName(APP_NAME)
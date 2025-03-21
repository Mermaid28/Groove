#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
# @Project ：Groove 
# @File    ：setting.py
# @IDE     ：PyCharm 
# @Author  ：A30041699
# @Date    ：2025/3/18 17:11
from pathlib import Path
from PyQt5.QtCore import QStandardPaths

"""
根据不同的运行模式（调试模式或正式模式）来设置应用程序配置文件夹的位置。
"""
# change DEBUG to False if you want to compile the code to exe
DEBUG = True

APP_NAME = "Groove"

if DEBUG:
	CONFIG_FOLDER = Path("AppData").absolute()
else:
	CONFIG_FOLDER = Path(QStandardPaths.wtitableLocation(QStandardPaths.AppDataLocation)) / APP_NAME

CONFIG_FILE = CONFIG_FOLDER / "config.json"
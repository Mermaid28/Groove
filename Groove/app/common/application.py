#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
# @Project ：Groove 
# @File    ：application.py
# @IDE     ：PyCharm 
# @Author  ：A30041699
# @Date    ：2025/3/18 17:34
# coding:utf-8

import sys
import traceback
from typing import List

from PyQt5.QtCore import QIODevice, QSharedMemory, pyqtSignal
from PyQt5.QtNetwork import QLocalServer, QLocalSocket
from PyQt5.QtWidgets import QApplication

from .logger import Logger
from .signal_bus import signalBus  # 直接导入了signalBus实例对象

class SingletonApplication(QApplication):
	"""Singleton application"""

	messageSig = pyqtSignal(object)
	logger = Logger("application")

	def __init__(self, argv: List[str], key: str):
		super().__init__(argv)
		self.key = key
		self.timeout = 1000
		self.server = QLocalServer(self)

		# cleanup (only needed for unix)
		QSharedMemory(key).attach()
		self.memory = QSharedMemory(self)
		self.memory.setKey(key)

		if self.memory.attach():
			self.isRunning = True
			self.sendMessage(argv[1] if len(argv) > 1 else "show")
			self.logger.info(
				"Another Groove Music is already running, you should kill it first to launch a new one."
			)
			sys.exit(1)

		self.isRunning = False
		if not self.memory.create(1):
			self.logger.error(self.memory.errorString())
			raise RuntimeError(self.memory.errorString())

		self.server.newConnection().connect(self.__onNewConnection)
		self.server.listen(key)

	def __onNewConnection(self):
		"""
		处理从另一个实例接收到的连接请求。
		如果接收到的请求包含消息，它会通过 signalBus.appMessageSig.emit 发出信号，将消息传递给应用程序。
		:return:
		"""
		socket = self.server.nextPendingConnection()
		if socket.waitForReadyRead(self.timeout):
			signalBus.appMessageSig.emit(socket.readAll().data().decode('utf-8'))
			socket.disconnectFromServer()

	def sendMessage(self, message: str):
		"""
		send message to another application
		向另一个运行中的应用程序实例发送消息。
		使用QLocalSocket与正在运行的应用程序连接，发送消息，并确保消息写入成功。
		:param message:
		:return:
		"""
		if not self.isRunning:
			return

		# connect to another application
		socket = QLocalSocket(self)
		socket.connectToServer(self.key, QIODevice.WriteOnly)
		if not socket.waitForConnected(self.timeout):
			self.logger.error(socket.errorString())
			return

		# send message
		socket.write(message.encode("utf-8"))
		if not socket.waitForBytesWritten(self.timeout):
			self.logger.error(socket.errorString())
			return

		socket.disconnectFromServer()

def exception_hook(exception: BaseException, value, tb):
	"""
	Exception callback function
	这是一个自定义的异常处理钩子（sys.excepthook）。
	当程序抛出未处理的异常时，这个函数会被调用。
	它会记录异常信息到日志中，并将异常详细信息发送到 signalBus.appErrorSig 信号。
	具体来说，traceback.format_tb(tb) 用于获取堆栈跟踪，exception.__name__ 和 value 会提供异常的名称和详细信息。
	"""
	SingletonApplication.logger.error("Unhandled exception", (exception, value, tb))
	message = '\n'.join([''.join(traceback.format_tb(tb)), '{0}: {1}'.format(exception.__name__, value)])
	signalBus.appErrorSig.emit(message)

# 这行代码将 sys.excepthook 设置为 exception_hook，这样当发生未处理的异常时，Python 就会调用 exception_hook 函数。
# exception_hook 会记录错误日志，并通过 signalBus.appErrorSig 将错误信息传递给其他部分
sys.excepthook = exception_hook


# 这段代码是一个基于 PyQt5 的应用程序框架，设计上允许确保同一时间只运行一个实例，同时也提供了日志记录和错误处理的机制。
#
# 下面是对代码的逐步分析：
#
# 1. SingletonApplication 类
# 继承自 QApplication，这个类确保了只有一个应用程序实例能够运行。
# messageSig 是一个信号（pyqtSignal），用于发送消息。
# logger 是一个日志记录器，用于记录应用程序的日志。
# 构造函数 __init__(self, argv: List[str], key: str)：
#
# key: 这是一个唯一的应用程序标识符，通常用于局部服务器通信和共享内存。
# QSharedMemory(key).attach(): 尝试附加一个与应用程序关联的共享内存，目的是检查是否已经有另一个实例在运行。
# 如果共享内存已经附加（即应用程序已经在运行），则会发送消息到另一个实例并退出当前实例。
# 如果共享内存没有附加，表示应用程序是第一次运行，接着会创建共享内存并启动 QLocalServer。
# self.server.listen(key): 启动一个本地服务器监听连接，key 用作服务器的标识符。
# __onNewConnection(self):
#
# 处理从另一个实例接收到的连接请求。
# 如果接收到的请求包含消息，它会通过 signalBus.appMessageSig.emit 发出信号，将消息传递给应用程序。
# sendMessage(self, message: str):
#
# 向另一个运行中的应用程序实例发送消息。
# 使用 QLocalSocket 与正在运行的应用程序连接，发送消息，并确保消息写入成功。
# 2. exception_hook 函数
# 这是一个自定义的异常处理钩子（sys.excepthook）。
# 当程序抛出未处理的异常时，这个函数会被调用。
# 它会记录异常信息到日志中，并将异常详细信息发送到 signalBus.appErrorSig 信号。
# 具体来说，traceback.format_tb(tb) 用于获取堆栈跟踪，exception.__name__ 和 value 会提供异常的名称和详细信息。
# 3. sys.excepthook = exception_hook
# 这行代码将 sys.excepthook 设置为 exception_hook，这样当发生未处理的异常时，Python 就会调用 exception_hook 函数。
# exception_hook 会记录错误日志，并通过 signalBus.appErrorSig 将错误信息传递给其他部分。
# 总结
# SingletonApplication：确保同一时间只运行一个应用程序实例，使用本地服务器和共享内存机制。
# 日志记录：通过 Logger 记录应用程序运行中的信息和错误。
# 异常处理：使用自定义的 exception_hook 捕捉未处理的异常并记录错误，同时通过信号系统将错误信息传递出去。
# sys.excepthook 的作用：它会将所有未处理的异常交由 exception_hook 处理，因此实现了对异常的集中管理。





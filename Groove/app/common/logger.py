#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
# @Project ：Groove 
# @File    ：logger.py
# @IDE     ：PyCharm 
# @Author  ：A30041699
# @Date    ：2025/3/19 10:03

import logging
import weakref

from .setting import CONFIG_FOLDER

LOG_FOLDER = CONFIG_FOLDER / "Log"  # 定义了日志文件存储的文件夹，CONFIG_FOLDER 是一个外部配置的文件夹路径，"Log" 是子文件夹，用于存放日志文件。
_loggers = weakref.WeakValueDictionary()  # 缓存池：使用 WeakValueDictionary 来缓存日志实例。WeakValueDictionary 会在对象没有其他引用时自动删除它，避免内存泄漏。

def loggerCache(cls):
	"""
	decorator for caching logger
	该装饰器用于缓存日志实例
	loggerCache 装饰器的作用是：当调用 Logger 类时，如果指定名称的日志实例已经存在，就直接返回缓存的实例；如果不存在，就创建新的实例并缓存。
	"""

	def wrapper(name, *args, **kwargs):
		if name not in _loggers:
			instance = cls(name, *args, **kwargs)
			_loggers[name] = instance
		else:
			instance = _loggers[name]

		return instance

	return wrapper


@loggerCache
class Logger:
	"""
	Logger class
	Logger 类是日志记录的主要实现类
	"""

	def __init__(self, fileName: str):
		"""
		:param filename: str, log filename which doesn't contain '.log' suffix
		日志文件的名称（不包括 .log 后缀），该文件将存储日志内容。
		"""
		LOG_FOLDER.mkdir(exist_ok=True, parents=True)  # 确保日志文件夹存在。
		self.__logFile = LOG_FOLDER / (fileName + '.log')  # 日志文件目录
		self.__logger = logging.getLogger(fileName)  # 日志实例
		self.__consoleHandler = logging.StreamHandler()  # 日志实例创建时，会初始化两个处理器：一个是控制台输出（StreamHandler），另一个是文件输出（FileHandler）
		self.__fileHandler = logging.FileHandler(self.__logFile, encoding='utf-8')

		# set log level
		self.__logger.setLevel(logging.DEBUG)  # 设置日志级别为 DEBUG，意味着记录所有级别的日志（从 DEBUG 到 CRITICAL）
		self.__consoleHandler.setLevel(logging.DEBUG)
		self.__fileHandler.setLevel(logging.DEBUG)

		# set log format
		fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # 设置日志的格式：时间戳、日志级别、日志消息
		self.__consoleHandler.setFormatter(fmt)
		self.__fileHandler.setFormatter(fmt)

		# 如果没有处理器，分别为控制台和文件添加处理器
		if not self.__logFile.hasHandlers():
			self.__logger.addHandler(self.__consoleHandler)
			self.__logger.addHandler((self.__fileHandler))

	# info, error, debug, warning, critical：这些是实际记录日志的方法，调用这些方法会记录不同级别的日志。
	def info(self, msg):
		self.__logger.info(msg)

	def error(self, msg):
		self.__logger.error(msg)

	def debug(self, msg):
		self.__logger.error(msg)

	def warning(self, msg):
		self.__logger.warning(msg)

	def critical(self, mag):
		self.__logger.critical(mag)


# 使用方式
# 通过 loggerCache 装饰器装饰后的 Logger 类会缓存日志实例。例如，你可以这样使用：
# log1 = Logger("my_log")
# log1.info("This is an info message.")
#
# log2 = Logger("my_log")
# log2.error("This is an error message.")
# 在这个例子中，由于 "my_log" 名称相同，第二次创建 Logger 实例时会直接获取缓存中的实例，避免创建新的日志对象。
#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
# @Project ：Groove 
# @File    ：config.py
# @IDE     ：PyCharm 
# @Author  ：A30041699
# @Date    ：2025/3/20 10:33

import json
import sys
from enum import Enum
from pathlib import Path
from typing import Iterable, List, Union

import darkdetect
from PyQt5.QtCore import Qt, QStandardPaths, QObject, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QGuiApplication
from PyQt5.QtMultimedia import QMediaPlaylist

from .quality import MvQuality, SongQuality
from .exception_handler import exceptionHandler
from .singleton import Singleton
from .setting import APP_NAME, CONFIG_FOLDER, CONFIG_FILE

class Language(Enum):
	""" Language enumeration
	这段代码定义了一个 Language 枚举类，使用了 Python 的 Enum 类型。让我们逐行解释它的含义：

	1. class Language(Enum):
	定义了一个名为 Language 的枚举类。Enum 是 Python 中用于创建枚举的基类，通过继承 Enum 类，你可以定义一组有名字和值的常量。

	2. ‘’‘ Language enumeration ’‘’
	这行是一个文档字符串（docstring），它对类 Language 进行了简短的说明，表示这个类是用于枚举语言类型的。

	3. CHINESE_SIMPLIFIED = "zh"
	这是 Language 枚举中的第一个成员，表示简体中文语言。它的名字是 CHINESE_SIMPLIFIED，它的值是 "zh"，通常用于表示简体中文。

	4. CHINESE_TRADITIONAL = "hk"
	这是枚举中的第二个成员，表示繁体中文语言。它的名字是 CHINESE_TRADITIONAL，它的值是 "hk"，这通常与香港使用的繁体中文相对应。

	5. ENGLISH = "en"
	这是枚举中的第三个成员，表示英文语言。它的名字是 ENGLISH，它的值是 "en"，表示英语。

	6. AUTO = "Auto"
	这是枚举中的第四个成员，表示自动语言选择。它的名字是 AUTO，它的值是 "Auto"，可以用于某些情况下系统自动选择语言。

	总结:
	这个 Language 类定义了一个语言的枚举，其中包括了简体中文、繁体中文、英文和自动语言选择。每个枚举成员都有一个名字和对应的值。例如，Language.CHINESE_SIMPLIFIED 的值是 "zh"，Language.ENGLISH 的值是 "en"。

	使用枚举的好处是，它提供了对常量值的命名，可以帮助代码更具可读性和可维护性，同时避免了使用魔法字符串或硬编码值。
	"""

	CHINESE_SIMPLIFIED = "zh"
	CHINESE_TRADITIONAL = "hk"
	ENGLISH = "en"
	AUTO = "Auto"


class Theme(Enum):
	""" Theme enumeration """

	LIGHT = "Light"
	DARK = "Dark"
	AUTO = "Auto"


"""
这个代码定义了一个 ConfigValidator 类及其多个子类，目的是提供对不同类型配置值的验证和纠正。每个子类负责特定类型的验证，如范围验证、选项验证、布尔值验证、文件夹验证等。让我们逐个分析这些类和方法的含义：

1. ConfigValidator 类
这是一个基类，用于定义配置验证器的基础功能。

validate(self, value) -> bool: 用于验证某个值是否合法。默认实现是返回 True，表示所有值都合法。
correct(self, value): 用于修正非法值。默认实现是直接返回传入的值。
2. RangeValidator 类
RangeValidator 继承自 ConfigValidator，用于验证数值是否在一个给定的范围内。

__init__(self, min, max): 构造函数接受两个参数 min 和 max，定义合法值的范围。
validate(self, value) -> bool: 检查给定的值是否在 min 和 max 之间。
correct(self, value): 如果值不在合法范围内，将其修正为 min 和 max 之间的值，使用 min(max(self.min, value), self.max) 来确保值在合法范围内。
3. OptionsValidator 类
OptionsValidator 继承自 ConfigValidator，用于验证值是否在一组合法选项中。

__init__(self, options: Union[Iterable, Enum]): 构造函数接受一个选项列表或枚举类型。如果是枚举类型，则转换为选项列表。
validate(self, value) -> bool: 检查给定的值是否是合法选项之一。
correct(self, value): 如果值不是合法选项之一，则返回选项列表中的第一个值。
4. BoolValidator 类
BoolValidator 继承自 OptionsValidator，专门用于验证布尔值。

__init__(self): 调用父类构造函数，定义合法选项为 [True, False]，即布尔值 True 或 False。
5. FolderValidator 类
FolderValidator 继承自 ConfigValidator，用于验证给定的路径是否是有效的文件夹。

validate(self, value: Union[str, Path]) -> bool: 检查给定的值（路径）是否存在。
correct(self, value: Union[str, Path]): 如果文件夹不存在，尝试创建该文件夹。如果路径有效，则返回绝对路径。
6. FolderListValidator 类
FolderListValidator 继承自 ConfigValidator，用于验证给定的路径列表中的所有路径是否有效。

validate(self, value: List[Union[str, Path]]) -> bool: 检查列表中的每个路径是否存在。
correct(self, value: List[Union[str, Path]]): 对于列表中的每个路径，检查路径是否存在并返回绝对路径列表。
7. ColorValidator 类
ColorValidator 继承自 ConfigValidator，用于验证 RGB 颜色值是否合法。

__init__(self, default): 构造函数接受一个默认颜色值。
validate(self, color) -> bool: 使用 QColor 类来验证给定的颜色值是否合法。QColor 是 PyQt 中的颜色类，isValid() 方法检查颜色是否有效。
correct(self, value): 如果颜色无效，返回默认颜色。否则，返回验证过的颜色值。
总结
这些类提供了一些常用的配置验证功能，可以确保传入的配置值符合预期的类型、范围或格式，并在必要时进行修正。每个验证器都继承自 ConfigValidator 类，并重写了 validate 和 correct 方法。这样设计的好处是可以在程序中对配置进行统一、灵活的验证和修正。

例如，如果你有一个配置项需要是一个有效的文件夹路径，FolderValidator 可以用来验证路径是否合法，如果不合法，可以通过 correct 方法自动创建文件夹。
"""
class ConfigValidator:
	""" config validator """

	def validate(self, value):
		""" verify whether the value is legal """
		return True

	def correct(self, value):
		""" correct illegal value """
		return value

class RangeValidator(ConfigValidator):
	""" Range validator """

	def __init__(self, min, max):
		self.min = min
		self.max = max
		self.range = (min, max)

	def validate(self, value) -> bool:
		return self.min <= value <= self.max

	def correct(self, value):
		return min(max(self.min, value), self.max)


class OptionsValidator(ConfigValidator):
	""" Options validator """

	def __init__(self, options: Union[Iterable, Enum]) -> None:
		if not options:
			raise ValueError("The `options` can't be empty.")

		if isinstance(options, Enum):
			options = options._member_map_.values()

		self.options = list(options)

	def validate(self, value) -> bool:
		return value in self.options

	def correct(self, value):
		return value if self.validate(value) else self.options[0]


class BoolValidator(OptionsValidator):
	""" Boolean validator """

	def __init__(self):
		super().__init__([True, False])


class FolderValidator(ConfigValidator):
	""" Folder validator """

	def validate(self, value: Union[str, Path]) -> bool:
		return Path(value).exists()

	def correct(self, value: Union[str, Path]):
		path = Path(value)
		try:
			path.mkdir(exist_ok=True, parents=True)
		except:
			pass
		return str(path.absolute()).replace("\\", "/")  # 返回绝对路径


class FolderListValidator(ConfigValidator):
	""" Folder list validator """

	def validate(self, value: List[Union[str, Path]]) -> bool:
		return all(Path(i).exists() for i in value)

	def correct(self, value: List[Union[str, Path]]):
		folders = []
		for folder in value:
			path = Path(folder)
			if path.exists():
				folders.append(str(path.absolute()).replace("\\", "/"))

		return folders


class ColorValidator(ConfigValidator):
	""" RGB color validator """

	def __init__(self, default):
		self.default = QColor(default)

	def validate(self, color) -> bool:
		try:
			return QColor(color).isValid()
		except:
			return False

	def correct(self, value):
		return QColor(value) if self.validate(value) else self.default


"""
这些代码定义了一些用于配置序列化和反序列化的类。每个类负责将特定类型的数据转换为可以保存到配置文件中的格式（序列化），以及从配置文件中恢复数据到相应的对象类型（反序列化）。

1. ConfigSerializer 类
这是一个基类，用于序列化和反序列化配置值。它提供了默认的 serialize 和 deserialize 方法，这两个方法都直接返回传入的值，表示没有任何处理。

serialize(self, value): 用于将配置值序列化，默认返回原始值。
deserialize(self, value): 用于从配置文件的值中反序列化数据，默认返回原始值。
2. EnumSerializer 类
EnumSerializer 继承自 ConfigSerializer，用于处理 Enum 类型的序列化和反序列化。

__init__(self, enumClass): 构造函数接收一个枚举类（enumClass），用来指定要处理的枚举类型。
serialize(self, value: Enum): 将一个枚举值序列化为其对应的值（即枚举成员的值）。
deserialize(self, value): 将一个枚举值（通常是一个基本类型的值，如字符串或整数）反序列化为该枚举类型的实例。
示例：
假设有一个枚举类型：

python
from enum import Enum

class Color(Enum):
	RED = 1
	GREEN = 2
	BLUE = 3
你可以使用 EnumSerializer 来序列化和反序列化 Color 枚举：

python
serializer = EnumSerializer(Color)
serialized = serializer.serialize(Color.RED)  # serialized = 1
deserialized = serializer.deserialize(1)  # deserialized = Color.RED
3. ColorSerializer 类
ColorSerializer 继承自 ConfigSerializer，用于处理 QColor 对象的序列化和反序列化。

serialize(self, value: QColor): 将一个 QColor 对象序列化为其颜色的名称（例如 "#FF5733"）。
deserialize(self, value): 将一个颜色值（可以是一个字符串或一个 RGB 数值列表）反序列化为一个 QColor 对象。如果传入的是一个列表，它会创建一个新的 QColor 实例。
示例：
假设有一个 QColor 对象：

python
from PyQt5.QtGui import QColor

color = QColor(255, 87, 51)
使用 ColorSerializer 进行序列化和反序列化：

python
serializer = ColorSerializer()
serialized = serializer.serialize(color)  # serialized = "#FF5733"
deserialized = serializer.deserialize("#FF5733")  # deserialized = QColor(255, 87, 51)
4. PlaybackModeSerializer 类
PlaybackModeSerializer 继承自 ConfigSerializer，用于处理 QMediaPlaylist.PlaybackMode 枚举值的序列化和反序列化。

serialize(self, value: QMediaPlaylist.PlaybackMode): 将 QMediaPlaylist.PlaybackMode 类型的值序列化为整数值（通常 QMediaPlaylist.PlaybackMode 是一个枚举类型，表示播放模式）。
deserialize(self, value): 将一个整数值反序列化为对应的 QMediaPlaylist.PlaybackMode 枚举值。
示例：
假设有 QMediaPlaylist.PlaybackMode 枚举：

python
from PyQt5.QtMultimedia import QMediaPlaylist

mode = QMediaPlaylist.PlaybackMode.CurrentItemInLoop
使用 PlaybackModeSerializer 进行序列化和反序列化：

python
serializer = PlaybackModeSerializer()
serialized = serializer.serialize(mode)  # serialized = 2 (假设当前模式的整数值为 2)
deserialized = serializer.deserialize(2)  # deserialized = QMediaPlaylist.PlaybackMode.CurrentItemInLoop
总结
这些类提供了将特定类型的配置值（例如枚举、颜色、播放模式等）序列化为适合存储的格式，并且能够将这些格式反序列化回原始类型。每个类通过继承自 ConfigSerializer 类，定义了如何处理其特定类型的数据，确保数据在配置文件中的持久化和恢复过程顺利进行。
"""
class ConfigSerializer:
	""" Config serializer """

	def serialize(self, value):
		""" serialize config value """
		return value

	def deserialize(self, value):
		""" deserialize config from config file's value """
		return value


class EnumSerializer(ConfigSerializer):
	""" enumeration class serializer """

	def __init__(self, enumClass):
		self.enumClass = enumClass

	def serialize(self, value: Enum):
		return value.value

	def deserialize(self, value):
		return self.enumClass(value)


class ColorSerializer(ConfigSerializer):
	""" QColor serializer """

	def serialize(self, value: QColor):
		return value.name()

	def deserialize(self, value):
		if isinstance(value, list):
			return QColor(*value)

		return QColor(value)


class PlaybackModeSerializer(ConfigSerializer):
	""" Playback mode class serializer """

	def serialize(self, value: QMediaPlaylist.PlaybackMode):
		return int(value)

	def deserialize(self, value):
		return QMediaPlaylist.PlaybackMode(value)


"""
这段代码定义了一个配置项系统，并且创建了多个配置项类型的类，主要用于管理一些配置项的值，验证这些值，序列化和反序列化，以及在某些情况下控制程序是否需要重启。这里每个类的具体含义和作用如下：

ConfigItem 类
这个类代表一个通用的配置项，包含了以下功能：

初始化 (__init__):

group：配置项所属的组（例如，数据库配置、UI 配置等）。
name：配置项的名称。
default：配置项的默认值。
validator：用于验证配置项的值的验证器（可选）。
serializer：用于序列化和反序列化配置项值的序列化器（可选）。
restart：指示更新配置项时是否需要重启应用（默认为 False）。
value 属性: 获取和设置配置项的值。每次设置新值时，都会通过 validator 对其进行验证。

key 属性: 返回配置项的键值，通常是以“组名.项名”格式表示，用于标识该配置项。

serialize 和 deserializeFrom 方法: 分别用于将配置项的值序列化为特定格式，和将序列化后的数据反序列化为配置项值。

RangeConfigItem 类
这是 ConfigItem 的一个子类，专门处理具有范围限制的配置项。它通过 range 属性提供配置项的可用范围，通常用来处理需要限定在某个值范围内的配置项。

OptionsConfigItem 类
这是 ConfigItem 的另一个子类，专门处理具有选项的配置项（例如，选择列表、枚举值等）。它通过 options 属性返回可选值列表，用于限定配置项值的合法性。

ColorConfigItem 类
这个类继承自 ConfigItem，并且专门处理颜色类型的配置项。它通过将默认值包装成 QColor 对象并使用 ColorValidator 和 ColorSerializer 进行验证和序列化，从而处理与颜色相关的配置项。

总结：
这些类主要用于处理各种类型的配置项，确保配置项的合法性（通过验证器），并且能够将配置项值转换为特定的格式进行存储和恢复（通过序列化器）。子类如 RangeConfigItem 和 OptionsConfigItem 用于处理有特殊限制条件的配置项（例如值范围或可选值）。而 ColorConfigItem 处理颜色类型的配置项，默认值使用了 QColor 对象来表示颜色。
"""
class ConfigItem:
	""" Config item """

	def __init__(self, group: str, name: str, default, validator: ConfigValidator = None,
				 serializer: ConfigSerializer = None, restart=False):
		"""
		Parameters
		----------
		group: str
			config group name

		name: str
			config item name, can be empty

		default:
			default value

		options: list
			options value

		serializer: ConfigSerializer
			config serializer

		restart: bool
			whether to restart the application after updating the configuration item
		"""
		self.group = group
		self.name = name
		self.validator = validator or ConfigValidator()
		self.serializer = serializer or ConfigSerializer()
		self.__value = default
		self.value = default
		self.restart = restart

	@property
	def value(self):
		""" get the value of config item """
		return self.__value

	@value.setter
	def value(self, v):
		self.__value = self.validator.correct(v)

	@property
	def key(self):
		""" get the config key separated by `.` """
		return self.group+"."+self.name if self.name else self.group

	def serialize(self):
		return self.serializer.serialize(self.value)

	def deserializeFrom(self, value):
		self.value = self.serializer.deserialize(value)


class RangeConfigItem(ConfigItem):
	""" Config item of range """

	@property
	def range(self):
		""" get the available range of config """
		return self.validator.range


class OptionsConfigItem(ConfigItem):
	""" Config item with options """

	@property
	def options(self):
		return self.validator.options


class ColorConfigItem(ConfigItem):
	""" Color config item """

	def __init__(self, group: str, name: str, default, restart=False):
		super().__init__(group, name, QColor(default),
						 ColorValidator(default), ColorSerializer(), restart)

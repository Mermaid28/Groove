#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
# @Project ：Groove 
# @File    ：singleton.py
# @IDE     ：PyCharm 
# @Author  ：A30041699
# @Date    ：2025/3/20 10:59
class Singleton:
	"""
	单例类
	这段代码定义了一个 Singleton 类，它实现了 单例模式 (Singleton Pattern)。单例模式确保一个类只有一个实例，并提供一个全局访问点来获取该实例。

	我们来逐行分析这段代码：

	1. class Singleton:
	这行定义了一个名为 Singleton 的类。

	2. def __new__(cls, *args, **kwargs):
	这是 __new__ 方法的定义，它是 Python 中创建新实例时调用的方法。__new__ 方法的作用是在实例化时返回一个新的对象，通常和 __init__ 方法一起使用。

	cls: 表示类本身（而不是实例）。在类方法中，通常使用 cls 作为类的引用。
	*args, **kwargs: 允许传递任意数量的位置参数和关键字参数。
	3. if not hasattr(cls, '_instance'):
	这个条件检查类是否已经有了 _instance 这个属性。_instance 属性用于存储这个类的唯一实例。

	hasattr(cls, '_instance'): 检查类 cls 是否已经有 _instance 这个属性。
	4. cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
	如果类 cls 没有 _instance 属性，说明该类还没有实例化过，那么我们就通过 super(Singleton, cls).__new__(cls, *args, **kwargs) 创建一个新实例并赋值给 cls._instance。super(Singleton, cls) 调用父类的 __new__ 方法，用于创建一个新对象。

	super(Singleton, cls).__new__(cls): 这个语法通过调用父类 Singleton 的 __new__ 方法来创建一个新实例。
	5. return cls._instance
	每次调用 __new__ 方法时，它都会返回 cls._instance，而不是每次都创建一个新的实例。因此，如果实例已经创建，__new__ 方法会返回同一个实例。

	总结:
	这个代码实现了 单例模式，确保 Singleton 类只有一个实例。如果我们多次实例化 Singleton 类，它将始终返回同一个实例，而不会创建新的对象。
	"""
	def __new__(cls, *args, **kwargs):
		if not hasattr(cls, '_instance'):
			cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)

		return cls._instance
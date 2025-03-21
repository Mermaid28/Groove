#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
# @Project ：Groove 
# @File    ：signal_bus.py
# @IDE     ：PyCharm 
# @Author  ：A30041699
# @Date    ：2025/3/19 12:12
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtMultimedia import QMediaPlaylist

from common.crawler import SongQuality, QueryServerType

from .database.entity import AlbumInfo, SingerInfo, SongInfo
from .singleton import Singleton


class SignalBus(Singleton, QObject):
    """ Signal bus in Groove Music
    SignalBus 类：SignalBus 类继承了 QObject 和 Singleton，
    它作为一个信号总线（Signal Bus）用来管理和广播各种信号。
    在 PyQt 中，信号用于在对象之间进行通信。例如，其他模块可以通过 signalBus 来触发播放音乐、切换界面、调整音量等操作。

	Singleton：SignalBus 继承了 Singleton，这意味着它是一个单例类。
	单例模式确保在应用程序中 SignalBus 只有一个实例，
	这样就能避免多个 SignalBus 实例的创建，确保信号总线的唯一性和统一性。

	QObject：SignalBus 还继承自 QObject，这是 PyQt5 中所有对象的基类。
	它提供了事件处理机制，信号槽机制等，允许在对象间传递信号。

	创建实例 signalBus：signalBus = SignalBus() 这行代码实际上是创建 SignalBus 类的一个实例。
	此实例会持有并管理所有信号，其他部分的代码可以通过 signalBus 来连接和发射这些信号。

	通过 signalBus，程序的不同部分可以通过信号与其他部分通信，触发事件或通知其他模块。
	信号机制是 PyQt 中的核心特性之一，它允许解耦对象之间的关系，使得程序更加灵活和易于维护。
	"""

    appMessageSig = pyqtSignal(object)          # APP 发来消息
    appErrorSig = pyqtSignal(str)               # APP 发生异常
    appRestartSig = pyqtSignal()                # APP 需要重启

    randomPlayAllSig = pyqtSignal()             # 无序播放所有
    playCheckedSig = pyqtSignal(list)           # 播放选中的歌曲
    nextToPlaySig = pyqtSignal(list)            # 下一首播放
    playAlbumSig = pyqtSignal(str, str)         # 播放专辑
    playOneSongCardSig = pyqtSignal(SongInfo)   # 将播放列表重置为一首歌
    playPlaylistSig = pyqtSignal(list, int)     # 播放歌曲列表

    playBySongInfoSig = pyqtSignal(SongInfo)          # 更新歌曲卡列表控件的正在播放歌曲
    getAlbumDetailsUrlSig = pyqtSignal(AlbumInfo)     # 在线查看专辑详细信息
    getSingerDetailsUrlSig = pyqtSignal(SingerInfo)   # 在线查看歌手详细信息
    getSongDetailsUrlSig = pyqtSignal(SongInfo, QueryServerType)  # 在线查看歌曲详细信息

    addSongsToPlayingPlaylistSig = pyqtSignal(list)      # 添加到正在播放
    addSongsToNewCustomPlaylistSig = pyqtSignal(list)    # 添加到新建自定义播放列表
    addSongsToCustomPlaylistSig = pyqtSignal(str, list)  # 添加到自定义播放列表
    addFilesToCustomPlaylistSig = pyqtSignal(str, list)  # 添加本地文件到播放列表

    editSongInfoSig = pyqtSignal(SongInfo, SongInfo)          # 编辑歌曲信息
    editAlbumInfoSig = pyqtSignal(AlbumInfo, AlbumInfo, str)  # 编辑专辑信息

    removeSongSig = pyqtSignal(list)            # 删除本地歌曲
    clearPlayingPlaylistSig = pyqtSignal()      # 清空正在播放列表
    deletePlaylistSig = pyqtSignal(str)         # 删除自定义播放列表
    renamePlaylistSig = pyqtSignal(str, str)    # 重命名自定义播放列表

    selectionModeStateChanged = pyqtSignal(bool)  # 进入/退出 选择模式

    showPlayingPlaylistSig = pyqtSignal()                        # 显示正在播放列表
    switchToPlayingInterfaceSig = pyqtSignal()                   # 显示正在播放界面信号
    switchToSettingInterfaceSig = pyqtSignal()                   # 切换到设置界面信号
    switchToSingerInterfaceSig = pyqtSignal(str)                 # 切换到歌手界面
    switchToAlbumInterfaceSig = pyqtSignal(str, str)             # 切换到专辑界面
    switchToMyMusicInterfaceSig = pyqtSignal()                   # 切换到我的音乐界面
    switchToRecentPlayInterfaceSig = pyqtSignal()                # 切换到最近播放界面
    switchToPlaylistInterfaceSig = pyqtSignal(str)               # 切换到播放列表界面信号
    switchToPlaylistCardInterfaceSig = pyqtSignal()              # 切换到播放列表卡界面
    switchToSmallestPlayInterfaceSig = pyqtSignal()              # 显示最小播放模式界面
    switchToVideoInterfaceSig = pyqtSignal(str, str)             # 切换到视频界面
    switchToLabelNavigationInterfaceSig = pyqtSignal(list, str)  # 显示标签导航界面
    switchToMoreSearchResultInterfaceSig = pyqtSignal(str, str, list) # 切换到更多搜索结果界面


    nextSongSig = pyqtSignal()             # 下一首
    lastSongSig = pyqtSignal()             # 上一首
    togglePlayStateSig = pyqtSignal()      # 播放/暂停
    progressSliderMoved = pyqtSignal(int)  # 播放进度条滑动
    downloadSongSig = pyqtSignal(SongInfo, SongQuality)   # 开始下载一首歌
    downloadSongsSig = pyqtSignal(list, SongQuality)   # 开始下载多首歌

    muteStateChanged = pyqtSignal(bool)   # 静音
    volumeChanged = pyqtSignal(int)       # 调整音量

    randomPlayChanged = pyqtSignal(bool)                        # 随机播放
    loopModeChanged = pyqtSignal(QMediaPlaylist.PlaybackMode)   # 循环模式

    playSpeedUpSig = pyqtSignal()       # 加速播放
    playSpeedDownSig = pyqtSignal()     # 减速播放
    playSpeedResetSig = pyqtSignal()    # 恢复播放速度

    writePlayingSongStarted = pyqtSignal()     # 开始向正在播放的歌曲写入数据
    writePlayingSongFinished = pyqtSignal()    # 完成向正在播放的歌曲写入数据

    showMainWindowSig = pyqtSignal()      # 显示主界面
    fullScreenChanged = pyqtSignal(bool)  # 全屏/退出全屏

    downloadAvatarFinished = pyqtSignal(str, str)  # 下载了一个头像

    totalOnlineSongsChanged = pyqtSignal(int)      # 搜索到的在线音乐总数发生变化

    lyricFontChanged = pyqtSignal(QFont)                       # 正在播放界面歌词字体改变
    albumBlurRadiusChanged = pyqtSignal(int)                   # 正在播放界面背景磨砂半径改变

    desktopLyricStyleChanged = pyqtSignal()              # 桌面歌词样式改变


signalBus = SignalBus()


# signalBus = SignalBus() 这一行代码创建了一个名为 signalBus 的实例，类型为 SignalBus 类。
#
# 具体解释如下：
#
# SignalBus 类：SignalBus 类继承了 QObject 和 Singleton，它作为一个信号总线（Signal Bus）用来管理和广播各种信号。在 PyQt 中，信号用于在对象之间进行通信。例如，其他模块可以通过 signalBus 来触发播放音乐、切换界面、调整音量等操作。
#
# Singleton：SignalBus 继承了 Singleton，这意味着它是一个单例类。单例模式确保在应用程序中 SignalBus 只有一个实例，这样就能避免多个 SignalBus 实例的创建，确保信号总线的唯一性和统一性。
#
# QObject：SignalBus 还继承自 QObject，这是 PyQt5 中所有对象的基类。它提供了事件处理机制，信号槽机制等，允许在对象间传递信号。
#
# 创建实例 signalBus：signalBus = SignalBus() 这行代码实际上是创建 SignalBus 类的一个实例。此实例会持有并管理所有信号，其他部分的代码可以通过 signalBus 来连接和发射这些信号。
#
# 通过 signalBus，程序的不同部分可以通过信号与其他部分通信，触发事件或通知其他模块。信号机制是 PyQt 中的核心特性之一，它允许解耦对象之间的关系，使得程序更加灵活和易于维护。
#!/usr/bin/env python
# coding: utf-8
#
# This file is part of Kacho
#
# Copyright (C) 2011 Junichi Shinohara <tabe1hands@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import fcntl

from kacho.lib import check

class Open:
    """
    ロックを使用して安全にファイルのread/writeを行うクラス
    """

    _data = {}
    _read_file = None
    _write_file = None

    def __init__(self, path):
        self._path = path

    def __lock_SH(self, f):
        """
        共有ロックを取得(読み込みの時に使用)
        </comment-en>
        """
        fcntl.lockf(f.fileno(), fcntl.LOCK_SH)
        
    def __lock_EX(self, f):
        """
        排他的ロックを取得(書き込みの時に使用)
        """
        fcntl.lockf(f.fileno(), fcntl.LOCK_EX)
        
    def __lock_UN(self, f):
        """
        アンロック(読み込み/書き込みの時に使用) 
        """
        fcntl.lockf(f.fileno(), fcntl.LOCK_UN)

    def read(self):
        if not check.type_read_file(self._path):
            return False

        self._read_file = open(self._path, 'r')
        try:
            self.__lock_SH(self._read_file)
            return self._read()
        finally:
            self.__lock_UN(self._read_file)
            self._read_file.close()
        return True

    def write(self):
        if not check.type_write_file(self._path):
            return False

        self._write_file = open(self._path, "w")
        try:
            self.__lock_EX(self._write_file)
            return self._write()
        finally:
            self.__lock_UN(self._write_file)
            self._write_file.close()
        return True

    def _read(self):
        raise NotImplementedError('Please implemente')

    def _write(self, data):
        raise NotImplementedError('Please implemente')

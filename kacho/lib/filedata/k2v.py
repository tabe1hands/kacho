#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of Karesansui Core.
#
# Copyright (C) 2009-2010 HDE, Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#

import re
import os
from copy import copy

from kacho.lib.filedata import secure

class Open(secure.Open):
    """
    key=value形式のファイルのread/writeを行うクラス
    """

    def _read(self):
        """
        設定ファイルの読み込みを行います。
        """
        data = self._data
        f = self._read_file
        if not f:
            return False

        for line in f.readlines():
            line = line.strip()
            if len(line) <= 0 or line[0] == "#":
                continue
            key, value = line.split('=',1)
            if not value.rfind('#') == -1:
                value = value[:value.rfind('#')]
            data[key] = value.strip()
        return data

    def _write(self, data):
        """
        データを、読み込んだデータとマージ(上書き)します。
        """
        rewrite_data = copy(self._data)
        f = self._write_file
        if not f:
            return False

        for key, value in data.iteritems():
            rewrite_data[key] = value

        for rewrite_key, rewrite_value in rewrite_data.iteritems():
            f.write("%s=%s%s" % (rewrite_key, rewrite_value, os.linesep))
        return True

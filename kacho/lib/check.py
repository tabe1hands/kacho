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

import os
import re

from const import UUID_REGEX

def type_uuid(target):
    _uuid = re.compile(UUID_REGEX)
    if _uuid.match(target):
        return True
    else:
        return False

def type_read_file(target):
    if os.access(os.path.abspath(target), os.R_OK):
        return True
    else:
        return False

def type_write_file(target):
    if os.access(os.path.abspath(target), os.R_OK|os.W_OK):
        return True
    else:
        return False

def type_file(target):
    if os.path.isfile(os.path.abspath(target)):
        return True
    else:
        return False

def type_dir(target):
    if os.path.isdir(os.path.abspath(target)):
        return True
    else:
        return False

def type_int(target):
    try:
        ret = int(target)
        return True
    except (TypeError, ValueError):
        return False

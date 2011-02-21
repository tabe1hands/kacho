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

import sys
from optparse import OptionParser, OptionValueError

from twisted.python import log
from twisted.internet import reactor
import cyclone.web

import kacho
from kacho.lib import check, filedata
from kacho.urls import urls

def get_options():
    usage = "%prog [options]"
    version = 'kacho %s' % kacho.__version__
    optp = OptionParser(usage=usage, version=version)
    optp.add_option(
            '-c', '--config', dest='config_path', 
            help='Configuration file of application')
    optp.add_option(
            '-s', '--shell', dest='shell', 
            action="store_true", help='Start at the terminal.(IPython)')
    return optp.parse_args()

def check_options(opts):
    if not opts.config_path:
        print >>sys.stderr, '-c or --config is required.'
        return False

    if not check.type_read_file(opts.config_path):
        print >>sys.stderr, '-c or --config file is specified in the option does not exist.'
        return False
    return True

def check_config(config):
    normal = True

    if normal and not 'log.config' in config:
        print >>sys.stderr, 'Configuration information is missing. - log.config'
        normal = False
    if normal and not check.type_file(config["log.config"]):
        print >>sys.stderr, 'There is a mistake in the configuration information. - log.config=%s' % config["log.config"]
        normal = False

    if normal and not 'bin.dir' in config:
        print >>sys.stderr, 'Configuration information is missing. - bin.dir'
        normal = False
    if normal and not check.type_dir(config["bin.dir"]):
        print >>sys.stderr, 'There is a mistake in the configuration information. - bin.dir=%s' % config["bin.dir"]
        normal = False
    if normal and not check.type_read_file(config["bin.dir"]):
        print >>sys.stderr, 'Not set the appropriate permissions to that directory. - bin.dir=%s' % config["bin.dir"]
        normal = False

    if normal and not 'tmp.dir' in config:
        print >>sys.stderr, 'Configuration information is missing. - tmp.dir'
        normal = False
    if normal and not check.type_dir(config["tmp.dir"]):
        print >>sys.stderr, 'There is a mistake in the configuration information. - tmp.dir=%s' % config["tmp.dir"]
        normal = False
    if normal and not check.type_write_file(config["tmp.dir"]):
        print >>sys.stderr, 'Not set the appropriate permissions to that directory. - tmp.dir=%s' % config["tmp.dir"]
        normal = False

    if normal and not 'server.interface' in config:
        print >>sys.stderr, 'Configuration information is missing. - server.interface'
        normal = False

    if normal and not 'server.port' in config:
        print >>sys.stderr, 'Configuration information is missing. - server.port'
        normal = False
    if normal and not check.type_int(config["server.port"]):
        print >>sys.stderr, 'Please set it by the numerical value. - server.port=%s' % config['server.port']
        normal = False

    if normal and not 'uniqkey' in config:
        print >>sys.stderr, 'Configuration information is missing. - uniqkey'
        normal = False
    if normal and not check.type_uuid(config["uniqkey"]):
        print >>sys.stderr, 'UUID format is not set. - uniqkey'
        normal = False

    return normal

def build_in_server(config_data):
    reactor.listenTCP(int(config_data['server.port']), Application())
    reactor.run()
    return True

class Application(cyclone.web.Application):
    def __init__(self):
        handlers = urls
        cyclone.web.Application.__init__(self, handlers)

if __name__ == "__main__":
    # オプション解析
    (opts, args) = get_options()
    if not check_options(opts):
        sys.exit(1)

    config_path = opts.config_path

    # 設定ファイル読み込み
    _f = filedata.k2v.Open(config_path)
    config_data = _f.read()

    if not check_config(config_data):
        sys.exit(2)

    # ロギング
    #log.startLogging(sys.stdout)

    # サーバー実行
    build_in_server(config_data)
else:
    from twisted.application import service, internet
    # TODO 環境変数
    application = service.Application("auth-basic")
    internet.TCPServer(int(config_data['server.port']), Application(),
            interface=config_data['server.interface']).setServiceParent(application)

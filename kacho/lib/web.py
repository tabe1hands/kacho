# coding: utf-8
# This file is part of Kacho
#
# Copyright (C) 2011 Junichi Shinohara <tabe1hands@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

import base64
import functools
import gettext

from mako.template import Template
from mako.lookup import TemplateLookup
from mako import exceptions
import cyclone.web

import kacho

def basic_auth(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            auth_type, auth_data = self.request.headers["Authorization"].split()
            assert auth_type == "Basic"
            usr, pwd = base64.b64decode(auth_data).split(":", 1)
            assert usr == "user@domain"
            assert pwd == "password"
        except:
            raise cyclone.web.HTTPAuthenticationRequired
        else:
            return method(self, *args, **kwargs)
    return wrapper

def translation(languages, domain='messages', localedir='locale'):
    """
    gettext.translationのラッパー
    """
    localedir = '/'.join([kacho.dirname, localedir])
    return gettext.translation(domain, localedir, tuple(languages))

class Rest(cyclone.web.RequestHandler):
    def _template_render(self, path, **kwargs):
        """
        テンプレートを使った画面のレンダリング
        """
        directories = [kacho.dirname, 'templates']
        directories.append('default')

        tl = TemplateLookup(
                directories='/'.join(directories),
                input_encoding='utf-8',
                output_encoding='utf-8',
                default_filters=['decode.utf8'],
                encoding_errors='replace')
        
        import pdb;pdb.set_trace()
        try:
            t = tl.get_template(path)
        except exceptions.TopLevelLookupException, tlle:
            raise cyclone.web.HTTPError(404)
            
        return t.render(**kwargs)

    def get(self):
        try:
            # 国際化
            self._ = translation(languages=['ja_JP']).ugettext

            # URLパース
            # TODO
            self.format = 'html'

            # レスポンス
            response = self._get()

            if not response:
                response = {}
                #TODO 値がないことをロギングする

            # レンダリング
            template_dir = kacho.dirname
            template_theme = 'default' #TODO
            template_file = self.__class__.__name__.lower()
            template_format = self.format
            if template_file == 'static':
                static_file_path = '%s/%s.%s' % (
                        template_dir, template_file, 
                        template_format)
                _f = open(static_file_path, "r")
                try:
                    result = _f.read()
                finally:
                    _f.close()
            else:
                template_path = '%s/template/%s/%s/%s.%s' % (
                        template_dir, template_theme, 
                        template_file, template_file, template_format)
                result = self._template_render(
                        template_path, _=self._, **response)
            self.finish(result)
        except cyclone.web.HTTPError, e:
            #TODO logging
            raise
        except:
            #TODO logging
            raise

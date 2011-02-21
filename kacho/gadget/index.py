# This file is part of Kacho
#
# Copyright (C) 2011 Junichi Shinohara <tabe1hands@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from kacho.lib.web import Rest, basic_auth

class Index(Rest):

    @basic_auth
    def _get(self):
        return {'title': 'Index'}

urls = [(r"/index.html", Index)]

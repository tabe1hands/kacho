#!/usr/bin/env python
#
# This file is part of Kacho
#
# Copyright (C) 2011 Junichi Shinohara <tabe1hands@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

from distutils.core import setup

from kacho import __version__, __release__, __app__

setuptools.setup(
    name=__app__,
    version="%s.%s" % (__version__, __release__),
    packages=["kacho"],
#    install_requires=["cyclone"],
    author="Junichi Shinohara",
    author_email="tabe1hands@gmail.com",
    url="http://github.com/fiorix/cyclone/",
    license="http://www.gnu.org/copyleft/lesser.html",
    description="Something.",
    long_description="""Something.""",
    keywords="python",
    classifiers=[
#        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Mako',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Natural Language :: Japanese',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Systems Administration'],
    ]
)

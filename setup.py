# (C) Copyright 2003 Nuxeo SARL <http://nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# $Id$

from distutils.core import setup
import py2exe
import glob

opts = {
    "py2exe": {
        "includes": "pango,atk,gobject,encodings,encodings.*",
        }
    }

setup(
    windows = [
        {"script": "cpsctl.py",
        "icon_resources": [(1, "cpsctl.ico")]
        }
    ],
    options=opts,
    data_files=[("locales", glob.glob("locales/*.*")),
                ("", glob.glob("lib/libpng12.dll")),
                ("", glob.glob("cps.conf.in")),
                ("", glob.glob("cpsctl.ico")),
                ("images", glob.glob("images/*.*")),
                ("glade", glob.glob("glade/cpsctl.glade"))
    ],
)

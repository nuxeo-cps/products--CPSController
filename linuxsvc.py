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

import os
import sys
import Zope
from Zope.Startup.zopectl import ZopeCtlOptions, ZopeCmd

class ServiceControl:
    def __init__(self, instance_home, software_home):
        self.instance_home = instance_home
        self.software_home = software_home

    def _getCmd(self):
        return os.path.join(self.instance_home, 'bin/zopectl')

    def start(self):
        os.system('%s start' % self._getCmd())

    def stop(self):
        os.system('%s stop' % self._getCmd())

    def isRunning(self):
        stdout = sys.stdout
        stderr = sys.stderr
        class Shutup:
            def write(*args):
                pass

        argv_orig = sys.argv[:]
        cmd_opts = ['zopectl', '-C', os.path.join(self.instance_home,
                                                  'etc/zope.conf')]
        #sys.argv.extend(cmd_opts)
        sys.argv = cmd_opts

        options = ZopeCtlOptions()
        options.realize(None)
        c = ZopeCmd(options)
        sys.argv = argv_orig
        try:
            #sys.stdout = Shutup()
            #sys.stderr = Shutup()
            c.get_status()
        finally:
            #sys.stdout = stdout
            #sys.stderr = stderr
            pass
        if c.zd_up:
            return 1
        else:
            return 0

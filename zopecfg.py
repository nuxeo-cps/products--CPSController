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

import binascii
import sha
import os
import sys
from config import *
import platform
from time import sleep
from iszope import examine
from events import UPDATE_EVT
from threading import Thread
import gtk

INSTANCE_HOME = os.environ.get('INSTANCE_HOME')
SOFTWARE_HOME = os.environ.get('SOFTWARE_HOME')

if platform.platform().lower().find('linux') < 0:
    from winsvc import ServiceControl
else:
    sys.path.insert(0, SOFTWARE_HOME)
    from linuxsvc import ServiceControl

try:
    import ZConfig
except ImportError:
    sys.path.insert(0, SOFTWARE_HOME)
    try:
        import ZConfig
    except ImportError:
        print "Import of ZConfig failed!"
        raise

FILES = {'Emergency User' :
         os.path.join(INSTANCE_HOME, 'access'),
         'CPS Config' :
         os.path.join(INSTANCE_HOME,  'etc', 'cps.conf'),
         'Zope Config' :
         os.path.join(INSTANCE_HOME,  'etc', 'zope.conf'),
         'Zope Schema' :
         os.path.join(SOFTWARE_HOME,  'Zope', 'Startup', 'zopeschema.xml'),
         }

PORTS = [
    "CPS_WEBSERVER_PORT",
    "ZOPE_MANAGEZODB_PORT",
    "CPS_FTPSERVER_PORT",
    "CPS_DAVSERVER_PORT"
    ]


class Zope:

    _instance = None

    def __init__(self):
        self.svc = ServiceControl(INSTANCE_HOME, SOFTWARE_HOME)
        self.cps_cfg = {}
        self.zope_cfg = None

        self.loadConfig()


    def getFilePath(self, key):
        return FILES[key]

    def getInstanceHome(self):
        return INSTANCE_HOME

    def createEmergencyUser(self, username, pw, pw_confirm):
        if not username:
            raise ValueError, NOUSERNAME_MSG
        if not pw:
            raise ValueError, NOPASSWD_MSG
        if pw != pw_confirm:
            raise ValueError, PASSWORDS_DONOT_MATCH_MSG

        ac_file = open(self.getFilePath('Emergency User'), 'w')
        passwd =  '{SHA}' + binascii.b2a_base64(sha.new(pw).digest())[:-1]
        ac_file.write('%s:%s\n' % (username, passwd))
        ac_file.close()


    def removeEmergencyUser(self):
        os.unlink(self.getFilePath('Emergency User'))


    def hasEmergencyUser(self):
        return os.path.exists(self.getFilePath('Emergency User'))


    def getPort(self, name):
        if name not in PORTS:
            raise ValueError, "Unknown port"
        return self.cps_cfg[name]


    def setPort(self, name, val):
        if name not in PORTS:
            raise ValueError, "Unknown port"
        self.cps_cfg[name] = int(val)
        self.saveConfig()

    def saveConfig(self):
        lines = open(self.getFilePath('CPS Config'), 'r').readlines()
        newlines = []

        for line in lines:
            line = line.strip()
            if line.startswith('%define'):
                define, name, port = line.split(' ')
                if name in PORTS:
                    num = str(self.getPort(name))
                    line = ' '.join((define, name, num))
            newlines.append(line)
        open(self.getFilePath('CPS Config'), 'w').write('\n'.join(newlines))


    def loadConfig(self):
        # FIXME: this makes py2exe to build executable which can't find
        # sax reader :( so we comment next lines
        #schema = ZConfig.loadSchema(self.getFilePath('Zope Schema'))
        #zconfig, handler = ZConfig.loadConfig(schema,
        #                                      self.getFilePath('Zope Config'))
        #self.zope_cfg = zconfig

        lines = open(self.getFilePath('CPS Config'), 'r').readlines()
        for line in lines:
            if line.startswith('%define'):
                define, name, port = line.strip().split(' ')
                self.cps_cfg[name] = port

    def getUrl(self):
        return "http://localhost:%s" % self.getPort('CPS_WEBSERVER_PORT')

    def getManageUrl(self):
        url = "http://localhost:%s/manage"
        return  url % self.getPort('ZOPE_MANAGEZODB_PORT')

    # Service control
    def start(self):
        self.svc.start()

    def stop(self):
        self.svc.stop()

    def getStatus(self):
        if self.svc.isRunning():
            # double check in separate thread
            #self.testUp()
            return 1
        else:
            return 0

    def testUp(self, tries=3, timeout=1):
        url = self.getUrl()
        th = ExamineThread(url, tries, timeout)
        th.start()

# simple Singleton
def Singleton(klass):
    if not klass._instance:
        klass._instance = klass()
    return klass._instance


def getZope():
    return Singleton(Zope)



class ExamineThread(Thread):

    def __init__(self, url, tries=3, timeout=5):
        if not url:
            raise ValueError, "No URL to examine"
        self.url = url
        self.tries = tries
        self.timeout = timeout
        Thread.__init__(self)

    def run(self):
        some_res = 0
        while self.tries:
            try:
                res = examine(self.url)
                if res:
                    gtk.threads_enter()
                    UPDATE_EVT().set_property('status', 1)
                    gtk.threads_leave()
                    some_res = 1
                    break
            except IOError:
                pass
            sleep(self.timeout)
            self.tries -= 1
        if not some_res:
            gtk.threads_enter()
            UPDATE_EVT().set_property('status', 0)
            gtk.threads_leave()



if __name__ == '__main__':
    z = getZope()
    #print z.getPort('CPS_WEBSERVER_PORT')
    #print z.setPort('CPS_WEBSERVER_PORT', 8080)
    #print z.getPort('CPS_WEBSERVER_PORT')

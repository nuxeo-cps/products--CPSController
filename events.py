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

import gobject

class UpdateEvt(gobject.GObject):
    __gproperties__ = {
        'status' : (gobject.TYPE_INT,
                    "status",
                    "status",
                    0,
                    200,
                    0,
                    gobject.PARAM_READWRITE),
        }

    __gsignals__ = {
        'cps-update' : (gobject.SIGNAL_RUN_LAST,
                        gobject.TYPE_NONE,
                        (gobject.TYPE_INT, ))
        }

    _instance = None

    def __init__(self):
        gobject.GObject.__init__(self)
        self.status = 0

    def do_get_property(self, property):
        if property.name == 'status':
            return self.status
        else:
            raise AttributeEror, 'unknown property %s' % property.name

    def do_set_property(self, property, value):
        if property.name == 'status':
            self.status = value
            self.emit('cps-update', self.get_property('status'))
        else:
            raise AttributeEror, 'unknown property %s' % property.name

    #def do_cps_update(self, my_status):
    #    print "my_status = ", my_status

gobject.type_register(UpdateEvt)

# simple Singleton
def Singleton(klass):
    if not klass._instance:
        klass._instance = klass()
    return klass._instance


def UPDATE_EVT():
    return Singleton(UpdateEvt)

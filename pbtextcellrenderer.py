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

import pygtk
import gtk
import gobject

PAD = 3

class PixbufTextCellRenderer(gtk.GenericCellRenderer):

    __gproperties__ = {
        "pixbuf": (gobject.TYPE_PYOBJECT, "Pixbuf",
                    "Pixbuf image", gobject.PARAM_READWRITE),
        "text": (gobject.TYPE_STRING, "Text", "Text string", None,
                 gobject.PARAM_READWRITE),
    }

    def __init__(self):
        self.__gobject_init__()
        self.prend = gtk.CellRendererPixbuf()
        self.trend = gtk.CellRendererText()
        self.percent = 0

    def do_set_property(self, pspec, value):
        setattr(self, pspec.name, value)

    def do_get_property(self, pspec):
        return getattr(self, pspec.name)

    def update_properties(self):
        self.trend.set_property('text', self.get_property('text'))
        self.prend.set_property('pixbuf', self.get_property('pixbuf'))
        return

    def on_render(self, window, widget, background_area,
                  cell_area, expose_area, flags):
        self.update_properties()
        ypad = self.get_property('ypad')
        px, py, pw, ph = self.prend.get_size(widget, cell_area)
        px += cell_area.x
        prect = (px, cell_area.y, pw, ph)
        tx, ty, tw, th = self.trend.get_size(widget, cell_area)
        tx = cell_area.x + (cell_area.width - tw) / 2
        ty = cell_area.y + ph + PAD
        trect = (tx, ty, tw, th)
        self.prend.render(window, widget, background_area, prect,
                          expose_area, flags)
        self.trend.render(window, widget, background_area, trect,
                          expose_area, flags)
        return

    def on_get_size(self, widget, cell_area):
        self.update_properties()
        xpad = self.get_property("xpad")
        ypad = self.get_property("ypad")
        xoff, yoff, width, height = self.trend.get_size(widget, cell_area)
        pxoff, pyoff, pwidth, pheight = self.prend.get_size(widget, cell_area)
        height += pheight + PAD + ypad
        width = max(width, pwidth) + xpad * 2
        return xoff, yoff, width, height

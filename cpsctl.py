#!/usr/bin/env python
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

import sys
import os
import pygtk
#this is needed for py2exe
if sys.platform == 'win32':
    #win32 platform, add the "lib" folder to the system path
    os.environ['PATH'] += ";lib;"
else:
    #not win32, ensure version 2.0 of pygtk is imported
    pygtk.require('2.0')
import gtk
import gtk.glade
import gobject
import os
import os.path
import locale, gettext
import webbrowser
from config import *
from pbtextcellrenderer import PixbufTextCellRenderer
from events import UPDATE_EVT

def fatal_error(msg):
    dialog = gtk.MessageDialog(None,
                               gtk.DIALOG_MODAL |
                               gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_INFO,
                               gtk.BUTTONS_OK,
                               str(msg))
    dialog.run()
    dialog.destroy()
    sys.exit(1)

if len(sys.argv) < 3 or not (os.path.isdir(sys.argv[1])
                             and os.path.isdir(sys.argv[2])):
    fatal_error(USAGE_MSG)
else:
    os.environ['INSTANCE_HOME'] = sys.argv[1]
    os.environ['SOFTWARE_HOME'] = sys.argv[2]

# uses above environment variables, so we need put this import here
from zopecfg import getZope


IMAGES_DIR = 'images'

PAGES = {'Ports': {'page_num': 0, 'image': 'ports.png'},
         'Status': {'page_num': 1, 'image': 'status.png'},
         'Emergency User': {'page_num': 2, 'image': 'emg_user.png'},
         'About': {'page_num': 3, 'image': 'about.png'},
         }

NUXEO_IMG = os.path.join(IMAGES_DIR, 'nuxeo.png')
CPS_IMG = os.path.join(IMAGES_DIR, 'cps.png')

gobject.type_register(PixbufTextCellRenderer)


class AppGUI:
    def on_cps_update(self, obj, status=0):
        if obj.get_property('status'):
            self._onStartStatusControls()
        else:
            self._onStopStatusControls()

    def __init__(self, argv):
        gladefile = os.path.join('glade', 'cpsctl.glade')

        gtk.glade.bindtextdomain(APP, DIR)
        gtk.glade.textdomain(APP)

        self.glade = gtk.glade.XML(gladefile, None, gettext.textdomain())
        #self.glade = gtk.glade.XML(gladefile)

        self._connectSignals()
        self._initWidgets()

        self._initTreeView()

        self._setPortsControls()

        self.initialize()
        self._initAbout()

        UPDATE_EVT().connect('cps-update', self.on_cps_update)

        self._setStatusControls('unknown')
        getZope().testUp()

    def _initAbout(self):
        img = gtk.Image()
        img.set_from_file(NUXEO_IMG)
        self.vbox_about.pack_start(img)
        img.show()
        img = gtk.Image()
        img.set_from_file(CPS_IMG)
        self.vbox_about.pack_start(img)
        img.show()

        self.about_cps_label.set_label(ABOUT_MSG)


    def _connectSignals(self):
        dic = {
            'on_closebutton_clicked':
                lambda win: gtk.main_quit(),
            'on_window_destroy':
                lambda win: gtk.main_quit(),
            'on_preftree_cursor_changed':
                self.on_preftree_cursor_changed,
            'on_emguser_button_clicked':
                self.on_emguser_button_clicked,
            'on_cpsport_focus_out_event':
                self.on_cpsport_focus_out_event,
            'on_zopeport_focus_out_event':
                self.on_zopeport_focus_out_event,
            'on_ftpport_focus_out_event':
                self.on_ftpport_focus_out_event,
            'on_davport_focus_out_event':
                self.on_davport_focus_out_event,
            'on_status_button_clicked':
                self.on_status_button_clicked,
            'on_viewcps_clicked':
                self.on_viewcps_clicked,
            'on_zmi_clicked':
                self.on_zmi_clicked,
            }

        self.glade.signal_autoconnect(dic)

    def _initWidgets(self):
        self.window = self.glade.get_widget('window')
        self.notebook = self.glade.get_widget('notebook')
        self.emguser_button = self.glade.get_widget('emguser_button')
        self.emguser_label = self.glade.get_widget('emguser_label')
        self.username_entry = self.glade.get_widget('username_entry')
        self.pw_entry = self.glade.get_widget('pw_entry')
        self.pwconfirm_entry = self.glade.get_widget('pwconfirm_entry')
        self.username_label = self.glade.get_widget('username_label')
        self.pw_label = self.glade.get_widget('pw_label')
        self.pwconfirm_label = self.glade.get_widget('pwconfirm_label')
        self.preftree = self.glade.get_widget('preftree')

        self.cps_port_sb = self.glade.get_widget('cps_port_spinbutton')
        self.zope_port_sb = self.glade.get_widget('zope_port_spinbutton')
        self.ftp_port_sb = self.glade.get_widget('ftp_port_spinbutton')
        self.webdav_port_sb = self.glade.get_widget('webdav_port_spinbutton')

        self.emguser_help_lbl = self.glade.get_widget('emguser_help_label')
        self.emguser_exist_lbl = self.glade.get_widget('emguser_exist_label')

        self.st_button = self.glade.get_widget('status_button')
        self.st_button_label = self.glade.get_widget('status_button_label')
        self.st_label = self.glade.get_widget('status_label')
        self.st_viewcps_btn = self.glade.get_widget('status_viewcps_button')
        self.st_zmi_btn = self.glade.get_widget('status_zmi_button')

        self.vbox_about = self.glade.get_widget('vbox_about')
        self.about_cps_label = self.glade.get_widget('about_cps_label')

    def _initTreeView(self):
        ls = gtk.ListStore(str, object, str)
        self.preftree.set_model(ls)

        pbtcell = PixbufTextCellRenderer()
        pbtcell.set_property('xpad', 5)
        pbtcell.set_property('ypad', 3)
        tvc = gtk.TreeViewColumn('', pbtcell, text=0, pixbuf=1)
        self.preftree.append_column(tvc)

        img_path = os.path.join(IMAGES_DIR, PAGES['Ports']['image'])
        ls.append([PORTS_TXT,
               gtk.gdk.pixbuf_new_from_file(img_path), 'Ports'])

        img_path = os.path.join(IMAGES_DIR, PAGES['Status']['image'])
        ls.append([STATUS_TXT,
               gtk.gdk.pixbuf_new_from_file(img_path), 'Status'])

        img_path = os.path.join(IMAGES_DIR, PAGES['Emergency User']['image'])
        ls.append([EMERGENCY_USER_TXT,
               gtk.gdk.pixbuf_new_from_file(img_path), 'Emergency User'])

        img_path = os.path.join(IMAGES_DIR, PAGES['About']['image'])
        ls.append([ABOUT_TXT,
               gtk.gdk.pixbuf_new_from_file(img_path), 'About'])


    def initialize(self):
        num = PAGES['Status']['page_num']
        self.notebook.set_current_page(num)
        self.preftree.get_selection().select_path(num)
        self.pw_entry.set_visibility(gtk.FALSE)
        self.pwconfirm_entry.set_visibility(gtk.FALSE)

        self._setEmergencygUserControls()


    def on_cpsport_focus_out_event(self, spinbutton, event, data=None):
        spinbutton.update()
        getZope().setPort('CPS_WEBSERVER_PORT', spinbutton.get_value_as_int())
        return gtk.FALSE

    def on_zopeport_focus_out_event(self, spinbutton, event, data=None):
        spinbutton.update()
        getZope().setPort('ZOPE_MANAGEZODB_PORT',
                          spinbutton.get_value_as_int())
        return gtk.FALSE

    def on_ftpport_focus_out_event(self, spinbutton, event, data=None):
        spinbutton.update()
        getZope().setPort('CPS_FTPSERVER_PORT', spinbutton.get_value_as_int())
        return gtk.FALSE

    def on_davport_focus_out_event(self, spinbutton, event, data=None):
        spinbutton.update()
        getZope().setPort('CPS_DAVSERVER_PORT', spinbutton.get_value_as_int())
        return gtk.FALSE

    def on_preftree_cursor_changed(self, treeview):
        tselection = treeview.get_selection()
        model, iter = tselection.get_selected()
        val = model.get_value(iter, 2)
        self.notebook.set_current_page(PAGES[val]['page_num'])


    def on_emguser_button_clicked(self, widget, data=None):
        z = getZope()
        if z.hasEmergencyUser():
            z.removeEmergencyUser()
        else:
            username = self.username_entry.get_text()
            pw = self.pw_entry.get_text()
            pw_confirm = self.pwconfirm_entry.get_text()
            try:
                z.createEmergencyUser(username, pw, pw_confirm)
            except ValueError, msg:
                self.showMsgDialog(msg)
            except Exception, msg:
                self.showMsgDialog(msg)

        self._setEmergencygUserControls()

    def on_viewcps_clicked(self, widget, data=None):
        webbrowser.open(getZope().getUrl())

    def on_zmi_clicked(self, widget, data=None):
        webbrowser.open(getZope().getManageUrl())

    def on_status_button_clicked(self, widget, data=None):
        zope = getZope()
        if zope.getStatus():
            self._setStatusControls('stop')
            zope.stop()
            zope.testUp()
        else:
            self._setStatusControls('start')
            zope.start()
            zope.testUp()

    def _setStatusControls(self, action):
        if action == 'stop':
            self.st_button_label.set_label('Stopping')
            self.st_label.set_label('CPS is stopping...')
        elif action == 'start':
            self.st_button_label.set_label('Starting')
            self.st_label.set_label('CPS is starting...')
        elif action == 'unknown':
            self.st_button_label.set_label('Unknown')
            self.st_label.set_label('Determining CPS status...')
        self.st_button.set_sensitive(gtk.FALSE)
        self.st_viewcps_btn.set_sensitive(gtk.FALSE)
        self.st_zmi_btn.set_sensitive(gtk.FALSE)

    def _onStartStatusControls(self):
        self.st_button_label.set_label('Stop')
        self.st_button.set_sensitive(gtk.TRUE)
        self.st_label.set_label('CPS is running.')
        self.st_viewcps_btn.set_sensitive(gtk.TRUE)
        self.st_zmi_btn.set_sensitive(gtk.TRUE)


    def _onStopStatusControls(self):
        self.st_button_label.set_label('Start')
        self.st_button.set_sensitive(gtk.TRUE)
        self.st_label.set_label('CPS is not running.')
        self.st_viewcps_btn.set_sensitive(gtk.FALSE)
        self.st_zmi_btn.set_sensitive(gtk.FALSE)

    def _setPortsControls(self):
        z = getZope()
        self.cps_port_sb.set_value(float(z.getPort('CPS_WEBSERVER_PORT')))
        self.zope_port_sb.set_value(float(z.getPort('ZOPE_MANAGEZODB_PORT')))
        self.ftp_port_sb.set_value(float(z.getPort('CPS_FTPSERVER_PORT')))
        self.webdav_port_sb.set_value(float(z.getPort('CPS_DAVSERVER_PORT')))


    def _setEmergencygUserControls(self):
        _s = ('username_label', 'pw_label', 'pwconfirm_label',
              'username_entry', 'pw_entry', 'pwconfirm_entry')
        _v = ('username_entry', 'pw_entry', 'pwconfirm_entry')

        if getZope().hasEmergencyUser():
            for el in _s:
                getattr(self, el).set_sensitive(gtk.FALSE)
            for el in _v:
                getattr(self, el).set_text('')
            self.emguser_label.set_label(REMOVE_EMERGENCY_USER_MSG)
            self.emguser_exist_lbl.set_label(EMERGENCY_USER_EXIST)
        else:
            for el in _s:
                getattr(self, el).set_sensitive(gtk.TRUE)
            for el in _v:
                getattr(self, el).set_text('')
            self.emguser_label.set_label(CREATE_EMERGENCY_USER_MSG)
            self.emguser_exist_lbl.set_label(EMERGENCY_USER_NOT_EXIST)



    def fatalError(self, msg):
        self.showMsgDialog(msg, exit=1)


    def showMsgDialog(self, msg, type=gtk.MESSAGE_INFO, exit=0):
        window = getattr(self, 'window', None)
        dialog = gtk.MessageDialog(window,
                                   gtk.DIALOG_MODAL |
                                   gtk.DIALOG_DESTROY_WITH_PARENT,
                                   type,
                                   gtk.BUTTONS_OK,
                                   str(msg))
        dialog.run()
        dialog.destroy()
        if exit:
            sys.exit(1)


if __name__ == "__main__":
    gtk.threads_init()
    app = AppGUI(sys.argv)
    gtk.threads_enter()
    gtk.main()
    gtk.threads_leave()

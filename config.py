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

import locale, gettext

APP = 'cpsctl'
DIR = 'locales'
gettext.textdomain(APP)
gettext.install(APP, DIR, unicode=1)

USAGE_MSG = _("Usage: cpsctl INSTANCE_HOME SOFTWARE_HOME")
CREATE_EMERGENCY_USER_MSG = _('Create User')
REMOVE_EMERGENCY_USER_MSG = _('Remove User')
PASSWORDS_DONOT_MATCH_MSG = _('Passwords do not match')
NOUSERNAME_MSG = _('No username')
NOPASSWD_MSG = _('No password')
ABOUT_MSG = _('Nuxeo CPS is a collaborative web content management solution for Zope.')

PORTS_TXT = _('Ports')
STATUS_TXT = _('Status')
EMERGENCY_USER_TXT = _('Emergency\nUser')
ABOUT_TXT = _('About')

EMERGENCY_USER_EXIST = _('An emergency user currently exists.')
EMERGENCY_USER_NOT_EXIST = _('There is no emergency user configured.')

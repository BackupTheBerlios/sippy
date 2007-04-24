# Copyright (c) 2003-2005 Maxim Sobolev. All rights reserved.
# Copyright (c) 2006-2007 Sippy Software, Inc. All rights reserved.
#
# This file is part of SIPPY, a free RFC3261 SIP stack and B2BUA.
#
# SIPPY is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# For a license to use the ser software under conditions
# other than those described here, or to purchase support for this
# software, please contact Sippy Software, Inc. by e-mail at the
# following addresses: sales@sippysoft.com.
#
# SIPPY is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA.

from socket import gethostbyname, gethostname

class SipConf:
    default_port = 5060

    try: my_address
    except: my_address = gethostbyname(gethostname())

    try: my_port
    except: my_port = default_port

    try: my_uaname
    except: my_uaname = 'Sippy'

    try: my_iaddress
    except: my_iaddress = '192.168.1.7'

    try: my_iport
    except: my_iport = default_port

    try: my_laddress
    except: my_laddress = '127.0.0.1'

    try: my_lport
    except: my_lport = default_port

    try: allow_formats
    except: allow_formats = None

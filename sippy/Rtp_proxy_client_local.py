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
# For a license to use the SIPPY software under conditions
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
#
# $Id: Rtp_proxy_client_local.py,v 1.5 2009/02/25 06:56:52 sobomax Exp $

from Timeout import Timeout
from errno import EINTR

import socket

class Rtp_proxy_client_local(object):
    address = None
    online = False
    proxy_address = None

    def __init__(self, global_config, address = '/var/run/rtpproxy.sock'):
        self.address = address
        self.proxy_address = global_config['sip_address']
        self.heartbeat()

    def send_command(self, command, result_callback = None, *callback_parameters):
        data = self.send_raw(command)
        if result_callback != None:
            Timeout(self.process_reply, 0, 1, (result_callback, data, callback_parameters))

    def send_raw(self, command):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(self.address)
        while True:
            try:
                s.send(command)
                break
            except socket.error, why:
                if why[0] == EINTR:
                    continue
                raise why
        while True:
            try:
                rval = s.recv(1024).strip()
                break
            except socket.error, why:
                if why[0] == EINTR:
                    continue
                raise why
        return rval

    def process_reply(self, args):
        args[0](args[1], *args[2])

    def heartbeat(self):
        try:
            version = self.send_raw('V')
            if version == '20040107':
                self.online = True
            else:
                self.online = False
        except:
            self.online = False
        Timeout(self.heartbeat, 60)

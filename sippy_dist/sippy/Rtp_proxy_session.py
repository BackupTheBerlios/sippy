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
#
# $Id: Rtp_proxy_session.py,v 1.1 2007/09/18 06:49:11 sobomax Exp $

from md5 import md5
from random import random
from time import time

class Rtp_proxy_session:
    rtp_proxy_client = None
    call_id = None
    from_tag = None
    to_tag = None
    local_address = None
    caller_session_exists = False
    caller_codecs = None
    callee_session_exists = False
    callee_codecs = None
    max_index = -1

    def __init__(self, global_config, call_id = None, from_tag = None, to_tag = None):
        if global_config.has_key('rtp_proxy_clients'):
            rtp_proxy_clients = filter(lambda x: x.online, global_config['rtp_proxy_clients'])
            n = len(rtp_proxy_clients)
            if n == 0:
                raise Exception('No online RTP proxy client has been found')
            self.rtp_proxy_client = rtp_proxy_clients[int(random() * n)]
        else:
            self.rtp_proxy_client = global_config['rtp_proxy_client']
            if not self.rtp_proxy_client.online:
                raise Exception('No online RTP proxy client has been found')
        self.local_address = global_config['sip_address']
        if call_id != None:
            self.call_id = call_id
        else:
            self.call_id = md5(str(random()) + str(time())).hexdigest()
        if from_tag != None:
            self.from_tag = from_tag
        else:
            self.from_tag = md5(str(random()) + str(time())).hexdigest()
        if to_tag != None:
            self.to_tag = to_tag
        else:
            self.to_tag = md5(str(random()) + str(time())).hexdigest()

    def version(self, result_callback):
        self.rtp_proxy_client.send_command('V', self.version_result, result_callback)

    def version_result(self, result, result_callback):
        result_callback(result)

    def play_caller(self, prompt_name, times = 1, result_callback = None, index = 0):
        if not self.caller_session_exists:
            return
        command = 'P%d %s %s %s %s %s' % (times, '%s-%d' % (self.call_id, index), prompt_name, self.caller_codecs, self.from_tag, self.to_tag)
        self.rtp_proxy_client.send_command(command, self.command_result, result_callback)

    def play_callee(self, prompt_name, times = 1, result_callback = None, index = 0):
        if not self.callee_session_exists:
            return
        command = 'P%d %s %s %s %s %s' % (times, '%s-%d' % (self.call_id, index), prompt_name, self.caller_codecs, self.to_tag, self.from_tag)
        self.rtp_proxy_client.send_command(command, self.command_result, result_callback)

    def stop_play_caller(self, result_callback = None, index = 0):
        if not self.caller_session_exists:
            return
        command = 'S %s %s %s' % ('%s-%d' % (self.call_id, index), self.from_tag, self.to_tag)
        self.rtp_proxy_client.send_command(command, self.command_result, result_callback)

    def stop_play_callee(self, result_callback = None, index = 0):
        if not self.caller_session_exists:
            return
        command = 'S %s %s %s' % ('%s-%d' % (self.call_id, index), self.to_tag, self.from_tag)
        self.rtp_proxy_client.send_command(command, self.command_result, result_callback)

    def copy_caller(self, remote_ip, remote_port, result_callback = None, index = 0):
        if not self.caller_session_exists:
            self.update_caller('0.0.0.0', 0, self._copy_caller, None, index, remote_ip, remote_port, result_callback, index)
            return
        self._copy_caller(None, remote_ip, remote_port, result_callback, index)

    def _copy_caller(self, result, remote_ip, remote_port, result_callback = None, index = 0):
        command = 'C %s udp:%s:%d %s %s' % ('%s-%d' % (self.call_id, index), remote_ip, remote_port, self.from_tag, self.to_tag)
        self.rtp_proxy_client.send_command(command, self.command_result, result_callback)

    def copy_callee(self, remote_ip, remote_port, result_callback = None, index = 0):
        if not self.callee_session_exists:
            self.update_callee('0.0.0.0', 0, self._copy_callee, None, index, remote_ip, remote_port, result_callback, index)
            return
        self._copy_callee(None, remote_ip, remote_port, result_callback, index)

    def _copy_callee(self, result, remote_ip, remote_port, result_callback = None, index = 0):
        command = 'C %s udp:%s:%d %s %s' % ('%s-%d' % (self.call_id, index), remote_ip, remote_port, self.to_tag, self.from_tag)
        self.rtp_proxy_client.send_command(command, self.command_result, result_callback)

    def command_result(self, result, result_callback):
        if result_callback != None:
            result_callback(result)

    def update_caller(self, remote_ip, remote_port, result_callback, options = None, index = 0, *callback_parameters):
        command = 'U'
        self.max_index = max(self.max_index, index)
        if options != None:
            command += options
        command += ' %s %s %d %s %s' % ('%s-%d' % (self.call_id, index), remote_ip, remote_port, self.from_tag, self.to_tag)
        self.rtp_proxy_client.send_command(command, self.update_result, (result_callback, 'caller', callback_parameters))

    def update_callee(self, remote_ip, remote_port, result_callback, options = None, index = 0, *callback_parameters):
        command = 'U'
        self.max_index = max(self.max_index, index)
        if options != None:
            command += options
        command += ' %s %s %d %s %s' % ('%s-%d' % (self.call_id, index), remote_ip, remote_port, self.to_tag, self.from_tag)
        self.rtp_proxy_client.send_command(command, self.update_result, (result_callback, 'callee', callback_parameters))

    def update_result(self, result, args):
        result_callback, face, callback_parameters = args
        if face == 'caller':
            self.caller_session_exists = True
        else:
            self.callee_session_exists = True
        if result == None:
            result_callback(None, *callback_parameters)
            return
        t1 = result.split()
        rtpproxy_port = int(t1[0])
        if rtpproxy_port == 0:
            result_callback(None, *callback_parameters)
        if len(t1) > 1:
            rtpproxy_address = t1[1]
        else:
            rtpproxy_address = self.local_address
        result_callback((rtpproxy_address, rtpproxy_port), *callback_parameters)

    def delete(self):
        while self.max_index >= 0:
            command = 'D %s %s %s' % ('%s-%d' % (self.call_id, self.max_index), self.from_tag, self.to_tag)
            self.rtp_proxy_client.send_command(command)
            self.max_index -= 1

    def on_caller_sdp_change(self, sdp_body, result_callback):
        self.on_xxx_sdp_change(self.update_caller, sdp_body, result_callback)

    def on_callee_sdp_change(self, sdp_body, result_callback):
        self.on_xxx_sdp_change(self.update_callee, sdp_body, result_callback)

    def on_xxx_sdp_change(self, update_xxx, sdp_body, result_callback):
        sects = []
        for i in range(1, len(sdp_body.content.sections)):
            sect = sdp_body.content.sections[i]
            if sect.getF('m').body.transport.lower() not in ('udp', 'udptl', 'rtp/avp'):
                continue
            sects.append(sect)
        if len(sects) == 0:
            return
        if update_xxx == self.update_caller:
            self.caller_codecs = reduce(lambda x, y: str(x) + ',' + str(y), sects[0].getF('m').body.formats)
        else:
            self.callee_codecs = reduce(lambda x, y: str(x) + ',' + str(y), sects[0].getF('m').body.formats)
        for sect in sects:
            update_xxx(sect.getF('c').body.addr, sect.getF('m').body.port, self.xxx_sdp_change_finish, None, \
              sects.index(sect), sdp_body, sect, sects, result_callback)
        return

    def xxx_sdp_change_finish(self, address_port, sdp_body, sect, sects, result_callback):
        sect.needs_update = False
        if address_port != None:
            sect.getF('c').body.addr = address_port[0]
            sect.getF('m').body.port = address_port[1]
        if len(filter(lambda x: x.needs_update, sects)) == 0:
            sdp_body.needs_update = False
            result_callback(sdp_body)

    def __del__(self):
        self.delete()
        self.rtp_proxy_client = None
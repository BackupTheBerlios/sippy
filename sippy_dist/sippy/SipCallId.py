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
# $Id: SipCallId.py,v 1.3 2007/09/18 04:55:37 sobomax Exp $

from random import random
from md5 import md5
from time import time
from SipConf import SipConf

class SipCallId:
    hf_names = ('call-id', 'i')
    body = None

    def __init__(self, body = None):
        if body != None:
            self.body = body
        else:
            self.body = md5(str((random() * 1000000000L) + time())).hexdigest() + '@' + SipConf.my_address

    def __str__(self):
        return self.body

    def __add__(self, other):
        return SipCallId(self.body + str(other))

    def getCopy(self):
        return SipCallId(self.body)

    def genCallId(self):
        self.body = md5(str((random() * 1000000000L) + time())).hexdigest() + '@' + SipConf.my_address

    def getCanName(self, name):
        return 'Call-ID'

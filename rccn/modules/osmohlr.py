############################################################################
#
# RCCN (Rhizomatica Community Cellular Network)
#
# Copyright (C) 2020 matt9j <matt9j@cs.washington.edu>
#
# RCCN is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RCCN is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero Public License for more details.
#
# You should have received a copy of the GNU Affero Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################

""" This module contains adaptors to interface with the osmohlr vty and db
"""

# Python3/2 compatibility
# TODO: Remove once python2 support no longer needed.
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sqlite3


class OsmoHlrError(Exception):
    pass


class OsmoHlrDb(object):

    def __init__(self, hlr_db_path):
        self.hlr_db_path = hlr_db_path

    def get_msisdn_from_imsi(self, imsi):
        # TODO(matt9j) Check for duplication
        try:
            sq_hlr = sqlite3.connect(self.hlr_db_path)
            sq_hlr_cursor = sq_hlr.cursor()
            sq_hlr_cursor.execute(
                "SELECT msisdn FROM subscriber WHERE imsi=?",
                [imsi]
            )
            connected = sq_hlr_cursor.fetchall()
            sq_hlr.close()
            if len(connected) <= 0:
                raise OsmoHlrError('imsi %s not found' % imsi)
            # TODO(matt9j) Loss of generality here could hide consistency errors
            return connected[0]
        except sqlite3.Error as e:
            sq_hlr.close()
            raise OsmoHlrError('SQ_HLR error: %s' % e.args[0])
        except TypeError as e:
            sq_hlr.close()
            raise OsmoHlrError('SQ_HLR error: number not found')

    def get_imsi_from_msisdn(self, msisdn):
        try:
            sq_hlr = sqlite3.connect(self.hlr_db_path)
            sq_hlr_cursor = sq_hlr.cursor()
            sq_hlr_cursor.execute('SELECT imsi from subscriber WHERE msisdn=?', [msisdn])
            imsi = sq_hlr_cursor.fetchone()
            if imsi is None:
                raise OsmoHlrError('MSISDN not found in the OsmoHLR')
        except sqlite3.Error as e:
            raise OsmoHlrError('SQ_HLR error: %s' % e.args[0])

        return str(imsi)

    def get_msisdn_from_imei(self, imei):
        try:
            sq_hlr = sqlite3.connect(self.hlr_db_path)
            sq_hlr_cursor = sq_hlr.cursor()
            sql = ('SELECT subscriber.imei, subscriber.imsi, '
                   'subscriber.msisdn, Subscriber.last_lu_seen '
                   'FROM subscriber '
                   'WHERE subscriber.imei=? '
                   'ORDER BY subscriber.last_lu_seen DESC LIMIT 1;')
            sq_hlr_cursor.execute(sql, [imei])
            extensions = sq_hlr_cursor.fetchall()
            sq_hlr.close()
            return extensions
        except sqlite3.Error as e:
            sq_hlr.close()
            raise OsmoHlrError('SQ_HLR error: %s' % e.args[0])

    def get_all_5digit_msisdns(self):
        try:
            sq_hlr = sqlite3.connect(self.hlr_db_path)
            sq_hlr_cursor = sq_hlr.cursor()
            sq_hlr_cursor.execute("SELECT id, msisdn FROM subscriber WHERE length(msisdn) = 5 ")
            msisdns = sq_hlr_cursor.fetchall()
            return msisdns
        except sqlite3.Error as e:
            sq_hlr.close()
            raise OsmoHlrError('SQ_HLR error: %s' % e.args[0])

    def get_all_imeis(self):
        try:
            sq_hlr = sqlite3.connect(self.hlr_db_path)
            sq_hlr_cursor = sq_hlr.cursor()
            sql = 'SELECT DISTINCT subscriber.imei FROM subscriber '
            sq_hlr_cursor.execute(sql)
            imeis = sq_hlr_cursor.fetchall()
            sq_hlr.close()
            return imeis
        except sqlite3.Error as e:
            sq_hlr.close()
            raise OsmoHlrError('SQ_HLR error: %s' % e.args[0])

    def get_matching_partial_imeis(self, partial_imei=''):
        try:
            sq_hlr = sqlite3.connect(self.hlr_db_path)
            sq_hlr_cursor = sq_hlr.cursor()
            sql = 'SELECT DISTINCT subscriber.imei FROM subscriber WHERE subscriber.imei LIKE ? ORDER BY subscriber.imei ASC'
            sq_hlr_cursor.execute(sql, [(partial_imei+'%')])
            imeis = sq_hlr_cursor.fetchall()
            sq_hlr.close()
            return imeis
        except sqlite3.Error as e:
            sq_hlr.close()
            raise OsmoHlrError('SQ_HLR error: %s' % e.args[0])

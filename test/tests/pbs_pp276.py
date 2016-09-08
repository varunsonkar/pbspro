# coding: utf-8

# Copyright (C) 1994-2016 Altair Engineering, Inc.
# For more information, contact Altair at www.altair.com.
#
# This file is part of the PBS Professional ("PBS Pro") software.
#
# Open Source License Information:
#
# PBS Pro is free software. You can redistribute it and/or modify it under the
# terms of the GNU Affero General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# PBS Pro is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Commercial License Information:
#
# The PBS Pro software is licensed under the terms of the GNU Affero General
# Public License agreement ("AGPL"), except where a separate commercial license
# agreement for PBS Pro version 14 or later has been executed in writing with
# Altair.
#
# Altair’s dual-license business model allows companies, individuals, and
# organizations to create proprietary derivative works of PBS Pro and
# distribute them - whether embedded or bundled with other software - under
# a commercial license agreement.
#
# Use of Altair’s trademarks, including but not limited to "PBS™",
# "PBS Professional®", and "PBS Pro™" and Altair’s logos is subject to Altair's
# trademark licensing policies.

from ptl.utils.pbs_testsuite import *


class TestPp276(PBSTestSuite):

    """
    This test suite contains hook test to verify that the internal,
    swig-generated 'pbs_ifl.py' does not cause an exception.
    """

    def test_hook(self):
        """
        Create a hook, import a hook content that test pbs.server() call.
        """
        hook_name = "testhook"
        hook_body = """
import pbs
e = pbs.event()
s = pbs.server()
if e.job.id:
    jid = e.job.id
else:
    jid = "newjob"
pbs.logjobmsg(jid, "server is %s" % (s.name,))
"""
        a = {'event': 'queuejob,execjob_begin', 'enabled': 'True'}
        self.server.create_import_hook(hook_name, a, hook_body)

        j = Job(TEST_USER)
        a = {'Resource_List.select': '1:ncpus=1', 'Resource_List.walltime': 30}

        j.set_attributes(a)
        j.set_sleep_time(10)

        try:
            jid = self.server.submit(j)
        except PbsSubmitError:
            pass
        rv = self.server.log_match("Job;%s;server is %s" % (
            "newjob", self.server.shortname), max_attempts=3)
        self.assertTrue(rv)

        rv = self.mom.log_match("Job;%s;server is %s" % (
            jid, self.server.shortname), max_attempts=3)
        self.assertTrue(rv)
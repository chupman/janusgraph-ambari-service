"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Ambari Agent

"""

import os
from resource_management import *
from resource_management.core.resources.system import Execute, File
from resource_management.core.source import InlineTemplate, StaticFile
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.version import compare_versions
from resource_management.libraries.functions.copy_tarball import copy_to_hdfs
from resource_management.libraries.script.script import Script
from resource_management.libraries.functions.validate import call_and_match_output
from ambari_commons.os_family_impl import OsFamilyFuncImpl, OsFamilyImpl

class JanusGraphServiceCheck(Script):
    pass

@OsFamilyImpl(os_family=OsFamilyImpl.DEFAULT)
class JanusGraphServiceCheckDefault(JanusGraphServiceCheck):
    def service_check(self, env):
        import params
        env.set_params(params)

        File( format("{tmp_dir}/janusgraphSmoke.groovy"),
              content = StaticFile("janusgraphSmoke.groovy"),
              mode = 0755
              )


        if params.security_enabled:
            kinit_cmd = format("{kinit_path_local} -kt {smoke_user_keytab} {smokeuser_principal};")
            Execute(kinit_cmd,
                    user=params.smokeuser
                    )

	secure=""
        if params.janusgraph_server_ssl == "true" :
                secure="-k"
                if params.janusgraph_server_ssl_key_cert_file:
                    secure="--cacert " + params.janusgraph_server_ssl_key_cert_file.split(":")[1]
        grepresult=""" | grep 99"""
        if len(params.janusgraph_server_simple_authenticator) > 0:
            grepresult = ""
        headers=""" -XPOST -Hcontent-type:application/json -d '{"gremlin":"100-1"}' """
        http="http://"
        if params.janusgraph_server_ssl == "true":
            http="https://"
        janusgraph_server_host = http + format("{janusgraph_host}")
        janusgraph_port=format("{janusgraph_server_port}")
        cmd = "curl " + secure + headers + janusgraph_server_host + ":" + janusgraph_port + grepresult
	gremlin_bin = params.janusgraph_bin_dir + "/gremlin.sh"

        Execute((cmd),
                tries     = 40,
                try_sleep = 5,
                path      = format('{janusgraph_bin_dir}:/usr/sbin:/sbin:/usr/local/bin:/bin:/usr/bin'),
                user      = params.smokeuser,
                logoutput = True
                )

        Execute(format("{gremlin_bin} {tmp_dir}/janusgraphSmoke.groovy"),
                tries     = 3,
                try_sleep = 5,
                path      = format('{janusgraph_bin_dir}:/usr/sbin:/sbin:/usr/local/bin:/bin:/usr/bin'),
                user      = params.smokeuser,
                logoutput = True
                )

if __name__ == "__main__":
    # print "Track service check status"
    JanusGraphServiceCheck().execute()

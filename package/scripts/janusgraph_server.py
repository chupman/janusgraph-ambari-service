#!/usr/bin/env python
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

"""

import sys
import os
from resource_management import *
from resource_management.libraries.functions import conf_select
from resource_management.libraries.functions import stack_select
from resource_management.libraries.functions import StackFeature
from resource_management.libraries.functions.stack_features import check_stack_feature
from resource_management.libraries.functions.check_process_status import check_process_status
from janusgraph_service import janusgraph_service
import janusgraph

class JanusGraphServer(Script):
  def install(self, env):
    import params
    env.set_params(params)

    Directory([params.janusgraph_log_dir, params.janusgraph_install_dir],
            owner=params.janusgraph_user,
            group=params.janusgraph_group
    )

    File(params.janusgraph_log_file,
            mode=0644,
            owner=params.janusgraph_user,
            group=params.janusgraph_group,
            content=''
    )
    # Download Janusgraph zip, if no cached package exists on Ambari server node
    if not os.path.exists(params.janusgraph_zip):
        Execute('wget ' + params.janusgraph_download_url + ' -O ' + params.janusgraph_zip + ' -a '  + params.janusgraph_log_file, user=params.janusgraph_user)
        Execute('unzip ' + params.janusgraph_zip + ' -d ' + params.janusgraph_install_dir + ' >> ' + params.janusgraph_log_file, user=params.janusgraph_user)
        Execute('mv ' + params.janusgraph_install_dir + '/janusgraph-*/* ' + params.janusgraph_install_dir, user=params.janusgraph_user)
        Execute('rmdir ' + params.janusgraph_install_dir + '/janusgraph-*')

    #update the configs specified by user
    self.configure(env, True)


  def get_component_name(self):
    return "janusgraph-server"

  def configure(self, env, upgrade_type=None):
    import params
    env.set_params(params)
    janusgraph.janusgraph(type='server', upgrade_type=upgrade_type)

# Upgrade function not currently supported
#  def pre_upgrade_restart(self, env, upgrade_type=None):
#    Logger.info("Executing Stack Upgrade pre-restart")
#    import params
#    env.set_params(params)
#    if params.version and check_stack_feature(StackFeature.ROLLING_UPGRADE, params.version):
#      stack_select.select("janusgraph-server", params.version)
#      conf_select.select(params.stack_name, "janusgraph", params.version)

  def start(self, env, upgrade_type=None):
    import params
    env.set_params(params)
    self.configure(env)
    janusgraph_service(action = 'start')

  def stop(self, env, upgrade_type=None):
    import params
    env.set_params(params)
    janusgraph_service(action = 'stop')

  def status(self, env, upgrade_type=None):
    import params_server
    check_process_status(params_server.janusgraph_pid_file)

if __name__ == "__main__":
  JanusGraphServer().execute()

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

from resource_management.libraries.script.script import Script
from resource_management.libraries.resources.hdfs_resource import HdfsResource
from resource_management.libraries.functions import conf_select
from resource_management.libraries.functions import stack_select
from resource_management.libraries.functions.format import format
from resource_management.libraries.functions.version import format_stack_version, get_major_version
from resource_management.libraries.functions.default import default
from resource_management.libraries.functions import get_kinit_path
from resource_management.libraries.functions.get_stack_version import get_stack_version

config = Script.get_config()
tmp_dir = Script.get_tmp_dir()
stack_root= Script.get_stack_root()

stack_name = default("/hostLevelParams/stack_name", None)

stack_version_unformatted = str(config['hostLevelParams']['stack_version'])
stack_version_formatted = format_stack_version(stack_version_unformatted)
major_stack_version = get_major_version(stack_version_formatted)
full_stack_version = get_stack_version('spark2-client')

# New Cluster Stack Version that is defined during the RESTART of a Rolling Upgrade
version = default("/commandParams/version", None)

janusgraph_user = config['configurations']['janusgraph-env']['janusgraph_user']
janusgraph_group = config['configurations']['janusgraph-env']['janusgraph_group']
user_group = config['configurations']['cluster-env']['user_group']
janusgraph_log_dir = config['configurations']['janusgraph-env']['janusgraph_log_dir']
janusgraph_server_port = config['configurations']['janusgraph-env']['janusgraph_server_port']
janusgraph_hdfs_home_dir = config['configurations']['jsnaugraph-env']['janusgraph_hdfs_home_dir']
janusgraph_log_file = format("{janusgraph_log_dir}/janusgraph-{janusgraph_server_port}.log")
janusgraph_err_file = format("{janusgraph_log_dir}/janusgraph-{janusgraph_server_port}.err")

smokeuser = config['configurations']['cluster-env']['smokeuser']
smokeuser_principal = config['configurations']['cluster-env']['smokeuser_principal_name']

security_enabled = config['configurations']['cluster-env']['security_enabled']
smoke_user_keytab = config['configurations']['cluster-env']['smokeuser_keytab']
kinit_path_local = get_kinit_path(default('/configurations/kerberos-env/executable_search_paths', None))


if security_enabled:
  _hostname_lowercase = config['hostname'].lower()
  janusgraph_jaas_princ = config['configurations']['janusgraph-env']['janusgraph_principal_name'].replace('_HOST',_hostname_lowercase)
  janusgraph_keytab_path = config['configurations']['janusgraph-env']['janusgraph_keytab_path']

janusgraph_bin_dir = config['configurations']['janusgraph-env']['janusgraph_install_dir']+ '/bin'
janusgraph_data_dir = config['configurations']['janusgraph-env']['janusgraph_install_dir']+ '/data'
# JanusGraph configurations
janusgraph_conf_dir = config['configurations']['janusgraph-env']['janusgraph_install_dir']+ '/conf'
janusgraph_hbase_solr_props = config['configurations']['janusgraph-hbase-solr']['content']
janusgraph_env_props = config['configurations']['janusgraph-env']['content']
log4j_console_props = config['configurations']['janusgraph-log4j']['content']

# JanusGraph server configurations
janusgraph_server_conf_dir = config['configurations']['janusgraph-env']['janusgraph_install_dir'] + "/conf/gremlin-server"
gremlin_server_configs = config['configurations']['gremlin-server']['content']

janusgraph_server_sasl= str(config['configurations']['janusgraph-env']['SimpleAuthenticator']).lower()
janusgraph_server_simple_authenticator = ""
if janusgraph_server_sasl == "true" and 'knox-env' not in config['configurations']:
  janusgraph_server_simple_authenticator = """authentication: {
  className: org.apache.tinkerpop.gremlin.server.auth.SimpleAuthenticator,
  config: {
    credentialsDb: conf/tinkergraph-empty.properties,
    credentialsDbLocation: data/credentials.kryo}}"""

janusgraph_server_ssl= str(config['configurations']['janusgraph-env']['ssl.enabled']).lower()
janusgraph_server_ssl_key_cert_file = default('/configurations/janusgraph-env/ssl.keyCertChainFile', None)
if janusgraph_server_ssl_key_cert_file:
  janusgraph_server_ssl_key_cert_file = format(", keyCertChainFile: {janusgraph_server_ssl_key_cert_file}")
janusgraph_server_ssl_key_file = default('/configurations/janusgraph-env/ssl.keyFile', None)
if janusgraph_server_ssl_key_file:
  janusgraph_server_ssl_key_file = format(", keyFile: {janusgraph_server_ssl_key_file}")
janusgraph_server_ssl_key_password = default('/configurations/janusgraph-env/ssl.keyPassword', None)
if janusgraph_server_ssl_key_password:
  janusgraph_server_ssl_key_password = format(", keyPassword: {janusgraph_server_ssl_key_password}")
janusgraph_server_ssl_trust_cert_chain_file=default('/configurations/janusgraph-env/ssl.trustCertChainFile', None)
# not supporting 32 bit jdk.
java64_home = config['hostLevelParams']['java_home']
hadoop_config_dir = conf_select.get_hadoop_conf_dir()
hbase_config_dir = format('{stack_root}/current/hbase-client/conf')

# JanusGraph SparkGraphComputer configuration
yarn_home_dir = format('{stack_root}/current/hadoop-yarn-client')
spark_home_dir = format('{stack_root}/current/spark2-client')
spark_config_dir = format('{stack_root}/current/spark2-client/conf')
janusgraph_home_dir = config['configurations']['janusgraph-env']['janusgraph_install_dir']
janusgraph_conf_dir = config['configurations']['janusgraph-env']['janusgraph_install_dir'] + '/conf'
janusgraph_conf_hadoop_graph_dir = config['configurations']['janusgraph-env']['janusgraph_install_dir'] + '/conf/hadoop-graph'
janusgraph_data_dir = config['configurations']['janusgraph-env']['janusgraph_install_dir']+ '/data'
hadoop_lib_native_dir = format('{stack_root}/current/hadoop-client/lib/native')
janusgraph_hadoop_gryo_props = config['configurations']['hadoop-gryo']['content']
hadoop_hbase_read_props = config['configurations']['hadoop-hbase-read']['content']
janusgraph_hdfs_data_dir = "/user/janusgraph/data"
janusgraph_hdfs_spark_lib_dir = "/user/spark/share/lib/spark"
janusgraph_ext_spark_plugin_dir = config['configurations']['janusgraph-env']['janusgraph_install_dir'] + '/ext/spark-client/plugin'
local_components = default("/localComponents", [])
yarn_client_installed = ( 'YARN_CLIENT' in local_components)
hbase_master_installed = ( 'HBASE_CLIENT' in local_components)

# JanusGraph required 'storage.hostname' which is hbase cluster in IOP 4.2.
# The host name should be zooKeeper quorum
storage_hosts = config['clusterHostInfo']['zookeeper_hosts']
zookeeper_port = config['configurations']['zoo.cfg']['clientPort']
storage_host_list = []
janusgraph_zookeeper_solr_host_list = []
for hostname in storage_hosts:
  janusgraph_zookeeper_solr_hostname = hostname+format(':{zookeeper_port}/solr')
  janusgraph_zookeeper_solr_host_list.append(janusgraph_zookeeper_solr_hostname)
  storage_host_list.append(hostname)
storage_host = ",".join(storage_host_list)
zookeeper_solr_for_janusgraph_hostname  = ",".join(janusgraph_zookeeper_solr_host_list)
hbase_zookeeper_parent = config['configurations']['hbase-site']['zookeeper.znode.parent']

if 'janusgraph_server_hosts' in config['clusterHostInfo'] and len(config['clusterHostInfo']['janusgraph_server_hosts']) > 0:
  janusgraph_host = config['clusterHostInfo']['janusgraph_server_hosts'][0]

# jts jar should be copy to solr site
janusgraph_dir = config['configurations']['janusgraph-env']['janusgraph_install_dir']
janusgraph_ext_dir = config['configurations']['janusgraph-env']['janusgraph_install_dir'] + '/ext'
janusgraph_solr_conf_dir = config['configurations']['janusgraph-env']['janusgraph_install_dir'] +  '/conf/solr'
#janusgraph_solr_jar_file = format('{stack_root}/current/janusgraph-client/lib/jts-1.13.jar')
# jaas file for solr when security is enabled
janusgraph_solr_jaas_file = format('{janusgraph_solr_conf_dir}/janusgraph_solr_jaas.conf')
janusgraph_solr_client_jaas_file = format('{janusgraph_solr_conf_dir}/janusgraph_solr_client_jaas.conf')
janusgraph_solr_client_jaas_config = "index.search.solr.jaas-file=" + format('{janusgraph_solr_conf_dir}/janusgraph_solr_client_jaas.conf')
if not security_enabled:
  janusgraph_solr_client_jaas_config=""
# config for solr collection creation
index = 0
zookeeper_quorum = ""
for host in config['clusterHostInfo']['zookeeper_hosts']:
  zookeeper_quorum += host + ":" + str(zookeeper_port)
  index += 1
  if index < len(config['clusterHostInfo']['zookeeper_hosts']):
    zookeeper_quorum += ","
if "solr-config-env" in config['configurations']:
    solr_znode = default('/configurations/solr-config-env/solr_znode', '/solr')
infra_solr_hosts = default("/clusterHostInfo/infra_solr_hosts", [])
infra_solr_replication_factor = 2 if len(infra_solr_hosts) > 1 else 1
janusgraph_solr_shards = 1
janusgraph_solr_hdfs_dir = "/apps/janusgraph"
janusgraph_solr_hdfs_conf_dir = "/apps/janusgraph/conf"
janusgraph_solr_hdfs_jar = "/apps/janusgraph/jts-1.13.jar"
janusgraph_tmp_dir = format('{tmp_dir}/janusgraph')
janusgraph_solr_dir = format('{janusgraph_tmp_dir}/solr_installed')
configuration_tags = config['configurationTags']
hdfs_user = config['configurations']['hadoop-env']['hdfs_user']
janusgraph_hdfs_mode = 0775
solr_conf_dir=format('{stack_root}/current/solr-server/conf')
janusgraph_solr_configset = 'janusgraph'
janusgraph_solr_collection_name = 'janusgraph'
solr_conf_trg_file = format('{stack_root}/current/solr-server/server/solr/configsets/{janusgraph_solr_configset}/conf/solrconfig.xml')
#for create_hdfs_directory
security_enabled = config['configurations']['cluster-env']['security_enabled']
hdfs_user_keytab = config['configurations']['hadoop-env']['hdfs_user_keytab']
kinit_path_local = get_kinit_path()
hadoop_bin_dir = stack_select.get_hadoop_dir("bin")
hadoop_conf_dir = conf_select.get_hadoop_conf_dir()
hdfs_site = config['configurations']['hdfs-site']
hdfs_principal_name = default('/configurations/hadoop-env/hdfs_principal_name', 'missing_principal').replace("_HOST", hostname)
default_fs = config['configurations']['core-site']['fs.defaultFS']

# Created by chupman@us.ibm.com
janusgraph_download_url = config['configurations']['janusgraph-env']['janusgraph_download_url']
janusgraph_zip = '/tmp/janusgraph.zip'
janusgraph_install_dir = config['configurations']['janusgraph-env']['janusgraph_install_dir']
solr_cloud_enabled = config['configurations']['solr_cloud_enable']
solr_cloud_zk_directory = config['configurations']['solr_cloud_zk_directory']
solr_port = config['configurations']['solr-config-env']['solr_config_port']
solr_user= config['configurations']['solr-config-env']['solr_config_user']
solr_ssl = config['configurations']['solr-ssl']['solr_ssl_enable']
solr_server_hosts = config['clusterHostInfo']['solr_server_hosts']
solr_server_list = []
solr_server_list2 = []
solr_http = 'https' if solr_ssl else 'http'

for solr_host in solr_server_hosts:
  solr_server_list.append(format("{solr_http}://{solr_host}:{solr_port}/solr"))
solr_server_urls = ",".join(solr_server_list)

platform_name = format('{stack_root}').split('/')[2]
janusgraph_spark2_archive_dir = format('/{platform_name}/apps/{full_stack_version}/spark2')
janusgraph_spark2_archive_file = format('spark2-{platform_name}-yarn-archive.tar.gz')

import functools
#to create hdfs directory we need to call params.HdfsResource in code
HdfsResource = functools.partial(
  HdfsResource,
  user = hdfs_user,
  security_enabled = security_enabled,
  keytab = hdfs_user_keytab,
  kinit_path_local = kinit_path_local,
  hadoop_bin_dir = hadoop_bin_dir,
  hadoop_conf_dir = hadoop_conf_dir,
  principal_name = hdfs_principal_name,
  hdfs_site = hdfs_site,
  default_fs = default_fs
)


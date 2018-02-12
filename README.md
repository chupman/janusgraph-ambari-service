# janusgraph-ambari-service
JanusGraph is a scalable graph database optimized for storing and querying graphs containing hundreds of billions of vertices and edges distributed across a multi-machine cluster. JanusGraph is a transactional database that can support thousands of concurrent users executing complex graph traversals in real time.

Instructions on how to add JanusGraph to Apache Ambari or Hortonworks Data Platform(HDP) as a service can be found below.


- To download the service and link it to Ambari run the following commands
```
VERSION=`hdp-select versions | cut -d'.' -f1,2`
git clone https://github.com/chupman/janusgraph-ambari-service.git /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/JANUSGRAPH
```

```
sudo service ambari-server restart
```

- Once the ambari-server service has restarted login into the webui and click on the Actions dropdown on the lower lefthand side and select '+Add Service'.
Click on the checkbox next to Janusgraph and then press next. 
Currently JanusGraph needs to be located on the same host as Solr. If solr is not yet installed you'll need to install it through the [mpack](https://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.6.4/bk_solr-search-installation/content/ch_hdp-search-install-ambari.html).

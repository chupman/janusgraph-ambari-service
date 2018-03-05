# janusgraph-ambari-service
JanusGraph is a scalable graph database optimized for storing and querying graphs containing hundreds of billions of vertices and edges distributed across a multi-machine cluster. JanusGraph is a transactional database that can support thousands of concurrent users executing complex graph traversals in real time.

Instructions on how to add JanusGraph to Apache Ambari or Hortonworks Data Platform(HDP) as a service can be found below.


- To download the service and link it to Ambari run the following commands
```
VERSION=`hdp-select versions | head -n1 | cut -d'.' -f1,2`
git clone https://github.com/chupman/janusgraph-ambari-service.git /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/JANUSGRAPH
```

```
sudo service ambari-server restart
```
## Service Installation
- Once the ambari-server service has restarted login into the webui and click on the Actions dropdown on the lower lefthand side and select '+Add Service'.
Click on the checkbox next to Janusgraph and then press next. 
Currently JanusGraph needs to be located on the same host as Solr. If solr is not yet installed you'll need to install it through the [mpack](https://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.6.4/bk_solr-search-installation/content/ch_hdp-search-install-ambari.html).

- Click add service from the actiosn dropdown:
![Image](../master/screenshots/add_service.png?raw=true)
- The add service wizard will show all available services:
![Image](../master/screenshots/add_service_wizard.png?raw=true)
- Scroll down and check the box nex to JanusGraph and click next. If solr is not already installed it will be automatically added as a dependancy:
![Image](../master/screenshots/add_service_wizard_select_JG.png?raw=true)
- The assign masters screen shows you where all of your existing services are installed. You'll need to scroll down to find JanusGraph:
![Image](../master/screenshots/assign_masters.png?raw=true)
- Select the host you want to install Janusgraph on from the dropdown. It's reccomended to install it on the same host as solr for performance:
![Image](../master/screenshots/add_service_wizard_JG.png?raw=true)
- There is currently no JanusGraph client so the Assign Slaves and Clients screen will be bypassed. Next you'll be able to customize your installation. No user supplied values are required:
![Image](../master/screenshots/customize_services.png?raw=true)
- You can customize environment details like target directories and your gremlin server configuration:
![Image](../master/screenshots/customize_services_jg-env.png?raw=true)
- Click Deploy on the Installation review screen:
![Image](../master/screenshots/review.png?raw=true)
- Once the JanusGraph installation has been successfully complete the sevices view should look like this:
![Image](../master/screenshots/janusgraph_installed.png?raw=true)

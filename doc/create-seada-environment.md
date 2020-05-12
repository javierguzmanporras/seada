# Create seada environmnet

### Install and run SEADA tools
```
git clone https://github.com/javierguzmanporras/project-seada
cd project-seada
pip3 install -r requirements.txt
python3 -m textblob.download_corpora
```

We need add twitter development keys to environmnet variables
```
export CONSUMER_KEY=XXXXXXXXXXXXXXXXXXXXXXXXX
export CONSUMER_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
export ACCESS_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
export ACCESS_TOKEN_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

Test SEADA program
```
cd seada-ingest
python3 seada-ingest.py -h
```

### Install Docker and Docker Compose

Install Docker
```
wget https://get.docker.com -O get-docker.sh
bash get-docker.sh
```

For execute dockers tools by one user
```
groupadd docker
usermod -aG docker $USER
```
If testing on a virtual machine, it may be necessary to restart the virtual machine for changes to take 
effect. 

Verify that you can run docker commands without sudo.
```
docker run hello-world
```

Install docker-compose
```
curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
``` 

Config Docker

Set vm.max_map_count to at least 262144

```
set or change vm.max_map_count=262144 in /etc/sysctl.conf
sysctl -p
```

### Elasticsearch with dockers
```
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.6.2
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.6.2
docker-compose -f <seada-es-kibana-cerebro-docker-compose-yml> up
curl -X GET "localhost:9200/_cat/nodes?v&pretty"
```

### Kibana with dockers
```
docker pull docker.elastic.co/kibana/kibana:7.6.2
docker run --link YOUR_ELASTICSEARCH_CONTAINER_NAME_OR_ID:elasticsearch -p 5601:5601 {docker-repo}:{version}
docker-compose -f <seada-es-kibana-cerebro-docker-compose-yml> up
curl -XGET http://localhost:5601/status -I
```

### Cerebro with dockers
```
docker pull lmenezes/cerebro
docker-compose -f <seada-es-kibana-cerebro-docker-compose-yml> up
```

### Install Elesticsearch and Kibana
```
sudo apt install apt-transport-https
sudo apt install software-properties-common
sudo apt install net-tools
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
add-apt-repository "deb https://artifacts.elastic.co/packages/7.x/apt stable main"
sudo apt update
sudo apt install elasticsearch
sudo apt install kibana
sudo systemctl start elasticsearch.service
sudo systemctl start kibana.service
```

Start with SSOO
```
sudo /bin/systemctl enable elasticsearch.service
sudo /bin/systemctl enable kibana.service
```

Test ElasticSearch and Kibana
```
Elasticsearch: http://localhost:9200/
kibana: http://localhost:5601/app/kibana#/home
```




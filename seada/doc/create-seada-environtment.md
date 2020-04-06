### Install and run SEADA Project
```
git clone https://github.com/javierguzmanporras/project-seada
cd project-seada
pip3 install -r requirements.txt
export CONSUMER_KEY=XXXXXXXXXXXXXXXXXXXXXXXXX
export CONSUMER_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
export ACCESS_TOKEN=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
export ACCESS_TOKEN_SECRET=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

Test SEADA program
```
cd seada
python3 seada.py -h
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




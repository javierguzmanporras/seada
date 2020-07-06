<p align="center">
  <img src="https://github.com/javierguzmanporras/project-seada/blob/master/doc/img/seada_logo.png"/>
</p>

# SEADA
<p align="center">Sistema de Extracción y Análisis de Datos de fuentes Abiertas</p>

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Installing

A step by step how to get a development env running:

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
cd seada
python3 seada.py -h
```

Demo:

![SEADA Demo](demo/demo1.gif)


### Installing Docker
Install Docker
```
wget https://get.docker.com -O get-docker.sh
bash get-docker.sh
```

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


## Deployment

You can deploy with Docker:

* [javierguzmanporras/seada:v1](https://hub.docker.com/repository/docker/javierguzmanporras/seada)
* [javierguzmanporras/seada-analysis:v1](https://hub.docker.com/repository/docker/javierguzmanporras/seada-analysis)

## Built With

* [Python](https://github.com/python) - The programming language used
* [Tweepy](https://github.com/tweepy/tweepy) - Used to Twitter API
* [Django](https://github.com/django/django) - The web application framework used
* [Elasticsearch](https://github.com/elastic/elasticsearch) - Used to database
* [Kibana](https://github.com/elastic/kibana) - Browser-based analytics and search dashboard for Elasticsearch


## Author

* **Javier Guzmán Porras** - [OctarineHat](https://github.com/javierguzmanporras)

## License

This project is licensed under the MIT License.


# Graph embedding music search


## Usage
Install python dependencies with running:

```
pip3 install -r requirements.txt
```

For playlist evaluation is elastic search required.



## API Server

The api server uses Docker:

### build
docker build -t gemsearch .


### run
''' docker run  --rm -p 8000:80 --name gemsearch-running gemsearch

### stop
docker stop gemsearch-running


get host ip in container:
export DOCKER_HOST_IP=$(route -n | awk '/UG[ \t]/{print $2}')

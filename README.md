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
```
docker build -t api_server .
```

### run
```
docker run -d --name api_server_instance -p 80:80 api_server
```

To view output:
```
docker logs -f api_server_instance
```

Connect to instance:
```
winpty docker exec -it api_server_i bash
```


USING compose:

restart container
docker-compose restart container_name

rebuild + restart changed containers:
- for all container
    docker-compose up -d --build
- for specifix container
    docker-compose up -d --build container_name


### stop
```
docker stop api_server_instance
```

get host ip in container:
export DOCKER_HOST_IP=$(route -n | awk '/UG[ \t]/{print $2}')

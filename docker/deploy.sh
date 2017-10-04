
function copyInitialVolumeData {
    # create volume and copy data
    echo "Copy initial data to shared volume"
    docker run -v gemsearch_data:/data --name copy-helper alpine
    docker cp data/api_graph_15000/. copy-helper:/data/api
    docker rm copy-helper

    # TODO: import data to mongodb and elasticsearch
}

function stopContainers {
    docker-compose stop
}

# status of containers:
# docker-compose ps

# start composed containers
# docker-compose -f docker-compose.yml up -d


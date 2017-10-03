
echo "stop running composed dockers"
docker-compose stop

echo "--- build api_server docker"
docker build -t api_server .

# docker run -d --name api_server_i -p 80:80 api_server
echo "--- start compose"
docker-compose -f docker-compose.yml up -d

echo "--- open logs"
docker logs -f code_api_server_i_1


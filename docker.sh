
docker-compose stop
echo "stoped"

docker build -t api_server .
echo "--- stoped"
# docker run -d --name api_server_i -p 80:80 api_server
docker-compose -f docker-compose.yml up -d
echo "--- started"
docker logs -f code_api_server_i_1


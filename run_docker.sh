docker stop slavka
docker rm slavka
git pull
docker build -t slavka:latest .
docker run -d --name slavka slavka

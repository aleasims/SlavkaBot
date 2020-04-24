docker stop slavka
docker rm slavka
git pull origin master
docker build -t slavka:latest .
docker run -d --name slavka slavka

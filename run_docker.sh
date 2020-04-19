docker stop slavka
docker rm slavka
git pull
docker build -t slavka:latest .
docker run -d --env-file env_vars.txt --name slavka slavka

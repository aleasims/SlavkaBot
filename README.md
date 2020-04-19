# SlavkaBot
SlavkaBot is our new best friend ![](https://static-cdn.jtvnw.net/emoticons/v1/86/1.0)

Telegram bot aiming to replace our friend Slavka in group chat. The state-of-the-art transformer GPT2-russian from [here](https://github.com/mgrankin/ru_transformers) has been fine-tuned on our small dataset of group chat history (~1Mb).


## Deploy with Docker

### Run bot

```
docker build -t slavka:latest .
docker run -d --env-file env_vars.txt --name slavka slavka
```

env_vars.txt file:

```
MODE=prod
TOKEN=1088...
API_ID=13...
API_HASH=67bd...
```

### Stop bot

```
docker stop slavka
docker rm slavka
```
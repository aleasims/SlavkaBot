# SlavkaBot
SlavkaBot is our new best friend ![](https://static-cdn.jtvnw.net/emoticons/v1/86/1.0)

Telegram bot aiming to replace our friend Slavka in group chat. The state-of-the-art transformer GPT2-russian from [here](https://github.com/mgrankin/ru_transformers) has been fine-tuned on our small dataset of group chat history (~1Mb).


## Deploy with Docker

This will automaticly destroy existing container, pull from master branch and launch new container in daemon.

```
./run_docker.sh
```

### Config file

Example:

```
mode: dev
bot_name: sluvka_bot
telegram:
    token: 10887...
    api_id: 13...
    api_hash: 67bd...
    use_proxy: false
    proxy:
        type: MTProto
        host: ...
        port: ...
        secret: 3a19...
bot:
    phrases_path: 'slavkabot/phrases.txt'
    max_dialogs: 10
    cache_size: 10
    model:
        model_path: slavkabot/ChatBotAI/model_checkpoint
        length: 20
```

### Run manualy

```
docker build -t slavka:latest .
docker run -d --name slavka slavka
```

### Stop bot

```
docker stop slavka
docker rm slavka
```
# AI-Twitter-Bot

## About


## How to run
### Setup
You will need an OpenAI API key and a Twitter account.

#### Twitter setup
First you need to log in to Twitter and get your tag (@...), you'll need it later.
Then you need to put properties > storage > cookies. Find there "auth_token" and this value is your auth cookie.

#### Using The Creator
```bash
python 
```

### Docker
```bash
sudo docker build . -t ai-twitter-bot
```

```bash
sudo docker run -e LANGUAGE_MODEL="gpt-4-0125-preview" -e OPEN_AI_API_KEY="<your OpenAI api key>" -e TWITTER_USER_TAG="<your twitter tag>" -e TWITTER_AUTH_COOKIE="<your twitter auth cookie>" -e AI_PERSONALITY_PROMPT='<personality prompt created by The Creator>' ai-twitter-bot
```

### Local
You need to have firefox and [geckodriver](https://github.com/mozilla/geckodriver) installed to run it locally!

```bash
pip install -r requirements.txt
```




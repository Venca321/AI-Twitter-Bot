
from config.settings import OPEN_AI_API_KEY, LANGUAGE_MODEL, TWITTER_AUTH_COOKIE, TWITTER_USER_TAG
from src.bot import Bot
from src.twitter import Twitter
from src.utils import random_wait
import random


def create_post(bot:Bot, twitter:Twitter) -> None:
    try:
        post_text = bot.create_post()
        print("New post:", post_text)
        try: twitter.posts.create(post_text)
        except Exception as e: print(e); twitter.reload()
    except Exception as e: print(e)

def read_post(bot:Bot, twitter:Twitter) -> None:
    try:
        post = twitter.posts.get_post()
        output = bot.respond_to_post(post)

        if output["like"]:
            print(f"Liking {post.author_tag}'s post")
            try: twitter.posts.like(post)
            except Exception as e: print(e); twitter.reload()

        if output["repost"]:
            print(f"Reposting {post.author_tag}'s post")
            try: twitter.posts.repost(post)
            except Exception as e: print(e); twitter.reload()

        if not ("None" in output["comment"] and len(output) < 10):
            print(f"Commenting on {post.author_tag}'s post:", output["comment"])
            try: twitter.posts.comment(post, output["comment"])
            except Exception as e: print(e); twitter.reload()
    except Exception as e: print(e)


if __name__ == "__main__":
    bot = Bot(OPEN_AI_API_KEY, LANGUAGE_MODEL)
    twitter = Twitter(TWITTER_AUTH_COOKIE, TWITTER_USER_TAG, False)

    for _ in range(10): 
        if random.randint(1, 100) > 95: create_post(bot, twitter)
        else: read_post(bot, twitter)
        random_wait(5000, 10000)

    twitter.close()

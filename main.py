
from config.settings import OPEN_AI_API_KEY, LANGUAGE_MODEL, TWITTER_AUTH_COOKIE, TWITTER_USER_TAG
from src.bot import Bot
from src.twitter import Twitter
from src.utils import random_wait, Colors
import random, datetime


WORKING_HOURS_START = datetime.time(7, 30, 0)
WORKING_HOURS_END = datetime.time(22, 0, 0)

def are_working_hours():
    x = datetime.datetime.now().time()
    if WORKING_HOURS_START <= WORKING_HOURS_END:
        return WORKING_HOURS_START <= x <= WORKING_HOURS_END
    else:
        return WORKING_HOURS_START <= x or x <= WORKING_HOURS_END

def create_post(bot:Bot, twitter:Twitter) -> None:
    try:
        post_text = bot.create_post()
        print(Colors.OK, "New post:", post_text, Colors.NORMAL)
        try: twitter.posts.create(post_text)
        except Exception as e: print(e); twitter.reload()
    except Exception as e: print(e)

def read_post(bot:Bot, twitter:Twitter) -> None:
    try:
        post = twitter.posts.get_post()
        output = bot.respond_to_post(post)

        if output["like"]:
            print(f"{Colors.OK}Liking {post.author_tag}'s post{Colors.NORMAL}")
            try: twitter.posts.like(post)
            except Exception as e: print(e); twitter.reload()

        if output["repost"]:
            print(f"{Colors.OK}Reposting {post.author_tag}'s post{Colors.NORMAL}")
            try: twitter.posts.repost(post)
            except Exception as e: print(e); twitter.reload()

        if not ("None" in output["comment"] and len(output) < 10):
            print(f"{Colors.OK}Commenting on {post.author_tag}'s post:", output["comment"], Colors.NORMAL)
            try: twitter.posts.comment(post, output["comment"])
            except Exception as e: print(e); twitter.reload()
    except Exception as e: print(e)


if __name__ == "__main__":
    bot = Bot(OPEN_AI_API_KEY, LANGUAGE_MODEL)
    while True:
        if are_working_hours():
            print(f"{Colors.WARNING}I'm back to work!{Colors.NORMAL}")
            twitter = Twitter(TWITTER_AUTH_COOKIE, TWITTER_USER_TAG, False)
            for _ in range(random.randint(5, 30)): 
                if random.randint(1, 10) == 10: create_post(bot, twitter)
                else: read_post(bot, twitter)
                random_wait(2500, 20000)
            twitter.close()
            print(f"{Colors.WARNING}Going AFK...{Colors.NORMAL}")
        random_wait(1000*60*30, 1000*60*30*2.5)

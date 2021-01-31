import os
import json
import bot
import multiprocessing
CONFIG_FILE_PATH = os.getenv("CONFIG_FILE", '/Volumes/NVMESSD/Projects/test_bot_task/bot/configs/development.json')


def spawn_bot(bot_number, max_posts_per_user, max_likes_per_user):
    bot_ = bot.Bot.get_from_conf(bot_number, max_posts_per_user, max_likes_per_user)
    bot_.run()

if __name__ == '__main__':
    with open(CONFIG_FILE_PATH) as f:
        conf = json.loads(f.read())
    number_of_users = int(conf.get("number_of_users"))
    max_posts_per_user = int(conf.get("max_posts_per_user"))
    max_likes_per_user = int(conf.get("max_likes_per_user"))
    for i in range(number_of_users):
        p = multiprocessing.Process(target=spawn_bot, args=(i, max_posts_per_user, max_likes_per_user))
        p.start()
        p.join()

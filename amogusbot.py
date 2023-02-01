import praw
import random
from itertools import chain as fusion
from datetime import datetime
from pmaw import PushshiftAPI as PsAPI

reddit = praw.Reddit(client_id=SOME_ID,
                     client_secret=ANOTHER_ID,
                     password=NOT_TELLING_YOU,
                     user_agent='AmogusBot by u/minami_kun',
                     username='amoguscountbot')
pushshift = PsAPI(praw=reddit, num_workers=1) # The PMAW API

sussy_check = ["amogus", "ඞ", "sussy", "sus", "sugoma",
               "amongus", "amogi", "amoguses", "amogussy",
               "amog", "sugnoma", "baka", "impostor",
               "vent", "vented", "electrical", "suspicious",
               "among", "mogus", "hentai", "onii-chan",
               "imposter", "amonger"]

botconfirm = "^(I am a bot and this message was generated automatically. Go check the pinned post for github code.)"
now = datetime.utcnow()


def replied(comt, user):
    for reply in comt.replies:
        if reply.author == user:
            return True
    return False


print(f"Started the bot at {now}")


def amongus_generator(user): # Creates a generator with all generators created by the pmaw search
    sus_list = []
    for key2 in sussy_check:
        sus_list.append(pushshift.search_comments(q=key2, author=user, limit=1000, mem_safe=True))
    for items in fusion(sus_list):
        yield items


def amongus_counter(user): # The Counting function of my bot
    lista = []
    sussy_dict = {key1: 0 for key1 in sussy_check}
    for item1 in amongus_generator(user):
        for it in item1:
            if it['body'] not in lista and it['body'] != "[deleted]":
                for item2 in it['body'].split(" "):
                    if item2 in sussy_check:
                        lista.append(item2)
    for it2 in lista:
        sussy_dict[it2] += 1
    result = {k: v for k, v in sussy_dict.items() if v != 0}
    if not result:
        return "not sus"
    return result


while True:
    inbox = reddit.inbox.mentions()
    for ment in inbox:
        if ment.new:
            person, person1 = "", ""
            mention = ment.body.split(" ")
            check = {}
            check.update(amongus_counter(str(mention[1]))) # Here's the line of code where it gives the error
            if ment.author != reddit.user.me() \
                    and (time.mktime(now.timetuple()) - ment.created_utc) - 10000 <= 10000 \
                    and replied(ment, reddit.redditor(reddit.user.me())) is False:
                string = f"That's sus... u/{ment.author} decided to check how many sussy words {mention[1]} said.\n\n" \
                         f"So let's check it out:\n\n"\
                         "Sussy Words | Times said \n" \
                         ":-- | --:\n"
                if check == "not sus":
                    ment.reply(f"{person1} didn't said any sussy words...\n\n"
                               f"It's definitely a crewmate!\n\n"
                               f"{botconfirm}")
                    print(f"Message sent to {ment.author} in the submission {ment.submission}")
                    ment.mark_read()
                else:
                    for item in check:
                        string += f"{item} | {check[item]}\n"
                    ment.reply(f"{string}\n\n"
                               f"{botconfirm}")
                    print(f"Message sent to {ment.author} in the submission {ment.submission}")
                    ment.mark_read()

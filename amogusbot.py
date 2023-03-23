import praw
import os
import random
import time
from itertools import chain as fusion
from datetime import datetime
from pmaw import PushshiftAPI as PsAPI

reddit = praw.Reddit(client_id= os.environ.get('client_id'), 
                     client_secret= os.environ.get('client_secret'),
                     password= os.environ.get('password'),
                     user_agent='AmogusBot by u/minami_kun',
                     username='amoguscountbot')
pushshift = PsAPI(praw=reddit, num_workers=1) # Set num_workers 1 for faster results

subreddits = ["terriblefacebookmemes", "amogus", "sus", 
              "fridaynightfunkin", "touhou", "genshinmemepact", 
              "shitposting", "comedynecrophilia", "amongus", 
              "amongusmemes", "196", "meme", "thepunchlineisamongus", 
              "thepunchlineisamogus", "amongusporn", "sandycheekscockvore", "fellowkids"] # This is all subreddits that it can send copypastas for now

sussy_check = ["amogus", "ඞ", "sussy", "sus", "sugoma",
               "amongus", "amogi", "amoguses", "amogussy",
               "amog", "sugnoma", "baka", "impostor",
               "vent", "vented", "electrical", "suspicious",
               "among", "mogus", "hentai", "onii-chan",
               "imposter", "amonger"] # All words that the pushshift uses for searching
sussy_keywords = ["amogus ඞ", "amongus", "you're sus",
                  "sussy baka", "amogus", "sus", "that's sussy"] # The words that triggers the bot to send a copypasta on the subreddits list

# Here's the text files I used for making the bot, and I'll probably not share it because yeah, it's just copypastas... You can find them easily om Internet
with open("copypasta.txt", "r") as sus:
    copy = sus.read()
with open("ascii.txt", "r") as sus1:
    pasta = sus1.read()
copypasta = [copy.split("\n\n\n"), pasta.split("\n\n\n")]

botconfirm = "^(I am a bot and this message was generated automatically. Go check the pinned post for github code.)"
now = datetime.utcnow()

# Checks if I sent a message to the author that mentioned me
def replied(comt, user):
    for reply in comt.replies:
        if reply.author == user:
            return True
    return False


print(f"Started the bot at {now}")


# The search function that return all comments with all the words that are in sussy_check list
def amongus_generator(user):
    sus_list = []
    for key2 in sussy_check:
        sus_list.append(pushshift.search_comments(q=key2, author=user, limit=1000, mem_safe=True))
    for items in fusion(sus_list):
        yield items


# The main function, basically.
def amongus_counter(user):
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
    # Mention section
    inbox = reddit.inbox.mentions()
    for ment in inbox:
        if ment.new:
            person, person1 = "", ""
            mention = ment.body.split(" ") # Here creates a list that separate the u/AmogusCountBot from the mentioned user
            check = {}
            if len(mention) == 1: 
                check.update(amongus_counter(str(ment.author)))
                person += "themself"
                person1 += "You"
            else:
                check.update(amongus_counter(str(mention[1])))
                print(check) # Just a checking... You can ignore that
                person += f"{mention[1]}"
                person1 += f"{mention[1]}"
            # It avoids replying to itself, replying to really old messages and replying to already replied mentions
            if ment.author != reddit.user.me() \
                    and (time.mktime(now.timetuple()) - ment.created_utc) - 10000 <= 10000 \
                    and replied(ment, reddit.redditor(reddit.user.me())) is False:
                string = f"That's sus... u/{ment.author} decided to check how many sussy words {person} said.\n\n" \
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
    # Copypasta section
    for sub in subreddits:
        subreddit = reddit.subreddit(sub)
        for comment in subreddit.comments(limit=None):
            for key in sussy_keywords:
                if comment.body.lower().startswith(key):
                    # Similar to the if function of the mention section, except it also avoids replying to unsaved messages
                    if comment.body.lower().startswith(key) \
                            and comment.author != reddit.user.me() \
                            and (time.mktime(now.timetuple()) - comment.created_utc) - 10000 <= 10000 \
                            and comment.saved is False \
                            and replied(comment, reddit.redditor(reddit.user.me())) is False:
                        comment.save()
                        response = random.choice(copypasta)
                        comment.reply(f"{random.choice(response)}\n\n"
                                      f"{botconfirm}")
                        print(f"Message send! {comment.body}")

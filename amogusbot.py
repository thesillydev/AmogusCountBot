import praw
import random
from datetime import datetime
from pmaw import PushshiftAPI as PsAPI

reddit = praw.Reddit(client_id=SOME_ID,
                     client_secret=ANOTHER_ID,
                     password=NOT_TELLING_YOU,
                     user_agent='AmogusBot by u/minami_kun',
                     username='amoguscountbot')
pushshift = PsAPI(praw=reddit, num_workers=1)

# List with all parameters that's used to the counting function
sussy_check = ["amogus", "ඞ", "sussy", "sus", "sugoma",
               "amongus", "amogi", "amoguses", "amogussy",
               "amog", "sugnoma", "baka", "impostor",
               "vent", "vented", "electrical"]

botconfirm = "^(I am a bot and this message was generated automatically. Go check the pinned post for github code.)"
now = datetime.utcnow()

# Check if it the message wasn't already replied
def replied(comt, user):
    for reply in comt.replies:
        if reply.author == user:
            return True
    return False


print(f"Started the bot at {now}")

# The counter function... Used to make my bot cleaner and with less codes...
def amongus_counter(user):
    sussy_dict = {key1: 0 for key1 in sussy_check}
    for key2 in sussy_check:
        search = pushshift.search_comments(q=key2, author=user, limit=1000, mem_safe=True)
        for sussy_item in search:
            if sussy_item['body'] != "[deleted]":
                for it in sussy_item['body'].split(" "):
                    if it.lower() in sussy_check:
                        sussy_dict[it.lower()] += 1
        result = {k: v for k, v in sussy_dict.items() if v != 0}
        if not result:
            return "not sus"
        return result


inbox = reddit.inbox.mentions()
while True:
    for ment in inbox:
        if ment.new:
            person, person1 = "", ""
            mention = ment.body.split(" ")
            if mention[0].lower() == "u/amoguscountbot" and len(mention) == 1:
                check = amongus_counter(ment.author)
                person += "themself"
                person1 += "You"
            else:
                check = amongus_counter(mention[1])
                person += f"{mention[1]}"
                person1 += f"{mention[1]}"
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
                    print(f"Message sent to {ment.author} in the comment {ment.submission}")
                    ment.mark_read()
                else:
                    for item in check:
                        string += f"{item} | {check[item]}\n"
                    ment.reply(f"{string}\n\n"
                               f"{botconfirm}")
                    print(f"Message sent to {ment.author} in the comment {ment.submission}")
                    ment.mark_read()

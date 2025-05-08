import os, time, json, tweepy
from telegram import Bot

bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))
client = tweepy.Client(bearer_token=os.getenv("TWITTER_BEARER_TOKEN"))

tracked_users = os.getenv("TRACKED_USERS", "jack,elonmusk").split(",")
keywords = os.getenv("KEYWORDS", "AI,OpenAI,urgent").split(",")
chat_id = os.getenv("TELEGRAM_CHAT_ID")
state_file = "state.json"

def load_state():
    if os.path.exists(state_file):
        with open(state_file) as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(state_file, "w") as f:
        json.dump(state, f)

def get_user_id(username):
    user = client.get_user(username=username)
    return user.data.id if user.data else None

def fetch_new_tweets(username, since_id):
    user_id = get_user_id(username)
    if not user_id:
        return []

    tweets = client.get_users_tweets(
        id=user_id,
        max_results=5,
        since_id=since_id,
        tweet_fields=["created_at", "text"],
        exclude=["retweets", "replies"]
    )

    return list(reversed(tweets.data)) if tweets.data else []

def matches_keywords(text):
    return any(kw.lower() in text.lower() for kw in keywords)

def send_to_telegram(tweet, username):
    url = f"https://twitter.com/{username}/status/{tweet.id}"
    msg = f"*{username} tweeted:*
{tweet.text}

[View Tweet]({url})"
    bot.send_message(chat_id=chat_id, text=msg, parse_mode='Markdown')

if __name__ == "__main__":
    print("Bot started.")
    state = load_state()
    while True:
        for user in tracked_users:
            try:
                since_id = state.get(user)
                tweets = fetch_new_tweets(user, since_id)
                for tweet in tweets:
                    if matches_keywords(tweet.text):
                        send_to_telegram(tweet, user)
                if tweets:
                    state[user] = tweets[-1].id
                    save_state(state)
            except Exception as e:
                print(f"Error with {user}: {e}")
        time.sleep(60)

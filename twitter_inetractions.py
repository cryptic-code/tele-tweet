from os import getenv
import tweepy

TWITTER_KEY = getenv('TWITTER_KEY')
TWITTER_SECRET = getenv("TWITTER_SECRET")

auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET)

def validate_tweets(tweets: list) -> dict:
    for tweet in tweets:
        tweet = tweet.strip('\n ')
        if len(tweet) > 280:
            return {"error": True, "msg_index": str(tweets.index(tweet)+1), "msg_len": str(len(tweet))}
    return {"error": False}

def post_tweets(auth: dict, tweets: list) -> dict:
    """ Post a tweet/thread and return its link. """

    auth.set_access_token(auth['access_token'], auth['access_token_secret'])
    api = tweepy.API(auth)

    tweet_count = 0
    tweet_url = None
    error = False

    if not len(tweets) > 1:
        try:
            tweet = tweets[0].strip('\n ')
            tweet = api.update_status(status=tweet)
            screen_name = tweet.user.screen_name
            tweet_id = tweet.id_str
            tweet_url = f"https://twitter.com/{screen_name}/status/{tweet_id}"
            tweet_count+=1
        except:
            error = True
    else:
        try:
            start_tweet = tweets[0].strip('\n ')
            start_tweet = api.update_status(status=start_tweet)
            screen_name = start_tweet.user.screen_name
            tweet_id = start_tweet.id_str
            tweet_url = f"https://twitter.com/{screen_name}/status/{tweet_id}"
            tweet_count+=1

            for tweet in tweets[1:]:
                tweet = tweet.strip('\n ')
                api.update_status(status=tweet, in_reply_to_status_id=tweet_id)
                tweet_count+=1
        except:
           error = True

    return {"error": error, "tweet_url": tweet_url, 'tweet_count': tweet_count}

def create_auth_url() -> dict:
    """ Create a Twitter authorization url and send it back with the request token. """

    auth_url = auth.get_authorization_url()
    req_token = auth.request_token['oauth_token']

    return [auth_url, req_token]

def authorize(req_token: str, verifier: str) -> dict:
    # load auth.request_token before requesting access tokens
    auth.request_token = {'oauth_token': req_token, 'oauth_token_secret': verifier}
    try:
        auth.get_access_token(verifier)
        access_token = auth.access_token
        access_token_secret = auth.access_token_secret
        auth.set_access_token(access_token, access_token_secret)
        return {'access_token': access_token, 'access_token_secret': access_token_secret}
    except Exception as e:
        print(e)
        return None

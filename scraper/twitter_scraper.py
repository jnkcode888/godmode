import os
import tweepy
from datetime import datetime, timedelta
from supabase_client import insert_mention, supabase
from dotenv import load_dotenv

load_dotenv()

# Twitter API credentials
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

# Initialize Twitter client with both OAuth 1.0a and OAuth 2.0
client = tweepy.Client(
    bearer_token=TWITTER_BEARER_TOKEN,
    consumer_key=TWITTER_API_KEY,
    consumer_secret=TWITTER_API_SECRET,
    access_token=TWITTER_ACCESS_TOKEN,
    access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
    wait_on_rate_limit=True
)

def scrape_twitter(companies, max_results=50):
    # Calculate previous day's UTC midnight range
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    start_time = datetime.combine(yesterday, datetime.min.time()).isoformat() + "Z"
    end_time = datetime.combine(today, datetime.min.time()).isoformat() + "Z"
    for company in companies:
        company_name = company['name'] if isinstance(company, dict) else company
        company_id = company['id'] if isinstance(company, dict) else None
        try:
            # Search for tweets from previous day
            tweets = client.search_recent_tweets(
                query=f'"{company_name}" -is:retweet lang:en',
                max_results=max_results,
                tweet_fields=['created_at', 'public_metrics', 'author_id'],
                start_time=start_time,
                end_time=end_time
            )
            if tweets.data:
                for tweet in tweets.data:
                    # Get user info
                    user = client.get_user(id=tweet.author_id).data
                    data = {
                        'source': 'twitter',
                        'text': tweet.text,
                        'author': user.username,
                        'date': tweet.created_at.strftime('%Y-%m-%dT%H:%M:%SZ'),
                        'likes': tweet.public_metrics['like_count'],
                        'retweets': tweet.public_metrics['retweet_count'],
                        'upvotes': None,
                        'matched_company': company_id,
                        'link': f'https://twitter.com/{user.username}/status/{tweet.id}'
                    }
                    insert_mention(data)
        except Exception as e:
            print(f"Error scraping tweets for {company_name}: {str(e)}")

if __name__ == "__main__":
    response = supabase.table('companies').select('id, name').execute()
    companies = response.data
    scrape_twitter(companies) 
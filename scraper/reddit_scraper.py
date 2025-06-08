import os
import praw
from datetime import datetime, timedelta, timezone
from supabase_client import insert_mention, supabase
from dotenv import load_dotenv

load_dotenv()

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "kenya-monitor-script")

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

def scrape_reddit(companies, subreddit_name="Kenya", max_results=50):
    subreddit = reddit.subreddit(subreddit_name)
    # Calculate previous day's UTC midnight range
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    start_timestamp = int(datetime.combine(yesterday, datetime.min.time()).replace(tzinfo=timezone.utc).timestamp())
    end_timestamp = int(datetime.combine(today, datetime.min.time()).replace(tzinfo=timezone.utc).timestamp())
    for company in companies:
        company_name = company['name'] if isinstance(company, dict) else company
        company_id = company['id'] if isinstance(company, dict) else None
        # Search posts
        for i, post in enumerate(subreddit.search(company_name, sort="new", limit=max_results)):
            if start_timestamp <= int(post.created_utc) < end_timestamp:
                data = {
                    'source': 'reddit',
                    'text': post.title + "\n" + (post.selftext or ""),
                    'author': str(post.author),
                    'date': datetime.fromtimestamp(post.created_utc, timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'likes': None,
                    'retweets': None,
                    'upvotes': post.score,
                    'matched_company': company_id,
                    'link': f'https://reddit.com{post.permalink}'
                }
                insert_mention(data)
        # Search comments
        for i, comment in enumerate(subreddit.comments(limit=max_results)):
            if company_name.lower() in comment.body.lower() and start_timestamp <= int(comment.created_utc) < end_timestamp:
                data = {
                    'source': 'reddit',
                    'text': comment.body,
                    'author': str(comment.author),
                    'date': datetime.fromtimestamp(comment.created_utc, timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    'likes': None,
                    'retweets': None,
                    'upvotes': comment.score,
                    'matched_company': company_id,
                    'link': f'https://reddit.com{comment.permalink}'
                }
                insert_mention(data)

if __name__ == "__main__":
    response = supabase.table('companies').select('id, name').execute()
    companies = response.data
    scrape_reddit(companies) 
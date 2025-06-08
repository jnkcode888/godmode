# Kenyan Companies Social Media Monitor

A full-stack web application to monitor Kenyan companies, brands, and public figures by scraping data from Twitter (X) and Reddit. The data is stored in Supabase and can be displayed in a Next.js dashboard.

## Features

- Twitter data scraping using Twitter API v2
- Reddit data scraping using PRAW
- Data storage in Supabase
- Row Level Security (RLS) for data protection
- Rate limiting handling
- Scheduled data collection

## Prerequisites

- Python 3.13+
- Supabase account
- Twitter Developer Account
- Reddit Developer Account

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-name>
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:

```env
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# Twitter
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
TWITTER_BEARER_TOKEN=your_twitter_bearer_token

# Reddit
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_reddit_user_agent
```

4. Set up Supabase:
   - Create a new project in Supabase
   - Run the migrations in `supabase/migrations/` directory
   - Configure RLS policies

## Usage

1. Run Twitter scraper:

```bash
python scraper/twitter_scraper.py
```

2. Run Reddit scraper:

```bash
python scraper/reddit_scraper.py
```

3. Run scheduled scraping:

```bash
python scraper/scheduler.py
```

## Project Structure

```
.
├── README.md
├── requirements.txt
├── scraper/
│   ├── twitter_scraper.py
│   ├── reddit_scraper.py
│   ├── supabase_client.py
│   └── scheduler.py
└── supabase/
    └── migrations/
        ├── 20240315_initial_schema.sql
        └── 20240320_add_rls_policies.sql
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

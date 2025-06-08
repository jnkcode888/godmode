import schedule
import time
import logging
from datetime import datetime
from twitter_scraper import scrape_twitter
from reddit_scraper import scrape_reddit
from supabase_client import supabase

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def run_scrapers():
    """Run both Twitter and Reddit scrapers."""
    logger.info("Starting scheduled scraping run")
    
    try:
        # Get companies from database
        response = supabase.table('companies').select('*').execute()
        companies = response.data
        
        if not companies:
            logger.warning("No companies found in database")
            return
            
        # Run Twitter scraper
        logger.info("Running Twitter scraper")
        scrape_twitter(companies)
        
        # Run Reddit scraper
        logger.info("Running Reddit scraper")
        scrape_reddit(companies)
        
        logger.info("Scheduled scraping run completed successfully")
        
    except Exception as e:
        logger.error(f"Error during scheduled scraping: {str(e)}")

def main():
    """Set up and run the scheduler."""
    logger.info("Starting scraper scheduler")
    
    # Schedule scrapers to run every day at midnight (00:00)
    schedule.every().day.at("00:00").do(run_scrapers)
    
    # Run immediately on startup (optional, can remove if not desired)
    run_scrapers()
    
    # Keep the script running
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
        except Exception as e:
            logger.error(f"Scheduler error: {str(e)}")
            time.sleep(300)  # Wait 5 minutes before retrying

if __name__ == "__main__":
    main() 
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def insert_mention(data: dict):
    """Insert a mention into the mentions table."""
    try:
        return supabase.table("mentions").insert(data).execute()
    except Exception as e:
        print(f"Error inserting data into Supabase: {str(e)}")
        raise 
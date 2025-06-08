import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Print environment variables to verify they're loaded
print("SUPABASE_URL:", os.getenv("SUPABASE_URL"))
print("SUPABASE_KEY:", os.getenv("SUPABASE_KEY"))

# Test Supabase connection
try:
    # Try with positional arguments instead of named parameters
    supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
    
    # Try a simple query to test the connection
    response = supabase.table("mentions").select("*").limit(1).execute()
    print("\nConnection successful!")
    print("Test query response:", response)
    
except Exception as e:
    print("\nError connecting to Supabase:", str(e)) 
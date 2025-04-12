from dotenv import load_dotenv
import os
load_dotenv()

from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

supabase = create_client(url, key)

# Test: Verificar conexión con Supabase
response = supabase.table('events').select('*').execute()
print("Data from Supabase:", response.data)
import psycopg2
import os

DB_URI = os.environ.get("SUPABASE_DB_URI", "postgresql://postgres.wtzivbtyoiyvwoknuzom:SupabaseIPQC2026!!@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres")

def run():
    print(f"Connecting to {DB_URI.split('@')[1]}...")
    conn = psycopg2.connect(DB_URI)
    cursor = conn.cursor()
    
    cursor.execute("ALTER TABLE public.audit_details ADD COLUMN IF NOT EXISTS category TEXT;")
    cursor.execute("ALTER TABLE public.audit_details ADD COLUMN IF NOT EXISTS question_zh TEXT;")
    cursor.execute("ALTER TABLE public.audit_details ADD COLUMN IF NOT EXISTS question_en TEXT;")
    
    # Also reload the schema cache so PostgREST instantly sees the new columns
    cursor.execute("NOTIFY pgrst, 'reload schema';")
    
    conn.commit()
    conn.close()
    print("Added columns successfully!")

if __name__ == "__main__":
    run()

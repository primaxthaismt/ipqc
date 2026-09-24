import psycopg2
conn = psycopg2.connect(
    host='aws-0-ap-southeast-1.pooler.supabase.com',
    port=6543,
    dbname='postgres',
    user='postgres.hnzmfcqnlqbbjpaxuucg',
    password='!Qaz7410@wsx7410'
)
cursor = conn.cursor()
cursor.execute('ALTER TABLE public.audit_details ADD COLUMN IF NOT EXISTS category TEXT;')
cursor.execute('ALTER TABLE public.audit_details ADD COLUMN IF NOT EXISTS question_zh TEXT;')
cursor.execute('ALTER TABLE public.audit_details ADD COLUMN IF NOT EXISTS question_en TEXT;')
cursor.execute("NOTIFY pgrst, 'reload schema';")
conn.commit()
conn.close()
print('Added columns successfully!')

CREATE TABLE IF NOT EXISTS public.users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'auditor',
    line_assignment TEXT DEFAULT 'All Lines',
    language_pref TEXT DEFAULT 'zh',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.stations (
    id TEXT PRIMARY KEY,
    station_code TEXT UNIQUE NOT NULL,
    station_name TEXT NOT NULL,
    line_name TEXT NOT NULL,
    area_name TEXT DEFAULT 'SMT Surface Mount Area',
    process_type TEXT NOT NULL,
    sequence_order INTEGER DEFAULT 1,
    pos_x INTEGER DEFAULT 50,
    pos_y INTEGER DEFAULT 50,
    width INTEGER DEFAULT 220,
    height INTEGER DEFAULT 130,
    qr_code_url TEXT,
    status TEXT DEFAULT 'OK',
    last_audit_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS public.checklist_master (
    id SERIAL PRIMARY KEY,
    item_no INTEGER UNIQUE NOT NULL,
    process TEXT NOT NULL,
    station_tag TEXT NOT NULL,
    requires_qty BOOLEAN DEFAULT FALSE,
    zh TEXT NOT NULL,
    en TEXT NOT NULL,
    th TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS public.audits (
    id TEXT PRIMARY KEY,
    station_code TEXT NOT NULL,
    station_name TEXT NOT NULL,
    line_name TEXT NOT NULL,
    auditor TEXT NOT NULL,
    shift TEXT NOT NULL,
    time_block TEXT NOT NULL,
    model_no TEXT NOT NULL,
    work_order TEXT DEFAULT 'WO-2026-0802-001',
    audit_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    overall_status TEXT DEFAULT 'OK',
    pass_count INTEGER DEFAULT 0,
    fail_count INTEGER DEFAULT 0,
    na_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS public.audit_details (
    id SERIAL PRIMARY KEY,
    audit_id TEXT REFERENCES public.audits(id) ON DELETE CASCADE,
    item_no INTEGER,
    result TEXT NOT NULL,
    qty INTEGER DEFAULT 0,
    remark TEXT,
    photo_url TEXT
);

CREATE TABLE IF NOT EXISTS public.capa (
    id TEXT PRIMARY KEY,
    audit_id TEXT,
    station_code TEXT NOT NULL,
    line_name TEXT NOT NULL,
    item_no INTEGER NOT NULL,
    defect_description TEXT NOT NULL,
    photo_url TEXT,
    severity TEXT DEFAULT 'HIGH',
    status TEXT DEFAULT 'OPEN',
    owner TEXT,
    root_cause TEXT,
    action_taken TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    due_date DATE
);

ALTER TABLE public.stations ADD COLUMN IF NOT EXISTS area_name TEXT DEFAULT 'SMT Surface Mount Area';
ALTER TABLE public.stations ADD COLUMN IF NOT EXISTS sequence_order INTEGER DEFAULT 1;
ALTER TABLE public.stations ADD COLUMN IF NOT EXISTS pos_x INTEGER DEFAULT 50;
ALTER TABLE public.stations ADD COLUMN IF NOT EXISTS pos_y INTEGER DEFAULT 50;
ALTER TABLE public.stations ADD COLUMN IF NOT EXISTS width INTEGER DEFAULT 220;
ALTER TABLE public.stations ADD COLUMN IF NOT EXISTS height INTEGER DEFAULT 130;
ALTER TABLE public.stations ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
ALTER TABLE public.audits ADD COLUMN IF NOT EXISTS work_order TEXT DEFAULT 'WO-2026-0802-001';

ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.stations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.checklist_master ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audits ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_details ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.capa ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "allow_public_all_users" ON public.users;
CREATE POLICY "allow_public_all_users" ON public.users FOR ALL USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "allow_public_all_stations" ON public.stations;
CREATE POLICY "allow_public_all_stations" ON public.stations FOR ALL USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "allow_public_all_checklist_master" ON public.checklist_master;
CREATE POLICY "allow_public_all_checklist_master" ON public.checklist_master FOR ALL USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "allow_public_all_audits" ON public.audits;
CREATE POLICY "allow_public_all_audits" ON public.audits FOR ALL USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "allow_public_all_audit_details" ON public.audit_details;
CREATE POLICY "allow_public_all_audit_details" ON public.audit_details FOR ALL USING (true) WITH CHECK (true);
DROP POLICY IF EXISTS "allow_public_all_capa" ON public.capa;
CREATE POLICY "allow_public_all_capa" ON public.capa FOR ALL USING (true) WITH CHECK (true);

GRANT ALL ON public.users TO anon, authenticated, postgres, service_role;
GRANT ALL ON public.stations TO anon, authenticated, postgres, service_role;
GRANT ALL ON public.checklist_master TO anon, authenticated, postgres, service_role;
GRANT ALL ON public.audits TO anon, authenticated, postgres, service_role;
GRANT ALL ON public.audit_details TO anon, authenticated, postgres, service_role;
GRANT ALL ON public.capa TO anon, authenticated, postgres, service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated, postgres, service_role;

-- ================================================================================
-- Smart IPQC Digital Audit System Database Schema (PostgreSQL on Oracle VM)
-- ================================================================================

CREATE TABLE IF NOT EXISTS public.users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'auditor',
    line_assignment TEXT DEFAULT 'All Lines',
    language_pref TEXT DEFAULT 'zh',
    email TEXT DEFAULT '',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS public.stations (
    id TEXT PRIMARY KEY,
    station_code TEXT UNIQUE NOT NULL,
    station_name TEXT NOT NULL,
    line_name TEXT NOT NULL,
    phase TEXT DEFAULT 'Phase 1',
    area_name TEXT DEFAULT 'SMT Surface Mount Area',
    process_type TEXT NOT NULL,
    standard_doc TEXT DEFAULT '5Q4-046',
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
    standard_doc TEXT DEFAULT '5Q4-046',
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
    work_order TEXT DEFAULT 'N/A',
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
    owner TEXT DEFAULT 'Line Supervisor',
    root_cause TEXT,
    action_taken TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    due_date DATE
);

CREATE TABLE IF NOT EXISTS public.fai_audits (
    audit_id TEXT PRIMARY KEY,
    audit_type TEXT DEFAULT 'FIRST_ARTICLE',
    process_type TEXT DEFAULT 'SOLDER_PASTE',
    line_name TEXT NOT NULL,
    work_order TEXT NOT NULL,
    model_no TEXT NOT NULL,
    customer TEXT,
    shift TEXT DEFAULT 'Day Shift',
    audit_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    green_hf TEXT DEFAULT 'Green/HF',
    pcba_photo_url TEXT,
    sample_qty INTEGER DEFAULT 5,
    lot_qty INTEGER DEFAULT 1000,
    pcb_pn TEXT,
    pcb_date_code TEXT,
    pdm_bom_version TEXT,
    solder_paste_brand TEXT,
    first_article_time TEXT,
    stencil_thickness TEXT,
    stencil_no TEXT,
    stencil_sn TEXT,
    paste_thickness_range TEXT,
    thickness_points JSONB DEFAULT '[]'::jsonb,
    notes_eng_change TEXT,
    ecn_mn_req TEXT,
    customer_email_req TEXT,
    critical_components JSONB DEFAULT '[]'::jsonb,
    details JSONB DEFAULT '[]'::jsonb,
    auditor TEXT,
    verifier TEXT,
    overall_status TEXT DEFAULT 'OK',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_audits_audit_time ON public.audits(audit_time);
CREATE INDEX IF NOT EXISTS idx_audits_line_name ON public.audits(line_name);
CREATE INDEX IF NOT EXISTS idx_audits_station_code ON public.audits(station_code);
CREATE INDEX IF NOT EXISTS idx_audits_time_block ON public.audits(time_block);
CREATE INDEX IF NOT EXISTS idx_audit_details_audit_id ON public.audit_details(audit_id);
CREATE INDEX IF NOT EXISTS idx_capa_status ON public.capa(status);
CREATE INDEX IF NOT EXISTS idx_capa_line_name ON public.capa(line_name);
CREATE INDEX IF NOT EXISTS idx_fai_audits_time ON public.fai_audits(audit_time);

-- Grant privileges to appuser
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO appuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO appuser;

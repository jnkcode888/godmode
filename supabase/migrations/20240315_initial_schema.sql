-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create mentions table
CREATE TABLE IF NOT EXISTS mentions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source TEXT NOT NULL CHECK (source IN ('twitter', 'reddit')),
    text TEXT NOT NULL,
    author TEXT NOT NULL,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    likes INTEGER,
    retweets INTEGER,
    upvotes INTEGER,
    matched_company TEXT NOT NULL,
    link TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create companies table
CREATE TABLE IF NOT EXISTS companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL UNIQUE,
    keywords TEXT[] NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert initial companies
INSERT INTO companies (name, keywords) VALUES
    ('Safaricom', ARRAY['safaricom', 'safcom']),
    ('Equity Bank', ARRAY['equity', 'equity bank', 'equitybank']),
    ('Kenya Power', ARRAY['kenya power', 'kplc', 'kenpower'])
ON CONFLICT (name) DO NOTHING;

-- Enable RLS (Row Level Security) if needed
ALTER TABLE mentions ENABLE ROW LEVEL SECURITY;
ALTER TABLE companies ENABLE ROW LEVEL SECURITY; 
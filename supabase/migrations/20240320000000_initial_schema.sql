-- Create companies table
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    keywords TEXT[] NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create mentions table
CREATE TABLE mentions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source TEXT NOT NULL CHECK (source IN ('twitter', 'reddit')),
    text TEXT NOT NULL,
    author TEXT NOT NULL,
    date TIMESTAMP WITH TIME ZONE NOT NULL,
    link TEXT NOT NULL,
    matched_company UUID REFERENCES companies(id),
    engagement_score INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create alerts table
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID REFERENCES companies(id),
    type TEXT NOT NULL CHECK (type IN ('sentiment', 'volume', 'engagement')),
    threshold INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes for better query performance
CREATE INDEX idx_mentions_source ON mentions(source);
CREATE INDEX idx_mentions_date ON mentions(date);
CREATE INDEX idx_mentions_matched_company ON mentions(matched_company);
CREATE INDEX idx_mentions_engagement_score ON mentions(engagement_score);
CREATE INDEX idx_companies_name ON companies(name);
CREATE INDEX idx_alerts_company_id ON alerts(company_id);

-- Add trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_companies_updated_at
    BEFORE UPDATE ON companies
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_alerts_updated_at
    BEFORE UPDATE ON alerts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column(); 
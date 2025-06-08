-- Add index for engagement_score after the column exists
CREATE INDEX IF NOT EXISTS idx_mentions_engagement_score ON mentions(engagement_score); 
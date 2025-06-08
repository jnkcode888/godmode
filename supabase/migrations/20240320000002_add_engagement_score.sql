-- Add engagement_score column to mentions table
ALTER TABLE mentions 
ADD COLUMN IF NOT EXISTS engagement_score INTEGER DEFAULT 0;

-- Update existing mentions with engagement scores
UPDATE mentions
SET engagement_score = 
    CASE 
        WHEN source = 'twitter' THEN 
            COALESCE((data->>'retweet_count')::integer, 0) + 
            COALESCE((data->>'favorite_count')::integer, 0) + 
            COALESCE((data->>'reply_count')::integer, 0)
        WHEN source = 'reddit' THEN 
            COALESCE((data->>'score')::integer, 0) + 
            COALESCE((data->>'num_comments')::integer, 0)
        ELSE 0
    END; 
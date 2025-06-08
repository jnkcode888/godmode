-- Drop existing policies if any
DROP POLICY IF EXISTS "Enable insert for service role" ON mentions;
DROP POLICY IF EXISTS "Enable read access for all users" ON mentions;

-- Create policy for service role to insert data
CREATE POLICY "Enable insert for service role" ON mentions
    FOR INSERT
    TO authenticated
    WITH CHECK (true);

-- Create policy for reading data
CREATE POLICY "Enable read access for all users" ON mentions
    FOR SELECT
    TO authenticated
    USING (true);

-- Grant necessary permissions
GRANT ALL ON mentions TO authenticated; 
-- Use a Common Table Expression (CTE) for clarity
WITH inconsistent_groups AS (
  -- Step 1: Find all subjects with inconsistent bodies
  -- and count how many total emails are in each of these groups.
  SELECT
    subject,
    COUNT(*) AS num_rows_in_group
  FROM
    message
  GROUP BY
    subject
  HAVING
    COUNT(DISTINCT body) > 1
)
-- Step 2: Sum the row counts from all the groups found in Step 1.
SELECT
  SUM(num_rows_in_group) AS total_affected_rows
FROM
  inconsistent_groups;

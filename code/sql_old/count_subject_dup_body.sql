SELECT
  COUNT(*) AS total_inconsistent_subjects
FROM (
  SELECT
    subject, body
  FROM
    message
  GROUP BY
    subject, body
  HAVING
    COUNT(DISTINCT body) > 1
);

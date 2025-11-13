SELECT
  COUNT(*) AS total_inconsistent_subjects
FROM (
  SELECT
    subject
  FROM
    message
  GROUP BY
    subject
  HAVING
    COUNT(DISTINCT body) == 1
);

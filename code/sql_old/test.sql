-- SELECT subject, body
-- From message
-- WHERE subject = (
--     SELECT subject FROM (
--         SELECT
--         subject,
--         COUNT(*) AS num_rows_in_group
--       FROM
--         message
--       GROUP BY
--         subject
--       HAVING
--         COUNT(*) > 1
--     ))
-- GROUP BY
--     subject, body
-- ;

-- ------- counting unique subject and body from dubplicate subject
-- SELECT COUNT(*) FROM (
--     SELECT subject, body
--     FROM message
--     WHERE subject IN (
--     SELECT subject FROM (
--         SELECT
--         subject,
--         COUNT(*)
--       FROM
--         message
--       GROUP BY
--         subject
--       HAVING
--         COUNT(*) > 1
--     ))
--     GROUP BY subject, body
--
-- );



SELECT COUNT(*)
FROM (
    SELECT body
    FROM message
    GROUP BY body
)

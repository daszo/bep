DROP VIEW IF EXISTS v_ExpMessages;

CREATE VIEW v_ExpMessages AS
SELECT * FROM v_CleanMessages
WHERE folder IS 'inbox';

DROP VIEW IF EXISTS v_CleanMessages;

CREATE VIEW v_CleanMessages AS
SELECT * FROM (
    SELECT *
    FROM v_DroppedFolders
    WHERE clean_length_word > 20
    
GROUP BY subject, body
);

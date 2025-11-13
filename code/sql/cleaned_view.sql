DROP VIEW IF EXISTS v_CleanMessages;

CREATE VIEW v_CleanMessages AS
SELECT * FROM (
    SELECT *
    FROM v_DroppedFolders
    WHERE length_word > 10 
    
GROUP BY subject, body
);

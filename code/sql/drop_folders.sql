DROP VIEW IF EXISTS v_DroppedFolders;

CREATE VIEW v_DroppedFolders AS
    SELECT *
    FROM Message
    WHERE folder NOT IN (
        'deleted_items',
        'calendar',
        'contacts',
        'notes',
        'drafts',
        'outbox',
        'discussion_threads',
        'all_documents',
        'notes_inbox' 
);

-- deletes anonymous users created more than 30 days ago
delete from auth.users
where
    is_anonymous is true
    and created_at < now() - interval '30 days';
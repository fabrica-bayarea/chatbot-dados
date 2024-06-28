create
or replace function fetch_conversations () returns table (
  id uuid,
  owner_id uuid,
  created_at timestamptz,
  status varchar,
  messages jsonb
) language plpgsql as $$
begin
  return query
    select
      c.id,
      c.owner_id,
      c.created_at,
      c.status,
      c.messages
    from
      conversations_view c
    where c.owner_id = auth.uid();
end;
$$;
create
or replace function fetch_support_by_id (support_id uuid) returns table (
  id uuid,
  conversation_id uuid,
  created_at timestamptz,
  status varchar,
  accepted_at timestamptz,
  accepted_by uuid,
  closed_at timestamptz,
  closed_by uuid,
  last_sent_at timestamptz,
  messages jsonb,
  owner_profile jsonb
) language plpgsql as $$
begin
  return query
select
    s.id,
    s.conversation_id,
    s.created_at,
    s.status,
    s.accepted_at,
    s.accepted_by,
    s.closed_at,
    s.closed_by,
    s.last_sent_at,
    s.messages,
    s.owner_profile
from 
    support_view s
where
    s.id = fetch_support_by_id.support_id
    and (
        s.status = 'open'
        or (
        s.accepted_by = auth.uid()
        ) 
    );
end;
$$;
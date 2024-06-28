drop view if exists conversations_view;

create view
  conversations_view as
select
  c.*,
  (
    select
      jsonb_agg(m)
    from
      (
        select
          ai.id,
          ai.conversation_id,
          ai.content,
          ai.created_at,
          'assistant' as role,
          null as owner_profile
        from
          public.ai_messages ai
        where
          ai.conversation_id = c.id
        union
        select
          hm.id,
          hm.conversation_id,
          hm.content,
          hm.created_at,
          hm.role,
          jsonb_build_object(
            'id',
            p.id,
            'email',
            p.email,
            'name',
            p.name,
            'picture',
            p.picture,
            'role',
            p.role
          ) as owner_profile
        from
          public.human_messages hm
          join public.profiles p on hm.owner_id = p.id
        where
          hm.conversation_id = c.id
          and hm.owner_id = c.owner_id
        order by
          created_at
      ) m
  ) as messages
from
  public.conversations c
  join public.profiles p on c.owner_id = p.id;
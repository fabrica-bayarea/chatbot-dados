drop table if exists public.conversations;

create table
  public.conversations (
    id uuid not null default gen_random_uuid (),
    owner_id uuid not null default auth.uid (),
    created_at timestamp with time zone not null default now(),
    status character varying(20) not null default 'open',
    constraint ai_conversations_pkey primary key (id),
    constraint conversations_user_id_fkey foreign key (owner_id) references auth.users (id) on update cascade on delete cascade
  ) tablespace pg_default;

  alter policy "read access"
  on "public"."conversations"
  to authenticated, postgres, supabase_admin
  using (true);

  alter policy "insert access"
  on "public"."conversations"
  to authenticated, postgres, supabase_admin
  with check (true);

-- create trigger after_conversation_status_update before
-- update of status on conversations for each row
-- execute function handle_conversation_status_update ();

drop table if exists public.ai_messages;

create table
  public.ai_messages (
    id uuid not null default gen_random_uuid (),
    conversation_id uuid not null,
    content text not null,
    created_at timestamp with time zone not null default now(),
    feedback character varying(4) null,
    constraint ai_messages_pkey primary key (id),
    constraint ai_messages_conversation_id_fkey foreign key (conversation_id) references conversations (id) on update cascade on delete cascade
  ) tablespace pg_default;

  alter policy "openai read access"
  on "public"."ai_messages"
  to authenticated
  using (true);

  alter policy "insert data"
  on "public"."ai_messages"
  to authenticated
  with check (true);

-- create trigger before_insert_ai_messages before insert on ai_messages for each row
-- execute function upsert_conversation ();

drop table if exists public.human_messages;

create table
  public.human_messages (
    id uuid not null default gen_random_uuid (),
    conversation_id uuid not null,
    owner_id uuid not null default auth.uid (),
    content text not null,
    created_at timestamp with time zone not null default now(),
    role character varying(20) not null,
    constraint human_messages_pkey primary key (id),
    constraint human_messages_conversation_id_fkey foreign key (conversation_id) references conversations (id) on update cascade on delete cascade,
    constraint human_messages_user_id_fkey foreign key (owner_id) references auth.users (id) on update cascade on delete cascade
  ) tablespace pg_default;

  alter policy "read access"
  on "public"."human_messages"
  to authenticated, authenticator, supabase_admin
  using (true);

  alter policy "insert access"
  on "public"."human_messages"
  to authenticated, authenticator, postgres, supabase_admin
  with check (true);

-- create trigger before_insert_human_messages before insert on human_messages for each row
-- execute function upsert_conversation ();

drop table if exists public.profiles;

create table
  public.profiles (
    id uuid not null,
    email character varying(50) not null,
    name character varying(50) not null,
    picture character varying(200) null,
    role character varying(20) not null default 'user',
    constraint profiles_pkey primary key (id),
    constraint profiles_id_fkey foreign key (id) references auth.users (id) on update cascade on delete cascade
  ) tablespace pg_default;

  alter policy "all access"
  on "public"."profiles"
  to authenticated, authenticator, dashboard_user, postgres, service_role, supabase_admin, supabase_auth_admin, supabase_storage_admin
  using (true);

drop table if exists public.support;

create table
  public.support (
    id uuid not null default gen_random_uuid (),
    conversation_id uuid not null,
    created_at timestamp with time zone not null default now(),
    status character varying not null default 'open',
    accepted_at timestamp with time zone null,
    accepted_by uuid null,
    closed_at timestamp with time zone null,
    closed_by uuid null,
    last_sent_at timestamp with time zone null,
    rating numeric null,
    constraint support_pkey primary key (id),
    constraint support_conversation_id_fkey foreign key (conversation_id) references conversations (id) on update cascade on delete cascade,
    constraint support_accepted_by_fkey foreign key (accepted_by) references auth.users (id) on update cascade on delete cascade,
    constraint support_closed_by_fkey foreign key (closed_by) references auth.users (id) on update cascade on delete cascade
  ) tablespace pg_default;

  alter policy "all access"
  on "public"."support"
  to authenticated, authenticator, dashboard_user, postgres, supabase_admin
  using (true);

-- create trigger after_support_status_update before
-- update of status on support for each row
-- execute function handle_support_status_update ();
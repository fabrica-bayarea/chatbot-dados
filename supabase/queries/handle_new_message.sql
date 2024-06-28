create
or replace function upsert_conversation () returns trigger as $$
begin
    insert into conversations (id)
    values (new.conversation_id)
    on conflict (id) do nothing;
    return new;
end;
$$ language plpgsql;

create trigger before_insert_ai_messages before insert on ai_messages for each row
execute function upsert_conversation ();

create trigger before_insert_human_messages before insert on human_messages for each row
execute function upsert_conversation ();
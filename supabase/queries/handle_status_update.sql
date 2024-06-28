create
or replace function handle_conversation_status_update () returns trigger as $$
begin
    if new.status = 'redirected' then
        insert into support (conversation_id)
        values (new.id);
    end if;
    return new;
end;
$$ language plpgsql;

create
or replace function handle_support_status_update () returns trigger as $$
begin
    if new.status = 'accepted' then
        new.accepted_at = now();
        new.accepted_by = auth.uid();
    elsif new.status = 'closed' then
        new.closed_at = now();
        new.closed_by = auth.uid();
    end if;
    return new;
end;
$$ language plpgsql;

create
or replace trigger after_conversation_status_update before
update of status on conversations for each row
execute function handle_conversation_status_update ();

create
or replace trigger after_support_status_update before
update of status on support for each row
execute function handle_support_status_update ();
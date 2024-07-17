create
or replace function public.handle_new_user () returns trigger language plpgsql security definer
set
  search_path = '' as $$
begin
  insert into public.profiles (id, email, name, picture)
  values (
    new.id,
    coalesce(new.email ,''),
    coalesce(new.raw_user_meta_data ->> 'name', 'Anônimo'),
    coalesce(new.raw_user_meta_data ->> 'picture', '')
  );
  return new;
end;
$$;

create trigger on_auth_user_created
after insert on auth.users for each row
execute procedure public.handle_new_user ();
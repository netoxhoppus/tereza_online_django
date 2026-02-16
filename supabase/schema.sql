-- Create table for Tereza Bicuda's chat history
create table if not exists tereza_chat_history (
    id bigint primary key generated always as identity,
    session_id text not null,
    role text not null check (role in ('user', 'assistant', 'system')),
    content text not null,
    created_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Index for faster retrieval by session
create index if not exists idx_tereza_chat_history_session_id on tereza_chat_history(session_id);

-- Optional: Enable Row Level Security (RLS) if you want to restrict access via API
alter table tereza_chat_history enable row level security;

-- Policy to allow anonymous access (if you are using the anon key for backend, 
-- but usually backend uses service_role key which bypasses RLS. 
-- If using anon key, you might need policies like this):
create policy "Allow all operations for anon" on tereza_chat_history for all using (true) with check (true);

-- Recreate the match_documents function with 768 dimensions (for Gemini)
-- FIX: Added table alias 'd' to avoid "column reference 'id' is ambiguous" error.

drop function if exists match_documents(vector(768), float, int);
drop function if exists match_documents(vector(3072), float, int);
drop function if exists match_documents(vector(1536), float, int);

create or replace function match_documents (
  query_embedding vector(768),
  match_threshold float,
  match_count int
)
returns table (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
language plpgsql
as $$
begin
  return query
  select
    d.id,
    d.content,
    d.metadata,
    1 - (d.embedding <=> query_embedding) as similarity
  from documents d
  where 1 - (d.embedding <=> query_embedding) > match_threshold
  order by d.embedding <=> query_embedding
  limit match_count;
end;
$$;

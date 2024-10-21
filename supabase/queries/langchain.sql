-- Enable the pgvector extension to work with embedding vectors
create extension vector;

-- Enable the UUID extension to work with UUIDs
create extension if not exists uuid-ossp; 

-- Create a table to store your documents
create table
  documents (
    id uuid default uuid_generate_v4() primary key, -- unique identifier for the document
    content text, -- corresponds to Document.pageContent
    metadata jsonb, -- corresponds to Document.metadata
    embedding vector (1536) -- 1536 works for OpenAI embeddings, change if needed
  );

-- Create a function to search for documents
create function match_documents (
  query_embedding vector (1536),
  match_count int default null,
  filter jsonb default '{}'
) returns table (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
) language plpgsql as $$
#variable_conflict use_column
begin
  return query
  select
    id,
    content,
    metadata,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where metadata @> filter
  order by documents.embedding <=> query_embedding
  limit match_count;
end;
$$;
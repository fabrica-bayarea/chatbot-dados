import 'dotenv/config';
import { DocxLoader } from '@langchain/community/document_loaders/fs/docx';
import { SupabaseVectorStore } from '@langchain/community/vectorstores/supabase';
import { DirectoryLoader } from 'langchain/document_loaders/fs/directory';
import { TextLoader } from 'langchain/document_loaders/fs/text';
import { OpenAIEmbeddings } from '@langchain/openai';
import { RecursiveCharacterTextSplitter } from '@langchain/textsplitters';
import { createClient } from '@supabase/supabase-js';

try {
  // Load documents
  const loader = new DirectoryLoader('src/data', {
    '.txt': (path) => new TextLoader(path),
    '.docx': (path) => new DocxLoader(path),
  });

  const docs = await loader.load();

  // Split the documents into smaller chunks
  const splitter = new RecursiveCharacterTextSplitter({
    // https://js.langchain.com/v0.1/docs/modules/data_connection/document_transformers/#get-started-with-text-splitters
    chunkSize: 800,
    chunkOverlap: 200,
  });

  const docOutput = await splitter.splitDocuments(docs);

  // Convert to vectors and save in the database
  const client = createClient(process.env.SUPABASE_URL, process.env.SUPABASE_PRIVATE_KEY);

  await SupabaseVectorStore.fromDocuments(docOutput, new OpenAIEmbeddings(), {
    client,
    tableName: 'documents',
    queryName: 'match_documents',
  });

  console.log('Success!');
} catch (error) {
  console.log(error);
}

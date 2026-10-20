-- pgvector adds the `vector` column type and distance operators (<=>, <->, <#>)
-- plus HNSW / IVFFlat indexes. Tables for laws and chunks arrive in M1/M2.
CREATE EXTENSION IF NOT EXISTS vector;

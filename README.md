# MelodicMatch

Swipe-based music recommendation engine built with:

- FastAPI (API layer)
- PySpark (ETL & feature store)
- Parquet (Gold feature layer)
- Vector similarity (upcoming stage)

## Architecture

Bronze → Raw Spotify JSON  
Silver → Structured Parquet  
Gold → Scaled feature vectors  

## Current Status

Stage 1: Spotify OAuth + ingestion ✅  
Stage 2: Spark ETL + feature store ✅  
Stage 3: Swipe-based recommender (in progress)
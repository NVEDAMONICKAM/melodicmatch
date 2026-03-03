from pyspark.sql import SparkSession
from pyspark.sql.functions import col, element_at

spark = SparkSession.builder \
    .appName("MelodicMatch Bronze to Silver") \
    .getOrCreate()

# Load raw liked tracks JSON
df = spark.read.option("multiline", "true").json("data/raw/liked_tracks.json")

# Flatten nested track object
track_df = df.select(
    col("added_at"),
    col("track.*")
)

# Extract primary artist safely (first in array)
track_df = track_df.withColumn(
    "primary_artist",
    element_at(col("artists"), 1)  # Spark arrays are 1-indexed
)

# Extract album cover image (first / largest)
track_df = track_df.withColumn(
    "primary_image",
    element_at(col("album.images"), 1)
)

# Select structured columns
silver_df = track_df.select(
    col("added_at"),
    col("id").alias("track_id"),
    col("name").alias("track_name"),
    col("duration_ms"),
    col("explicit"),
    col("disc_number"),
    col("track_number"),
    col("is_playable"),

    # Album fields
    col("album.id").alias("album_id"),
    col("album.name").alias("album_name"),
    col("album.release_date").alias("album_release_date"),
    col("album.release_date_precision").alias("album_release_precision"),
    col("album.total_tracks").alias("album_total_tracks"),
    col("album.album_type").alias("album_type"),

    # Artist fields
    col("primary_artist.id").alias("primary_artist_id"),
    col("primary_artist.name").alias("primary_artist_name"),

    # Image
    col("primary_image.url").alias("album_cover_url")
)

# Remove local tracks and null IDs
silver_df = silver_df.filter(
    (col("track_id").isNotNull()) &
    (col("is_playable") == True)
)

# Drop duplicates
silver_df = silver_df.dropDuplicates(["track_id"])

# Save Silver table
silver_df.write.mode("overwrite").parquet("data/processed/silver_tracks.parquet")

print("Bronze → Silver complete.")


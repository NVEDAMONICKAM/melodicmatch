from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, to_date, current_date, datediff
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml import Pipeline

spark = SparkSession.builder \
    .appName("MelodicMatch Silver to Gold (Minimal No Popularity)") \
    .getOrCreate()

df = spark.read.parquet("data/processed/silver_tracks.parquet")

# --- Feature Engineering ---

# Release year
df = df.withColumn(
    "release_year",
    year(to_date(col("album_release_date")))
)

# Duration seconds
df = df.withColumn(
    "duration_seconds",
    col("duration_ms") / 1000
)

# Explicit flag
df = df.withColumn(
    "explicit_flag",
    col("explicit").cast("int")
)

# Track position ratio
df = df.withColumn(
    "track_position_ratio",
    col("track_number") / col("album_total_tracks")
)

# Recency (years since added)
df = df.withColumn(
    "added_date",
    to_date(col("added_at"))
)

df = df.withColumn(
    "recency_years",
    datediff(current_date(), col("added_date")) / 365
)

feature_cols = [
    "duration_seconds",
    "release_year",
    "album_total_tracks",
    "explicit_flag",
    "track_position_ratio",
    "recency_years"
]

df = df.dropna(subset=feature_cols)

assembler = VectorAssembler(
    inputCols=feature_cols,
    outputCol="raw_features"
)

scaler = StandardScaler(
    inputCol="raw_features",
    outputCol="features",
    withMean=True,
    withStd=True
)

pipeline = Pipeline(stages=[assembler, scaler])
model = pipeline.fit(df)

gold_df = model.transform(df)

final_df = gold_df.select("track_id", "features")

final_df.write.mode("overwrite").parquet("data/features.parquet")

print("Silver → Gold complete (Minimal, no popularity).")

df = spark.read.parquet("data/features.parquet")
df.show(5)

row = df.first()
print(row.features)
print(len(row.features))
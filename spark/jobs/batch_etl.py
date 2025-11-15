import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from dq import validators


def get_spark(app_name: str) -> SparkSession:
    return (
        SparkSession.builder.appName(app_name)
        .config("spark.sql.shuffle.partitions", os.getenv("SPARK_SHUFFLE_PARTITIONS", "200"))
        .getOrCreate()
    )


def main() -> None:
    input_path = os.getenv("INPUT_PATH", "s3://bucket/raw/sample.csv")
    output_path = os.getenv("OUTPUT_PATH", "/tmp/out/parquet")

    spark = get_spark("data-platform-batch-etl")

    # Placeholder input schema (adjust in production)
    df = spark.read.option("header", True).csv(input_path)
    df = df.withColumn("value_times_two", F.col("value").cast("double") * 2)

    # Data quality checks
    dq_results = {
        **validators.run_standard_checks(df),
        **dict([validators.validate_not_null(df, ["id"])])
    }
    print({"dq": dq_results})

    # Write output
    (
        df.repartition(1)
        .write.mode("overwrite")
        .parquet(output_path)
    )

    spark.stop()


if __name__ == "__main__":
    main()



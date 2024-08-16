"""
cmd to download packages manually
    bin ./pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1
"""

import pyspark.sql.functions as F
from pyspark.sql import SparkSession
from pyspark.sql.types import (
    ArrayType,
    FloatType,
    IntegerType,
    StringType,
    StructField,
    StructType,
)

SPARK_MASTER = "spark://localhost:7077"
KAFKA_BOOTSTRAP_SERVER = "localhost:9092"
TOPIC = "quickstart-events"


schema = StructType(
    [
        StructField(
            "customer",
            StructType(
                [
                    StructField(
                        "name", StringType(), True
                    ),  # Allow null values
                    StructField("email", StringType(), True),
                   StructField("address", StringType(), True),
                ]
            ),
            True,
        ),  # Allow null values for the entire "customer" struct
        StructField("order_id", IntegerType(), True),
        StructField(
            "items",
            ArrayType(
                StructType(
                    [
                        StructField("name", StringType(), True),
                        StructField("price", FloatType(), True),
                        StructField("quantity", IntegerType(), True),
                    ]
                )
            ),
           True,
        ),  # Allow null values for the "items" array
    ]
)

if __name__ == "__main__":

    spark: SparkSession = (
        SparkSession.builder.appName("Data Engineering")
        .master(SPARK_MASTER)
        .config("spark.streaming.stopGracefullyOnShutdown", "true")
        .getOrCreate()
    )

    df = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVER)
        .option("subscribe", TOPIC)
        .option("startingOffsets", "earliest")
        .load()
    )
    json_df = df.withColumn(
        "value_json", F.col("value").cast("string")
    ).withColumn(
        "value_parsed",
        F.from_json(F.col("value_json"), schema=schema),
    )
    query = (
        json_df.selectExpr(
            "CAST(key AS STRING)", "value_parsed"
        )  # Select key and parsed JSON
        .writeStream.format("console")
        .option("truncate", False)  # Prevent truncation for better readability
        .start()
    )

    query.awaitTermination()
#

import os
import logging

import pyspark.sql.functions as F
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName('ingest_data')
    .config(
        'spark.jars.packages',
        'org.postgresql:postgresql:42.2.25')
    .getOrCreate()
)
spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")

db_user = os.environ["POSTGRES_USER"]
db_password = os.environ["POSTGRES_PASSWORD"]
logging.basicConfig(level=logging.INFO)

############################## SENSORS LOG ####################################
logging.info("writing table: sensors_log")
sensors_log = spark.read.csv("/opt/spark-data/equipment_failure_sensors.log", sep="\t")
sensors_log = (
    sensors_log
    .withColumn("_c0", F.to_timestamp(F.col("_c0"), "[yyyy-MM-dd HH:mm:ss]"))
    .withColumn("_c2", F.regexp_extract(F.col("_c2"), "sensor\[(\d*)\]:", 1) )
    .withColumn("_c4", F.regexp_extract(F.col("_c4"), "-?\d*\.?\d*", 0) )
    .withColumn("_c5", F.regexp_extract(F.col("_c5"), "-?\d*\.?\d*", 0) )
).select(
    F.col("_c0").alias("event_date").cast("timestamp")
    ,F.col("_c1").alias("status").cast("string")
    ,F.col("_c2").alias("sensor_id").cast("integer")
    ,F.col("_c4").alias("temperature").cast("numeric")
    ,F.col("_c5").alias("vibration").cast("numeric")
)

(
    sensors_log
    .write
    .jdbc(
        "jdbc:postgresql://172.19.0.6:5432/shape",
        "shape.sensors_log",
        mode="append",
        properties={"user": db_user, "password": db_password,
                    "driver": "org.postgresql.Driver"}
    )
)
############################## SENSORS LOG ####################################

########################### EQUIPAMENT SENSORS ################################
logging.info("writing table: equipment_sensors")
(
    spark.read.csv("/opt/spark-data/equipment_sensors.csv", sep=";", header=True)
    .select(
        F.col("equipment_id").cast("integer"),
        F.col("sensor_id").cast("integer")
    )
    .write
    .jdbc(
        "jdbc:postgresql://172.19.0.6:5432/shape",
        "shape.equipment_sensors",
        mode="append",
        properties={"user": db_user, "password": db_password,
                    "driver": "org.postgresql.Driver"}
    )
)
########################### EQUIPAMENT SENSORS ################################

########################### EQUIPAMENT GROUP ##################################
logging.info("writing table: equipament_group")
(
    spark.read.json("/opt/spark-data/equipment.json", multiLine=True)
    .write
    .jdbc(
        "jdbc:postgresql://172.19.0.6:5432/shape",
        "shape.equipment_group",
        mode="append",
        properties={"user": db_user, "password": db_password,
                    "driver": "org.postgresql.Driver"}
    )
)
########################### EQUIPAMENT GROUP ##################################

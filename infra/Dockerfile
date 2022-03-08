FROM ubuntu:18.04

# Add Dependencies for PySpark
RUN apt-get update && apt-get install -y wget software-properties-common python3 python3-pip default-jdk
RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1

# Fix the value of PYTHONHASHSEED
ENV SPARK_VERSION=3.0.2 \
HADOOP_VERSION=3.2 \
SPARK_HOME=/opt/spark \
PYTHONHASHSEED=1

# Download and uncompress spark from the apache archive
RUN wget --no-verbose -O apache-spark.tgz "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
&& mkdir -p /opt/spark \
&& tar -xf apache-spark.tgz -C /opt/spark --strip-components=1 \
&& rm apache-spark.tgz

# install python packages
RUN pip3 install pyspark

# Define paths
KAFKA_HOME := /opt/kafka
ZOOKEEPER_HOME := /opt/kafka

TOPIC_NAME := quickstart-events
TOPIC_RETRIES := quickstart-events-retries
TOPIC_DLQ := quickstart-events-DLQ

BOOTSTRAP_SERVER := localhost:9092

# Define commands
ZOOKEEPER_START := $(ZOOKEEPER_HOME)/bin/zookeeper-server-start.sh $(ZOOKEEPER_HOME)/config/zookeeper.properties
KAFKA_START := $(KAFKA_HOME)/bin/kafka-server-start.sh $(KAFKA_HOME)/config/server.properties


SPARK_HOME := /opt/spark
SPARK_HOST := spark://MacBook-Pro-cua-Thuy.local:7077 

zookeeper:
	$(ZOOKEEPER_START)

kafka:
	$(KAFKA_START)

producer:
	$(KAFKA_HOME)/bin/kafka-console-producer.sh --topic $(TOPIC_NAME) --bootstrap-server $(BOOTSTRAP_SERVER)

consumer:
	$(KAFKA_HOME)/bin/kafka-console-consumer.sh --topic $(TOPIC_NAME) --bootstrap-server $(BOOTSTRAP_SERVER)

topic-create:
	$(KAFKA_HOME)/bin/kafka-topics.sh --create --topic $(TOPIC_NAME) --bootstrap-server $(BOOTSTRAP_SERVER)

topic-create-retries:
	$(KAFKA_HOME)/bin/kafka-topics.sh --create --topic $(TOPIC_RETRIES) --bootstrap-server $(BOOTSTRAP_SERVER)

topic-create-dlq:
	$(KAFKA_HOME)/bin/kafka-topics.sh --create --topic $(TOPIC_DLQ) --bootstrap-server $(BOOTSTRAP_SERVER)

spark-master:
	$(SPARK_HOME)/sbin/start-master.sh

spark-worker:
	$(SPARK_HOME)/sbin/start-worker.sh $(SPARK_HOST)

spark-start:
	$(SPARK_HOME)/sbin/start-master.sh
	$(SPARK_HOME)/sbin/start-worker.sh $(SPARK_HOST)

spark-stop:
	$(SPARK_HOME)/sbin/stop-worker.sh
	$(SPARK_HOME)/sbin/stop-master.sh

consumer-spark-app:
	$(SPARK_HOME)/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 ./src/spark_consumer.py

consumer-python-app:
	python ./src/python_consumer.py

clean: 
	$(RM) $(KAFKA_HOME)/logs/* $(ZOOKEEPER_HOME)/logs/*


# ETL with Apache Spark 

Project description:

   This project aims to obtain data from a certain subset of a bank's customers, in order to make marketing decisions regarding them. Their data is 
   distributed in two databases. 
      For this, an ETL process will be implemented, which consists of extracting the information from these sources (using pyspark), joining them, and
    determining the number of clients by geographic area and gender, as well as the number of products contracted in these groups. 
	 One condition is that the customers' Score must be greater than 500. And the number of products in the group (resulting) must be less than 1900.
      The result (csv) of the ETL process will be saved in the /data/output path. 

Elements that interact with the ETL Process (Docker) :
  1) PostgreSQL Database.
  2) MongoDb Database.
  3) Cluster with Apache Spark.

Steps to be able to execute the ETL process:

Pre requirements

Docker installed.

Docker Compose installed.

Build the spark cluster image: (go to the root of the project)

Run by command line (takes 15-20 minutes):

   docker build -t cluster-apache-spark:3.0.2 .
   
Docker Compose :
 Run by command line:

   docker-compose up -d

Cluster validation:

Spark Master
http://localhost:9090/

Spark Worker 1
http://localhost:9091/

Spark Worker 2
http://localhost:9092/


Access the master container of the Spark cluster:

docker exec -it master_container bash

Locate in the bin folder

cd bin

Execute the ETL process by command line with the following instruction (previously located in spark/bin):

spark-submit --master spark://spark-master:7077 --packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.1,org.postgresql:postgresql:42.0.0  /opt/spark-apps/etl.py 

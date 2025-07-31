# Simulated EMR Data Integration & Analysis with Hadoop and HiveQL

## Project Summary: 
This project simulates Electronic Medical Record (EMR) data in a FHIR-like JSON format (unstructured data) and builds an ETL pipeline to extract, normalize, and load the data into a Hadoop ecosystem. The pipeline flattens nested JSON using Python, converts it to a relational format (CSV), stores it in HDFS, and defines an external Hive table for querying. HiveQL is then used to perform exploratory data analysis (EDA) on patient demographics and other clinical attributes.


```
# Start pre-confiugred Hadoop + Hive stack
# Open Windows PowerShell and type the following command:
docker-compose up -d
```


```
# Copy transformed data into Hive server
docker cp path\to\EMR_simulated.csv hive-server:/EMR_simulated.csv
```

```
# Access Hive CLI (Beeline):
docker exec -it hive-server /bin/bash
```


```
# Start Beeline (Hive CLI):
beeline -u jdbc:hive2://localhost:10000
```

```
# Upload CSV file to HFDS:
hfds dfs -mkdir -p /user/hive/warehouse/EMR_simulated

hfds dfs -put /EMR_simulated.csv /user/hive/warehouse/EMR_simulated/
```

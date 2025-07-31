# Simulated EMR Data Integration & Analysis with Hadoop and HiveQL

## Project Summary: 
This project simulates Electronic Medical Record (EMR) data in a FHIR-like JSON format (unstructured data) and builds an ETL pipeline to extract, normalize, and load the data into a Hadoop ecosystem. The pipeline flattens nested JSON using Python, converts it to a relational format (CSV), stores it in HDFS, and defines an external Hive table for querying. HiveQL is then used to perform exploratory data analysis (EDA) on patient demographics and other clinical attributes.

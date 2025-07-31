# Simulated EMR Data Integration & Analysis with Hadoop and HiveQL

## Project Summary: 
This project simulates Electronic Medical Record (EMR) data in a FHIR-like JSON format (unstructured data) and builds an ETL pipeline to extract, normalize, and load the data into a Hadoop ecosystem. The pipeline flattens nested JSON using Python, converts it to a relational format (CSV), stores it in HDFS, and defines an external Hive table for querying. HiveQL is then used to perform exploratory data analysis (EDA) on patient demographics and other clinical attributes. EMR data will be simulated using Synthea which is designed specifically for simulating realistic, synthetic EMR data using using clincal workflows, population distributions, and coding standards (ICD-10, LOINC, SNOMED, RxNorm). Synthea will generate:
1. Realistic clinical encounters (simulates entire patient lifecycles, visits, diagnoses, procedures, and medications)
2. Standard coding (Uses ICD-10, LOINC, RxNorm, and SNOMED)
3. Population diversity (Age, race, gender, insurance, social determinants)
4. Output formats (CSV, FHIR, JSON, HL7, CCDA)
5. Time-series (Longitudinal encounter data per patient)

## Getting started with Synthea:
```
# Install Synthea (Java required)
git clone https://github.com/synthetichealth/synthea.git
cd synthea
./gradlew build check test
```


### Types of normalization for EMR data:
1. Schema (Relational) Normalization
   - Goal: Eliminate redundancy and maintain data integrity.
     1. Remove duplicated values
     2. Separate patient info, encounters, diagnoses, labs, medications, etc.
     3. Abstract lookups like gender codes, medication names, and diagnosis codes into separate reference tables.
2. Feature (Statistical) Normalization
   - Goal: Make numeric data suitable for modeling or analysis.
     1. Use z-score normalization for continuous variables.
     2. Applied to:
        1. Lab test values (e.g., glucose, cholesterol)
        2. Vitals (e.g., heart rate, weight)
        3. Age, BMI, or derived features
3. Categorical Normalization
   - Goal: Standardize code systems and text values.
     1. Map diagnoses to ICD-10, procedures to CPT, labs to LOINC, and medications to RxNorm
     2. Normalize gender to standard codes (e.g., M, F, O)
     3. Clean text (e.g., title casing names, removing typos)
  
    

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

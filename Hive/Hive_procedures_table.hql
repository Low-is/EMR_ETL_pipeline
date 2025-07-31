CREATE EXTERNAL TABLE IF NOT EXISTS emr_procedures (
  id STRING,
  patient_id STRING,
  encounter_id STRING,
  procedure_code STRING,
  procedure_description STRING,
  performed_date TIMESTAMP
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/emr_data/procedures/';

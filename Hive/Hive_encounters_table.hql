CREATE EXTERNAL TABLE emr_encounters (
  id STRING,
  start STRING,
  stop STRING,
  patient STRING,
  organization STRING,
  provider STRING,
  payer STRING,
  encounterclass STRING,
  code STRING,
  description STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/emr_data/encounters'
TBLPROPERTIES ("skip.header.line.count"="1");

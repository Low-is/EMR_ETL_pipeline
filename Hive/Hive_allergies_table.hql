CREATE EXTERNAL TABLE emr_allergies (
  id STRING,
  patient STRING,
  encounter STRING,
  start STRING,
  stop STRING,
  code STRING,
  description STRING,
  type STRING,
  category STRING,
  reaction1 STRING,
  reaction2 STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/emr_data/allergies'
TBLPROPERTIES ("skip.header.line.count"="1");

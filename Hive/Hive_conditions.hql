CREATE EXTERNAL TABLE emr_conditions (
  id STRING,
  start STRING,
  stop STRING,
  patient STRING,
  encounter STRING,
  code STRING,
  description STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/emr_data/conditions'
TBLPROPERTIES ("skip.header.line.count"="1");

CREATE EXTERNAL TABLE emr_medications (
  id STRING,
  start STRING,
  stop STRING,
  patient STRING,
  payer STRING,
  encounter STRING,
  code STRING,
  description STRING,
  base_cost DOUBLE,
  payer_coverage DOUBLE,
  dispenses INT,
  total_cost DOUBLE,
  reasoncode STRING,
  reason_description STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/emr_data/medications'
TBLPROPERTIES ("skip.header.line.count"="1");

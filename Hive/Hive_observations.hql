CREATE EXTERNAL TABLE emr_observations (
  id STRING,
  date STRING,
  patient STRING,
  encounter STRING,
  code STRING,
  description STRING,
  value STRING,
  units STRING,
  type STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/emr_data/observations'
TBLPROPERTIES ("skip.header.line.count"="1");

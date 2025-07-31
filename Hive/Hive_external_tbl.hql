CREATE EXTERNAL TABLE emr_patients (
  id STRING,
  family_name STRING,
  given_name_1 STRING,
  given_name_2 STRING,
  birth_date STRING,
  gender STRING,
  phone STRING,
  email STRING,
  city STRING,
  postal_code STRING
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/emr_data'
TBLPROPERTIES ("skip.header.line.count"="1");

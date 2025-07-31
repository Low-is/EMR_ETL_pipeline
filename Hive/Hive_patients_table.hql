CREATE EXTERNAL TABLE emr_patients (
  id STRING,
  birthdate STRING,
  deathdate STRING,
  ssn STRING,
  drivers STRING,
  passport STRING,
  prefix STRING,
  first STRING,
  last STRING,
  suffix STRING,
  maiden STRING,
  marital STRING,
  race STRING,
  ethnicity STRING,
  gender STRING,
  birthplace STRING,
  address STRING,
  city STRING,
  state STRING,
  county STRING,
  zip STRING,
  lat DOUBLE,
  lon DOUBLE,
  healthcare_expenses DOUBLE,
  healthcare_coverage DOUBLE
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hive/warehouse/emr/patients'
TBLPROPERTIES ("skip.header.line.count"="1");

 -- Count total patients
SELECT COUNT(*) FROM emr_patients;

-- Gender distribution
SELECT gender, COUNT(*) AS count FROM emr_patients GROUP BY gender;

-- City-level patient count
SELECT city, COUNT(*) AS patient_count FROM emr_patients GROUP BY city;

-- Age analysis 
SELECT birth_data, YEAR(FROM_UNIXTIME(UNIX_TIMESTAMP())) - YEAR(TO_DATE(birth_date)) AS age
FROM emr_patients;

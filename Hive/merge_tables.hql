CREATE TABLE emr_flat AS
SELECT
  p.id AS patient_id,
  p.birthdate,
  p.gender,
  e.id AS encounter_id,
  e.date AS encounter_date,
  c.code AS condition_code,
  m.code AS med_code,
  o.code AS obs_code,
  o.value AS obs_value
FROM emr_patients p
LEFT JOIN emr_encounters e ON p.id = e.patient
LEFT JOIN emr_conditions c ON e.id = c.encounter
LEFT JOIN emr_medications m ON e.id = m.encounter
LEFT JOIN emr_observations o ON e.id = o.encounter;

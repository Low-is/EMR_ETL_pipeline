import json
import pandas as pd
import os
from glob import glob

# -----------------------------
# 0. Setup paths
# -----------------------------
FHIR_FOLDER = r"C:\Users\RANDOLPHL\Documents\Predicting_30day_readmission_and_mortality_for_CV_events\docker_output\fhir"
OUTPUT_FOLDER = r"C:\Users\RANDOLPHL\Documents\Predicting_30day_readmission_and_mortality_for_CV_events\docker_output\csv"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -----------------------------
# 1. Helper function for nested dicts
# -----------------------------
def get_nested(d, keys, default=None):
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d

# -----------------------------
# 2. Flatten Patients
# -----------------------------
patient_records = []

for filepath in glob(os.path.join(FHIR_FOLDER, "Patient-*.json")):
    try:
        with open(filepath) as f:
            patient = json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        continue

    name = patient.get("name", [{}])[0]
    address = patient.get("address", [{}])[0]
    telecom = patient.get("telecom", [])

    record = {
        "patient_id": patient.get("id"),
        "family_name": get_nested(name, ["family"]),
        "given_name_1": get_nested(name, ["given", 0]),
        "given_name_2": get_nested(name, ["given", 1]),
        "birth_date": patient.get("birthDate"),
        "gender": patient.get("gender"),
        "phone": next((x.get("value") for x in telecom if x.get("system") == "phone"), None),
        "email": next((x.get("value") for x in telecom if x.get("system") == "email"), None),
        "city": get_nested(address, ["city"]),
        "state": get_nested(address, ["state"]),
        "postal_code": get_nested(address, ["postalCode"]),
        "country": get_nested(address, ["country"]),
        "death_date": patient.get("deceasedDateTime"),
        "died": int(patient.get("deceasedDateTime") is not None)
    }
    patient_records.append(record)

df_patients = pd.DataFrame(patient_records)
df_patients.to_csv(os.path.join(OUTPUT_FOLDER, "patients_flat.csv"), index=False)
print(f"Saved {len(df_patients)} patients.")

# -----------------------------
# 3. Flatten Encounters
# -----------------------------
encounter_records = []
for filepath in glob(os.path.join(FHIR_FOLDER, "Encounter-*.json")):
    try:
        with open(filepath) as f:
            enc = json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        continue

    record = {
        "encounter_id": enc.get("id"),
        "patient_id": get_nested(enc, ["subject", "reference"], "").replace("Patient/", ""),
        "start": enc.get("period", {}).get("start"),
        "stop": enc.get("period", {}).get("end"),
        "type": get_nested(enc, ["type", 0, "coding", 0, "code"]),
        "class": get_nested(enc, ["class", "code"])
    }
    encounter_records.append(record)

df_encounters = pd.DataFrame(encounter_records)
df_encounters.to_csv(os.path.join(OUTPUT_FOLDER, "encounters_flat.csv"), index=False)
print(f"Saved {len(df_encounters)} encounters.")

# -----------------------------
# 4. Flatten Conditions
# -----------------------------
condition_records = []
for filepath in glob(os.path.join(FHIR_FOLDER, "Condition-*.json")):
    try:
        with open(filepath) as f:
            cond = json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        continue

    coding = get_nested(cond, ["code", "coding", 0], {})
    record = {
        "condition_id": cond.get("id"),
        "patient_id": get_nested(cond, ["subject", "reference"], "").replace("Patient/", ""),
        "encounter_id": get_nested(cond, ["encounter", "reference"], "").replace("Encounter/", ""),
        "condition_code": coding.get("code"),
        "condition_description": coding.get("display"),
        "onset_date": cond.get("onsetDateTime")
    }
    condition_records.append(record)

df_conditions = pd.DataFrame(condition_records)
df_conditions.to_csv(os.path.join(OUTPUT_FOLDER, "conditions_flat.csv"), index=False)
print(f"Saved {len(df_conditions)} conditions.")

# -----------------------------
# 5. Flatten Procedures
# -----------------------------
procedure_records = []
for filepath in glob(os.path.join(FHIR_FOLDER, "Procedure-*.json")):
    try:
        with open(filepath) as f:
            proc = json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        continue

    coding = get_nested(proc, ["code", "coding", 0], {})
    record = {
        "procedure_id": proc.get("id"),
        "patient_id": get_nested(proc, ["subject", "reference"], "").replace("Patient/", ""),
        "encounter_id": get_nested(proc, ["encounter", "reference"], "").replace("Encounter/", ""),
        "procedure_code": coding.get("code"),
        "procedure_description": coding.get("display"),
        "performed_date": proc.get("performedDateTime")
    }
    procedure_records.append(record)

df_procedures = pd.DataFrame(procedure_records)
df_procedures.to_csv(os.path.join(OUTPUT_FOLDER, "procedures_flat.csv"), index=False)
print(f"Saved {len(df_procedures)} procedures.")

# -----------------------------
# 6. Feature Engineering Example
# -----------------------------
# Age at first encounter
df_patients["birth_date"] = pd.to_datetime(df_patients["birth_date"])
df_encounters["start"] = pd.to_datetime(df_encounters["start"])
first_encounter = df_encounters.groupby("patient_id")["start"].min().reset_index()
df_patients = df_patients.merge(first_encounter, left_on="patient_id", right_on="patient_id", how="left")
df_patients["age_at_first_encounter"] = (df_patients["start"] - df_patients["birth_date"]).dt.days // 365

# Number of conditions per patient
df_patients["num_conditions"] = df_conditions.groupby("patient_id").size().reindex(df_patients["patient_id"]).fillna(0).astype(int)

# Number of procedures per patient
df_patients["num_procedures"] = df_procedures.groupby("patient_id").size().reindex(df_patients["patient_id"]).fillna(0).astype(int)

# Save enriched patient table
df_patients.to_csv(os.path.join(OUTPUT_FOLDER, "patients_features.csv"), index=False)
print("Saved patients_features.csv with enriched attributes.")

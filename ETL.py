import json
import pandas as pd
import os
from glob import glob


# -----------------------------
# Loading json files 
# -----------------------------

with open("patients.json") as f:
    raw = json.load(f)

records_json = []
for patient_json in raw:
    record = {
        "id": patient_json["id"],
        "family_name": patient_json["name"]["family"],
        "given_name_1": patient_json["name"]["given"][0],
        "given_name_2": patient_json["name"]["given"][1] if len(patient_json["name"]["given"]) > 1 else None,
        "birth_date": patient_json["birthDate"],
        "gender": patient_json["gender"],
        "phone": next((x["value"] for x in patient_json["telecom"] if x["system"] == "phone"), None),
        "email": next((x["value"] for x in patient_json["telecom"] if x["system"] == "email"), None),
        "city": patient_json["address"]["city"],
        "postal_code": patient_json["address"]["postalCode"]
    }
    records_json.append(record)

df_json = pd.DataFrame(records_json)
df_json.to_csv("patients_flat.csv", index=False)



# -----------------------------
# Loading FHIR files 
# -----------------------------
# Folder containing FHIR Patient JSON files (e.g., output/fhir/)
FHIR_FOLDER = "output/fhir/"

records_FHIR = []

for filepath in glob(os.path.join(FHIR_FOLDER, "Patient-*.json")):
    try:
        with open(filepath) as f:
            patient_FHIR = json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        continue
        

    # Extract patient fields safely
    name = patient_FHIR.get("name", [{}])[0]
    address = patient_FHIR.get("address", [{}])[0]
    telecom = patient_FHIR.get("telecom", [])

    record = {
        "id": patient_FHIR.get("id"),
        "family_name": name.get("family"),
        "given_name_1": name.get("given", [None])[0],
        "given_name_2": name.get("given", [None, None])[1] if len(name.get("given", [])) > 1 else None,
        "birth_date": patient_FHIR.get("birthDate"),
        "gender": patient_FHIR.get("gender"),
        "phone": next((x.get("value") for x in telecom if x.get("system") == "phone"), None),
        "email": next((x.get("value") for x in telecom if x.get("system") == "email"), None),
        "city": address.get("city"),
        "postal_code": address.get("postalCode"),
        "state": address.get("state"),
        "country": address.get("country")
    }

    records_FHIR.append(record)

# Create and export DataFrame
df_fhir = pd.DataFrame(records_FHIR)
df_fhir.to_csv("patients_flat_fhir.csv", index=False)

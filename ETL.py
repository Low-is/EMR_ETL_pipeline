import json
import pandas as pd

with open("patients.json") as f:
    raw = json.load(f)

records = []
for patient in raw:
    record = {
        "id": patient["id"],
        "family_name": patient["name"]["family"],
        "given_name_1": patient["name"]["given"][0],
        "given_name_2": patient["name"]["given"][1] if len(patient["name"]["given"]) > 1 else None,
        "birth_date": patient["birthDate"],
        "gender": patient["gender"],
        "phone": next((x["value"] for x in patient["telecom"] if x["system"] == "phone"), None),
        "email": next((x["value"] for x in patient["telecom"] if x["system"] == "email"), None),
        "city": patient["address"]["city"],
        "postal_code": patient["address"]["postalCode"]
    }
    records.append(record)

df = pd.DataFrame(records)
df.to_csv("patients_flat.csv", index=False)

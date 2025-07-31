import pandas as pd

# Load all CSVs
patients = pd.read_csv(r"path\to\patients.csv")
encounters = pd.read_csv(r"path\to\encounters.csv")
conditions = pd.read_csv(r"path\to\conditions.csv")
meds = pd.read_csv(r"path\to\medications.csv")
obs = pd.read_csv(r"path\to\observations.csv")

# Merge step by step
df = encounters.merge(patients, left_on="patient", right_on="Id", how="left")\
               .merge(conditions, on="encounter", how="left")\
               .merge(meds, on="encounter", how="left")\
               .merge(obs, on="encounter", how="left")

df.to_csv("flat_emr.csv", index=False)

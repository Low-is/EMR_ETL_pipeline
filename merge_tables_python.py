import pandas as pd

base = r"C:\Users\RANDOLPHL\Documents\Predicting_30day_readmission_and_mortality_for_CV_events\docker_output\csv"

####################################
# LOADING DATA FROM OUTPUT DIRECTORY 
####################################
patients = pd.read_csv(f"{base}/patients.csv")
encounters = pd.read_csv(f"{base}/encounters.csv")
conditions = pd.read_csv(f"{base}/conditions.csv")
procedures = pd.read_csv(f"{base}/procedures.csv")
observations = pd.read_csv(f"{base}/observations.csv")



####################################
# MORTALITY OUTCOME 
####################################
patients["died"] = patients["DEATHDATE"].notnull().astype(int)
mortality_rate = patients["died"].mean()

print(f"Mortality rate: {mortality_rate: .2%}")


####################################
# 30-Day Readmission
####################################
encounters["START"] = pd.to_datetime(encounters["START"])
encounters = encounter.sort_values(["PATIENT", "START"])



####################################
# Identify Readmission (creating function)
####################################
def has_30d_readmit(group):
    group = group.sort_values("START")
    readmit = [0] * len(group)
    for i in range(len(group)-1):
        delta = (group.iloc[i+1]["START"] - group.iloc[i]["STOP"]).days
        if 0 < delta <= 30:
            readmit[i] = 1
    group["readmit_30d"] = readmit
    return group


encounters = encounters.groupby("PATIENT").apply(has_30d_readmit)




####################################
# Calculate readmission day
####################################
readmission_rate = encounters["readmit_30d"].mean()
print(f"30-day readmission rate: {readmission_rate:.2%}")

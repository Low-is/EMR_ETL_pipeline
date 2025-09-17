import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, classification_report


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
# CARDIOVASCULAR EVENT PATIENTS 
####################################
cv_conditions = conditions[
    conditions["DESCRIPTON"].str.lower().str.contains(
        "ischemic|heart failure|stroke"
    )
]

cv_patients = cv_conditions["PATIENT"].unique()

# Subset encounters and patients for these CV patients
encounters_cv = encounters[encounters["PATIENT"].isin(cv_patients)]
patients_cv = patients[patients["Id"].isin(cv_patients)]



####################################
# MORTALITY OUTCOME 
####################################
patients_cv["died"] = patients_cv["DEATHDATE"].notnull().astype(int)
mortality_rate = patients_cv["died"].mean()

print(f"Mortality rate: {mortality_rate: .2%}")


####################################
# 30-DAY READMISSION
####################################
encounters_cv["START"] = pd.to_datetime(encounters_cv["START"])
encounters_cv = encounters_cv.sort_values(["PATIENT", "START"])



####################################
# IDENTIFY READMISSION (CREATING FUNCTION)
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


encounters_cv = encounters_cv.groupby("PATIENT").apply(has_30d_readmit)




####################################
# CALCULATE READMISSION DAY
####################################
readmission_rate = encounters_cv["readmit_30d"].mean()
print(f"30-day readmission rate: {readmission_rate:.2%}")



####################################
# PREPARING FOR MODELING/ANALYSIS
####################################
# Get first readmission per patient (or max)
readmit_flags = encounters_cv.groupby("PATIENT")["readmit_30d"].max().reset_index()

patients_cv_summary = patients_cv.merge(readmit_flags, left_on="Id", right_on="PATIENT", how="left")

# Fill NaNs with 0 if patient had no readmissions
patients_cv_summary["readmit_30d"] = patients_cv_summary["readmit_30d"].fillna(0).astype(int)

# Feature engineering
patients_cv_summary["num_conditions"] = conditions[conditions["PATIENT"].isin(cv_patients)].groupby("PATIENT").size().reindex(patients_cv_summary["Id"]).fillna(0)



####################################
# EDA
####################################
# Showing distribution of age, gender, and other covariates
# Mortality rate and readmission rate stratified by age, gender, and comorbidities

sns.histplot(patients_cv_summary["AGE"])
plt.show()

sns.barplot(x="GENDER", y="died", data=patients_cv_summary)
plt.show()




####################################
# PREDICTIVE MODELING
####################################
# Building a random forest model to predict:
# 30-day readmission: (1 = readmitted within 30 days, 0 = not)
# Mortality

X = patients_cv_summary[["AGE", "num_conditions"]]  # add more features as needed
y = patients_cv_summary["readmit_30d"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf = RandomForestClassifier()
rf.fit(X_train, y_train)
y_pred = rf.predict(X_test)

print(classification_report(y_test, y_pred))

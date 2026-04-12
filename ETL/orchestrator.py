import glob
import os
import subprocess

scriptdir="/home/aymanfen/Desktop/BankAnalytics/ETL"
files = glob.glob("/home/aymanfen/Desktop/BankAnalytics/Reports/Excel/*.xlsx")

for file in files:
    filename = os.path.basename(file)
    subprocess.run(["python", f"{scriptdir}/Cleaning.py", filename])

files = glob.glob("/home/aymanfen/Desktop/BankAnalytics/Reports/Cleaned/*.xlsx")

for file in files:
    filename = os.path.basename(file)
    subprocess.run(["python", f"{scriptdir}/Ingestion.py", filename])
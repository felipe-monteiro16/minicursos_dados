from curl_cffi import requests
from pathlib import Path
import pandas as pd

url = "https://dados.ons.org.br/api/3/action/package_show?id=cvu-usitermica" # trocar a base para uma mais leve
SOURCE_RAW_PATH = Path("data/cvu-usitermica/source_raw")
RAW_PATH = Path("data/cvu-usitermica/raw")


# # ===== extract ========================
response = requests.get(url, impersonate="chrome")
response.raise_for_status()

resources = response.json()["result"]["resources"]

paths = []
for item in resources:
    if item["format"] != "CSV":
        continue

    year = item["name"].split("-")[2]    

    SOURCE_RAW_PATH.mkdir(parents=True, exist_ok=True)
    file_path = SOURCE_RAW_PATH / f"cvu_usitermica_{year}.csv"

    response = requests.get(item["url"], impersonate= "chrome")
    response.raise_for_status()

    with open(file_path, "wb") as f:
        f.write(response.content)

    paths.append(file_path)

# ===== transform ========================
dfs = []
for path in paths:
    df = pd.read_csv(path, sep=";")
    dfs.append(df)

df = pd.concat(dfs)
df = df.drop_duplicates()
df = df.sort_values(by="dat_iniciosemana")

dataframes = {}
RAW_PATH.mkdir(parents=True, exist_ok=True)
regions = ['N', 'NE', 'S', 'SE']

for region in regions:
    filtered_df = df[df["id_subsistema"] == region]
    
    # ==== load =============================

    file_path = RAW_PATH / f"cvu_usitermica_{region}.csv"
    filtered_df.to_csv(file_path)

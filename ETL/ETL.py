import numpy as np
import pandas as pd
from clickhouse_driver import Client

filename="CDMQ32025.xlsx"

dfs=pd.read_excel(f"Reports/Cleaned/{filename}",header=None,sheet_name=None)

# ClickHouse connection
client = Client(
    host="localhost",   
    port=9000,
    database="analytics"
)

for sheetname, df in dfs.items():
    #pivot to obtain correct format
    widedf=df.assign(group=df.index//3,pos=df.index%3).pivot(index='group',columns='pos', values=0).rename(columns={0:"IndicatorName",1:"col1",2:"col2"}).reset_index(drop=True)

    widedf.columns=widedf.iloc[0]
    widedf=widedf.iloc[1:]
    widedf=widedf.reset_index(drop=True)

    #unpivot back to get indicator name : indicator value format
    longdf=widedf.melt(id_vars='Results',var_name='Date',value_name='IndicatorValue').rename(columns={"Results":"IndicatorName"})

    #enrich data
    longdf['Bank']=filename.split("Q")[0]
    longdf['Type']=sheetname

    
    #Clean & cast
    longdf['Date'] = pd.to_datetime(longdf['Date'])
    longdf['IndicatorValue'] = longdf['IndicatorValue'].astype(str).str.replace(r'\s+', '', regex=True)
    longdf['IndicatorValue'] = pd.to_numeric(longdf['IndicatorValue'],errors='coerce').fillna(0)

    # Convert to list of tuples
    data = list(
        longdf[['IndicatorName', 'Date', 'IndicatorValue', 'Bank', 'Type']]
        .itertuples(index=False, name=None)
    )

    # Insert into ClickHouse
    client.execute(
        """
        INSERT INTO analytics.stg
        (IndicatorName, Date, IndicatorValue, Bank, Type)
        VALUES
        """,
        data
    )

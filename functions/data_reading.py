import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 900)

df = pd.read_csv('Freiburg_Data.csv', engine="pyarrow")
df = df.iloc[:-2, 2:]
df = df.replace('-', 0)
df = df.replace('N/A', 0)
df.fillna(0)
cols = list(df)

df = df.replace({'km': ''}, regex=True)
df = df.replace({'kg': ''}, regex=True)
df = df.replace({'cm': ''}, regex=True)
df = df.replace({'%': ''}, regex=True)
df = df.replace({'£': ''}, regex=True)
df = df.replace({'p/w': ''}, regex=True)
df['Wage'] = df['Wage'].replace({',': ''}, regex=True)

# TODO: Format transfer value and wage columns to numeric
for i in cols[17:]:
    df[i] = pd.to_numeric(df[i])

#df['Wage'] = pd.to_numeric(df['Wage'])
#df['Height'] = pd.to_numeric(df['Height'])
#df['Weight'] = pd.to_numeric(df['Weight'])


def call_data():

    return df
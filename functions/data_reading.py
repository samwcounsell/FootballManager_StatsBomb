import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 900)

df = pd.read_csv('./the_dataset.csv', engine="pyarrow")
df = df.iloc[:-2, 2:]
df = df.replace('-', 0)
df.fillna(0)
cols = list(df)

df = df.replace({'km': ''}, regex=True)
df = df.replace({'kg': ''}, regex=True)
df = df.replace({'cm': ''}, regex=True)
df = df.replace({'%': ''}, regex=True)
df = df.replace({'£': ''}, regex=True)
df = df.replace({'p/w': ''}, regex=True)

# TODO: Format transfer value and wage columns to numeric
for i in cols[13:]:
    df[i] = pd.to_numeric(df[i])

def call_data():

    return df
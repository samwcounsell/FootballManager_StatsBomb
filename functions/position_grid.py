import pandas as pd

from functions.data_reading import call_data

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

df = call_data()

######### Binary Position Dataframe

# Adding Position Columns
positions = ['GK', 'DL', 'DC', 'DR', 'WBL', 'DM', 'WBR', 'ML', 'MC', 'MR', 'AML', 'AMC', 'AMR', 'ST']
for i in positions:
    df[i] = 0

# Splitting Position List by Vertical Placement on Pitch
column = list(df.Position)
split_column = []

for i in column:
    x = i.split(", ")
    split_column.append(x)

# Working out what positions every player plays in
for i in range(len(split_column)):

    j = split_column[i]

    for k in j:

        l = k.split("/")

        for m in l:

            if 'L' in k:
                if m[0] == 'D':
                        df.loc[i, 'DL'] = 1
                if m[0] == 'W':
                     df.loc[i, 'WBL'] = 1
                if m[0] == 'M':
                        df.loc[i, 'ML'] = 1
                if m[0] == 'A':
                        df.loc[i, 'AML'] = 1

            if 'C' in k:
                if m[0] == 'D':
                        df.loc[i, 'DC'] = 1
                if m[0] == 'M':
                        df.loc[i, 'MC'] = 1
                if m[0] == 'A':
                        df.loc[i, 'AMC'] = 1

            if 'R' in k:
                if m[0] == 'D':
                        df.loc[i, 'DR'] = 1
                if m[0] == 'W':
                        df.loc[i, 'WBR'] = 1
                if m[0] == 'M':
                        df.loc[i, 'MR'] = 1
                if m[0] == 'A':
                        df.loc[i, 'AMR'] = 1

        if 'DM' in k:
            df.loc[i, 'DM'] = 1

        if 'GK' in k:
            df.loc[i, 'GK'] = 1

        if 'ST' in k:
            df.loc[i, 'ST'] = 1


# Calling dataframe from main page

df.to_csv('processed_data_23.csv', index=False)

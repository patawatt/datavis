"""
June 23, 2022

I noticed the neighborhoods have numbers in brackets after each neighbourhood name. Can remove these.
"""

import pandas as pd

df = pd.read_csv('bees.csv')
df['neigbourhood_numbers'] = df.location.map(lambda x: x.split('(')[1].lstrip().rstrip(')'))
df["location"] = df.location.map(lambda x: x.split('(')[0].rstrip())
print(df.head())
df.to_csv('bees.csv')
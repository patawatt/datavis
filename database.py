import sqlite3
import pandas as pd

df_bees = pd.read_csv('bees.csv').iloc[:, 1:]
df_temps = pd.read_excel("day_night_temp_daily_AV.xlsx")

# export to sql database
conn = sqlite3.connect('resources.db')
c = conn.cursor()
c.execute('CREATE TABLE BEES(date, bees)')
conn.commit()
df_bees.to_sql('BEES', conn, if_exists='replace', index=False)

c.execute('CREATE TABLE TEMPS(date, temps)')
conn.commit()
df_temps.to_sql('TEMPS', conn, if_exists='replace', index=False)

# c.execute('''
# SELECT * FROM BEES
# ''')
#
# for row in c.fetchall():
#     print(row)
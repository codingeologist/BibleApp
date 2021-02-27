import sqlite3
import pandas as pd

db = sqlite3.connect('./Data/BIBLE.db')
df = pd.read_sql_query('SELECT * FROM KJV', db)
dfwiki = pd.read_sql_query('SELECT * FROM WIKI', db)
dflocs = pd.read_sql_query('SELECT * FROM LOCATIONS', db)

chapter_filter = df.loc[(df['BOOK'] == 'PSA') & (df['CHAPTER'] == 91)]
verse_filter = df.loc[(df['BOOK'] == 'HEB') & (df['CHAPTER'] == 11) & (df['VERSE'] == 1)]

check = df.loc[(df['BOOK'] == '2KI') & (df['CHAPTER'] == 5) & (df['VERSE'] == 12)]
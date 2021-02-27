import sqlite3
import pandas as pd
###############################################################################
###############################################################################
##Collects SQL Database of the New King James Version + Apocrypha from:      ##
##https://ebible.org/kjv/                                                    ##
##Book codes lookup table created using Wikipedia entries:                   ##
##https://en.wikipedia.org/wiki/List_of_books_of_the_King_James_Version      ##
###############################################################################
###############################################################################
def read_txt(txt, cl_csv):
    df = pd.DataFrame(open(txt, 'r').read().splitlines(),columns=['DATA'])
    df[['BOOK']] = df['DATA'].str.split(' ').str[0]
    df[['CHAPTER_VERSE']] = df['DATA'].str.split(' ').str[1]
    df[['CHAPTER']] = df['CHAPTER_VERSE'].str.split(':').str[0].astype(int)
    df[['VERSE']] = df['CHAPTER_VERSE'].str.split(':').str[1].astype(int)
    df[['TEXT']] = df['DATA'].str.split(' ', 2).str[2].str.replace('Â¶', '')
    
    df = df.drop(['DATA', 'CHAPTER_VERSE'], axis=1)

    dfwiki = pd.read_html('https://en.wikipedia.org/wiki/List_of_books_of_the_King_James_Version')
    old_df = dfwiki[0]
    apo_df = dfwiki[1]
    new_df = dfwiki[2]

    books = df['BOOK'].unique()
    dfwiki = pd.concat([old_df, apo_df, new_df], sort=False)
    dfwiki.columns = ['KING JAMES', 'VULGATE', 'RHEIMS', 'FULL']
    dfwiki['CODE'] = books
    dfwiki = dfwiki[['CODE', 'KING JAMES', 'VULGATE', 'RHEIMS', 'FULL']]
    
    dflocs = pd.read_csv(cl_csv, header=0)
    dflocs = pd.merge(dflocs, df, how='left', left_on=['BOOK', 'CHAPTER', 'VERSE'], right_on=['BOOK', 'CHAPTER', 'VERSE'])
    
    return df, dfwiki, dflocs
    
def save_db(df, dfwiki, dflocs):
    db = sqlite3.connect('./Data/BIBLE.db')
    dfwiki.to_sql('WIKI', db, if_exists='replace', index=False)
    df.to_sql('KJV', db, if_exists='replace', index=False)
    dflocs.to_sql('LOCATIONS', db, if_exists='replace', index=False)

if __name__ == '__main__':
    df, dfwiki, dflocs = read_txt('./Data/eng-kjv_vpl.txt', './DATA/CleanedLocations.csv')
    save_db(df, dfwiki, dflocs)
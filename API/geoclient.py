import pandas as pd

df = pd.read_excel('/Users/lordxuzhiyu/Desktop/Penthouse_Listing_SS.xlsx', sheetname = 'report generated at 0520pm on 2')
df = df.drop([df.columns[0]], axis = 'columns')
df = df.drop(df.index[[0,1,2]])
df.columns = df.iloc[0]
df = df.drop(df.index[0])
df.reset_index(drop = True)

df.to_csv('/Users/lordxuzhiyu/Desktop/Penthouse_Listing_SS.csv')

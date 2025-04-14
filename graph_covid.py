import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_csv("covid_articles_cleaned.csv")
# filter out rows with unknown date
df = df[df['Date'] != 'Unknown']
# Remove known timezones like 'EDT', 'EST', 'PST', etc.
df['Date'] = df['Date'].str.replace(r'\s+[A-Z]{2,4}$', '', regex=True)
# convert to datetime object
df['Date'] = pd.to_datetime(df['Date'], errors='coerce',utc=True)
print(df['Date'].dtype)
df['Date']=df['Date'].dt.tz_localize(None)
df['Date']=df['Date'].dt.date
df = df.sort_values('Date')
#df = df[(df['Date'] > '2020-03-01') & (df['Date'] < '2022-01-31')]
# save as csv
df.to_csv("covid_articles_sorted.csv", index=False)
# get columns other than 'date'
# value_columns = ['disapproval']
# #[col for col in df.columns if col != 'Date' and
# #                col != 'URL' and col != 'Text' and col != 'Sentiment Score']

# # plot them
# for col in value_columns:
#     plt.plot(df['Date'], df[col], label=col)
# plt.savefig('covid_sentiment_analysis.png')
# plt.title('Covid Sentiment Analysis')
# plt.xlabel('Date')
# plt.ylabel('Sentiment Score')
# plt.legend()
# plt.show()
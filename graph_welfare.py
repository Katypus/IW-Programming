import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df1 = pd.read_csv("welfare-1.csv")
df2 = pd.read_csv("welfare-2.csv")
df = pd.concat([df1, df2], ignore_index=True)
# filter out rows with unknown date
df = df[df['Date'] != 'Unknown']
# Remove known timezones like 'EDT', 'EST', 'PST', etc.
df['Date'] = df['Date'].str.replace(r'\s+[A-Z]{2,4}$', '', regex=True)
# convert to datetime object
df['Date'] = pd.to_datetime(df['Date'], errors='coerce',utc=True)
print(df['Date'].dtype)
df['Date']=df['Date'].dt.tz_localize(None)
df = df.sort_values('Date')

# save as csv
df.to_csv("welfare_results.csv", index=False)
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
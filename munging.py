import numpy as np
import pandas as pd

def convert_data(df):
    df = df[['sale_duration', 'previous_payouts', 'acct_type', 'channels', 'delivery_method', 'ticket_types', 'user_type', 'fb_published', 'num_order']]
    df['num_previous_payouts']= [len(row) for row in df['previous_payouts']]

    total = []
    for row in df['ticket_types']:
        cost= 0
        for num in range(len(row)):
            cost +=row[num]['cost']
        total.append(cost)
    df['total_cost'] = total

    df.drop(['ticket_types', 'previous_payouts'], axis =1, inplace = True)
    df['fraud'] = pd.Series(['fraudster' in word for word in df['acct_type']])
    df.drop(['acct_type'], axis = 1, inplace = True)
    df.fillna(inplace = True, value = 44.66)

    print "columns:", df.columns
    return df

if __name__ == '__main__':
    filepath = '../data/data.json'
    df = pd.read_json(filepath)
    df = convert_data(df)
    df.to_csv('../data/clean_data.csv', index = False)

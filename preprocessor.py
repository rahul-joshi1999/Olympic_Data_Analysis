import pandas as pd 



def preprocess(data, region_df):
    
    # filter for only summer olympics
    data = data[data['Season'] ==  'Summer']
    # merge with region_df
    data = data.merge(region_df, on = 'NOC', how = 'left' )
    # dropping duplicates
    data.drop_duplicates(inplace = True)
    # on hot encoding medals
    data = pd.concat([data,pd.get_dummies(data['Medal'])], axis = 1)

    return data 
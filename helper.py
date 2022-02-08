import numpy as np 




def Medal_data(data):
    Medal_data = data.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    Medal_data = Medal_data.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    Medal_data['Total'] = Medal_data['Gold'] + Medal_data['Silver'] + Medal_data['Bronze']
    
    Medal_data['Gold'] = Medal_data['Gold'].astype('int')
    Medal_data['Silver'] = Medal_data['Silver'].astype('int')
    Medal_data['Bronze'] = Medal_data['Bronze'].astype('int')
    Medal_data['Total'] = Medal_data['Total'].astype('int')

    return Medal_data


def Country_Year_List(data):
    years = data['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    
    country = data['region'].sort_values().unique().tolist()
    #country = data['region'].unique().tolist()
    #country.sort()
    country.insert(0,'Overall')

    return years, country 

def Fetch_Medal_data(data,country, year):
    Medal_df = data.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0
    if country == 'Overall' and year == 'Overall':
        temp_df = Medal_df 
    if country == 'Overall' and year != 'Overall':
        temp_df = Medal_df[Medal_df['Year'] == int(year) ]
    if country != 'Overall' and year == 'Overall':
        flag = 1
        temp_df = Medal_df[Medal_df['region'] == country ]
    if country != 'Overall' and year != 'Overall':
        temp_df = Medal_df[(Medal_df['region'] == country) & (Medal_df['Year'] == int(year))]
        
        #print(temp_df)
        
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year',ascending=True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
        
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')
    
    return(x)


def participating_nations_over_time(data):

    nations_over_time = data.drop_duplicates(['region','Year'])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_time.rename(columns = {'index':'Edition', 'Year':"No of Country's"},inplace = True)
    return nations_over_time

def events_over_time(data):
    events_over_time = data.drop_duplicates(['Event','Year'])['Year'].value_counts().reset_index().sort_values('index')
    events_over_time.rename(columns = {'index':'Edition', 'Year':"No of Event's"},inplace = True)
    return events_over_time

def athletes_over_time(data):
    athletes_over_time = data.drop_duplicates(['Name','Year'])['Year'].value_counts().reset_index().sort_values('index')
    athletes_over_time.rename(columns = {'index':'Edition', 'Year':"Number of athletes"},inplace = True)
    return athletes_over_time


def most_succesfull(data,sport):
    temp_df = data.dropna(subset = ['Medal'])
    
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
        
    x = temp_df['Name'].value_counts().reset_index().head(15).merge(data,left_on = 'index', right_on = 'Name', how = 'left')[['index','Name_x','Sport','region']].drop_duplicates('index')
    x.rename(columns={'index':'Name','Name_x':'Medals'},inplace = True)
    return x


def yearwise_medal_tally(data,country):
    temp_df = data.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace = True) 
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df


def countru_event_heatmap(data,country):
    temp_df = data.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'],inplace = True) 
    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index = 'Sport', columns = 'Year', values = 'Medal', aggfunc = 'count').fillna(0)
    return pt

def most_successfull_countrywise(data,country):
    temp_df = data.dropna(subset = ['Medal'])
    temp_df = temp_df[temp_df['region'] == country]
    x = temp_df['Name'].value_counts().reset_index().head(10).merge(data,left_on = 'index', right_on = 'Name', how = 'left')[['index','Name_x','Sport']].drop_duplicates('index')
    x.rename(columns={'index':'Name','Name_x':'Medals'},inplace = True)
    return x


def weight_v_height(data,sport):
    athlete_df = data.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(data):
    athlete_df = data.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final
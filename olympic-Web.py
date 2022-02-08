import streamlit as st
import pandas as pd 
import preprocessor,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

data = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')


data = preprocessor.preprocess(data,region_df)

st.sidebar.title("Olympic Analysis")
st.sidebar.image("Olympic_Rings.png")

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Data','Overall Analysis','Country Wise Analysis','AthleteWise Analysis')
)


#st.dataframe(region_df)

if user_menu == 'Medal Data':
    st.header("Medal Data")
    years,country = helper.Country_Year_List(data)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    Medal_data = helper.Fetch_Medal_data(data, selected_country, selected_year)
    if selected_country == 'Overall' and selected_year == 'Overall':
        st.title("Overall Tally")
    if selected_country != 'Overall'  and selected_year == 'Overall':
        st.title(" Country is {} and year is Overall" .format(selected_country))
    if selected_country == 'Overall'  and selected_year != 'Overall':
        st.title(" Country is Overall and year is {}" .format(selected_year))
    if selected_country != 'Overall'  and selected_year != 'Overall':
        st.title(" Country is {} and year is {}" .format(selected_country,selected_year))
    
    
    st.table(Medal_data)

if user_menu == "Overall Analysis":
    st.header("Overall Analysis")
    editions = data["Year"].unique().shape[0]-1
    cities = data["City"].unique().shape[0]
    sports = data['Sport'].unique().shape[0]
    event = data['Event'].unique().shape[0]
    athletes = data['Name'].unique().shape[0]
    nations = data['region'].unique().shape[0]
    
    st.title("Top Statistics")

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(event)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes) 
    

    st.title("Number of Participating Nation over the Years")
    nations_over_time = helper.participating_nations_over_time(data)
    fig = px.line(nations_over_time, x = 'Edition', y = "No of Country's")
    st.plotly_chart(fig)

    st.title("Number of Events over the Years")
    events_over_time = helper.events_over_time(data)
    fig = px.line(events_over_time, x = 'Edition', y = "No of Event's")
    st.plotly_chart(fig)

    st.title("Number of Athletes over the Years")
    athletes_over_time = helper.athletes_over_time(data)
    fig = px.line(athletes_over_time, x = 'Edition', y = "Number of athletes")
    st.plotly_chart(fig)

    st.title("Number of Events over Time")
    fig,ax = plt.subplots(figsize=(20,10))
    x = data.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index = 'Sport', columns = 'Year', values = 'Event', aggfunc = 'count' ).fillna(0).astype(int),annot = True)
    st.pyplot(fig)

    st.title("Most Successfull Athletes")
    sport_list = data['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list) 
    x = helper.most_succesfull(data,selected_sport)
    st.table(x)

if user_menu == 'Country Wise Analysis':
    st.header("Country Wise Analysis")
    st.sidebar.title('Country Wise Analysis')
    country_list = data['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select Country', country_list)
    country_df = helper.yearwise_medal_tally(data, selected_country)
    fig = px.line(country_df, x = "Year", y = "Medal")
    st.title(selected_country + " Medal Tally Over The Years")
    st.plotly_chart(fig)

    st.title(selected_country + " excels in the following sports")
    pt = helper.countru_event_heatmap(data, selected_country)
    fig, ax = plt.subplots(figsize=(10,10))
    ax = sns.heatmap(pt,annot = True)
    st.pyplot(fig)

    st.title("Top 10 Athletes of Country " + selected_country)
    top_df = helper.most_successfull_countrywise(data, selected_country)
    st.table(top_df)


if user_menu == 'AthleteWise Analysis':
    st.header("AthleteWise Analysis")
    athlete_df = data.drop_duplicates(subset = ['Name','region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4],['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist = False, show_rug = False )
    fig.update_layout(autosize = False, width = 1000, height = 600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)


    
    

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    
    fig = ff.create_distplot(x,name, show_hist=False,show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)


    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
        name.append(sport)

    
    fig = ff.create_distplot(x,name, show_hist=False,show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Silver Medalist)")
    st.plotly_chart(fig)


    sport_list = data['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(data,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(temp_df['Weight'],temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.pyplot(fig)

    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(data)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

    
    
    
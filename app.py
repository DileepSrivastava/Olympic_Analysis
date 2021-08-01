import streamlit as st
import pandas as pd
import preprocessor
import helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')


df = preprocessor.preprocess(df, region_df)



st.sidebar.title("Olympic Analysis")
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis ')
)

#st.dataframe(df)

if user_menu== 'Medal Tally':
    st.sidebar.header('Medal Tally')
    years, country = helper.country_year_list(df)

    selected_years= st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox('Select Country', country)
    medal_tally = helper.fetch_medal_tally(df, selected_years,selected_country)
    if selected_years =='Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_years != 'Overall' and selected_country == 'Overall':
        st.title('Medall Tally in ' + str(selected_years) + ' Olympics')
    if selected_years == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + 'Overall performance')
    if selected_years !='Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Performance in ' + str(selected_years) + ' Olympics')
    st.table(medal_tally)



# Overall Analysis
if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    # Top Stats
    st.title('Top Stats')
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Cities')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Athletes')
        st.title(athletes)
    with col3:
        st.header('Participating Nations')
        st.title(nations)

    # Most Successful Athletes
    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('select sport', sport_list)
    Msa = helper.most_succesful_athletes(df, selected_sport)
    st.table(Msa)

    # Participating Nations over the years
    nations_over_time = helper.dat_over_time(df, 'region')
    fig = px.line(nations_over_time, x="Editions", y='region')
    st.title('Participating Nations over the years')
    st.plotly_chart(fig)

    # Events Over the years
    events_over_time = helper.dat_over_time(df, 'Event')
    fig = px.line(events_over_time, x='Editions', y='Event')
    st.title('Events Over the years')
    st.plotly_chart(fig)

    # Athletes Over the years
    athletes_over_time = helper.dat_over_time(df, 'Name')
    fig = px.line(athletes_over_time, x='Editions', y='Name')
    st.title('Athletes Over the years')
    st.plotly_chart(fig)

    # No of Events over the time(Every Sport)
    st.title("No of Events over the time(Every Sport)")
    fig, ax = plt.subplots(figsize=(25,25))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
                annot=True, cmap='YlGnBu')
    st.pyplot(fig)


if user_menu == 'Country-wise Analysis':

    st.title('Country-wise Analysis')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    #country_list.insert(0,'Select')
    selected_country = st.sidebar.selectbox('Select Country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + ' Medal tally Over the years')
    st.plotly_chart(fig)

    st.title(selected_country + ' Excel in the following sports')
    pt = helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(25, 25))
    ax = sns.heatmap(pt, annot=True, cmap='YlGnBu')
    st.pyplot(fig)

    st.title('Top 100 Athletes of ' + selected_country)
    top60_df = helper.most_successful_countrywise(df, selected_country)
    st.table(top60_df)









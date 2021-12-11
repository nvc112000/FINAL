"""
Class: CS230--Section 004
Name: Nick Carson
Description: Final Project. This Program reads the data from Boston crimes and displays
it in a number of ways. Users can select by crime or district and see charts,maps, and
detailed information for both.
"""
import pandas as pd
import pydeck as pdk
import streamlit as st
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
districts = pd.read_csv("BostonPoliceDistricts.csv").set_index("District")


def read_data():
    return pd.read_csv("bostoncrime2021_7000_sample.csv").set_index("INCIDENT_NUMBER")


# MAIN MAPS & CHARTS
# Map of crime locations (based on input from sidebar)
def map_create2(df_filtered):
    lat = 42.29755533
    lon = -71.0589
    view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=10)
    layer = pdk.Layer('ScatterplotLayer', data=df_filtered, get_position=['Long', 'Lat'], get_radius=200,
                      get_color=[100, 150, 200])
    tool_tip = {'html': 'Listing:<br><b>{name}</b>', 'style': {'backgroundColor': 'steelblue', 'color': 'white'}}
    map = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9',
                   initial_view_state=view_state,
                   layers=[layer],
                   tooltip=tool_tip)
    st.pydeck_chart(map)


# Pie chart of overall occurrence of different types of crimes (may have to be by code)
def crime_rate(sel_districts, df):
    result = [df.loc[df['DISTRICT'] == district].shape[0] for district in sel_districts]
    return result


def pie_chart(counts, sel_districts):
    plt.figure()
    plt.pie(counts, labels=sel_districts, autopct="%1.1f%%")
    plt.title(f"Frequency of Crimes per District: {','.join(sel_districts)}")
    return plt


# Bar chart displaying the occurrence of crimes by day for a selected district
def bar_chart2(fd, color, district):
    plt.figure()
    x = fd['Days']
    y = fd['Counts']
    plt.bar(x, y, color=color)
    plt.xticks(rotation='vertical')
    plt.title(f"Number of Crimes by Day: {''.join(district)}")
    plt.ylabel("Number of Crimes", fontsize=16, fontweight="bold")
    plt.xlabel("Day of Week", fontsize=16, fontweight="bold")
    return plt


def main():

    # District read in
    d_chart = pd.read_csv("BostonPoliceDistricts.csv").set_index("District")
    # FORMATTING
    st.subheader("By Nick Carson", st.title("Analysis of Boston Crime"))
    st.sidebar.header("Boston Crime Filters")
    df = read_data()
    df.dropna()

    # SIDEBAR
    # Drop down list of types of crime
    crimes = df['OFFENSE_DESCRIPTION'].unique()
    crime = st.sidebar.selectbox('Crime type (For Map)', crimes)

    # multiselect list of districts
    dricts = df['DISTRICT'].unique()
    sel_districts = st.sidebar.multiselect('Districts (For Pie Chart)', dricts)

    # Drop down list of District
    st.sidebar.write("District chart", d_chart)
    district = df['DISTRICT'].unique()
    sel_district = st.sidebar.selectbox('District (For Bar Chart)', district)

    # MAP
    df_filtered = df[df['OFFENSE_DESCRIPTION'] == crime]
    st.subheader("Map based on selected crime")
    df_filtered["Long"] = df_filtered["Long"]
    df_filtered["Lat"] = df_filtered["Lat"]
    map_data = df_filtered[["Long", "Lat"]]
    map_create2(map_data)

    # Details/statistics for specified crime
    st.subheader("Detailed Crime Data")
    df_filtered = df_filtered.drop(
        columns=['OFFENSE_CODE_GROUP', 'SHOOTING', 'UCR_PART', 'MONTH', 'HOUR', 'Location', 'REPORTING_AREA'])
    st.dataframe(df_filtered)
    c_count = df_filtered['OFFENSE_CODE'].count()
    st.write("Total Number of Offenses:", c_count)
    d_count = df_filtered['DISTRICT'].mode()
    st.write(f"District(s) Crime Occurs Most in: {','.join(d_count)}")

    # piechart
    st.subheader("Pie Chart Comparing Crime Rate Based on District")
    st.pyplot(pie_chart(crime_rate(sel_districts, df), sel_districts))

    # bar chart
    fda = df[df['DISTRICT'] == sel_district]
    st.subheader("Bar chart of Number of crimes per day of week")
    fd = fda['DAY_OF_WEEK'].value_counts().rename_axis("Days").reset_index(name="Counts")
    color = st.sidebar.color_picker('Pick A Color (For Bar Charts)', '#7AD8D8')
    st.pyplot(bar_chart2(fd, color, sel_district))

    # Bar chart stats
    st.subheader("Detailed District Data")
    fda = fda.drop(
        columns=['OFFENSE_CODE_GROUP', 'SHOOTING', 'UCR_PART', 'MONTH', 'HOUR', 'Location', 'REPORTING_AREA'])
    st.dataframe(fda)
    t_crimes = fda['DISTRICT'].count()
    st.write('Total Number of Offenses in District: ', t_crimes)
    most_crime = fda['OFFENSE_DESCRIPTION'].mode()
    st.write(f"Most Frequent Crime(s) In District: {''.join(most_crime)}")
    s_count = fda['STREET'].mode()
    st.write(f"Street With Most Crime: {''.join(s_count)}")


main()

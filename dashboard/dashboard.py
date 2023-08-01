import streamlit as st
import pandas   as pd
import matplotlib.pyplot as plt
import seaborn as sns



def create_day_df(df):
    byday_df = df.groupby(by="weekday").instant.nunique().reset_index()
    byday_df.rename(columns={"instant": "sum"}, inplace=True)
    return byday_df

def create_weathersit_df(df):
    weathersit_df = df.groupby(by="weathersit").instant.nunique().reset_index()
    weathersit_df.rename(columns={"instant": "sum"}, inplace=True)
    return weathersit_df

def create_season_df(df):
    season_df = df.groupby(by="season").instant.nunique().reset_index()
    season_df.rename(columns={"instant": "sum"}, inplace=True)
    return season_df

day_df = pd.read_csv("dashboard/main_data.csv")

day_df.loc[day_df["weekday"] == 0, "weekday"] = "sunday"
day_df.loc[day_df["weekday"] == 1, "weekday"] = "monday"
day_df.loc[day_df["weekday"] == 2, "weekday"] = "tuesday"
day_df.loc[day_df["weekday"] == 3, "weekday"] = "wednesday"
day_df.loc[day_df["weekday"] == 4, "weekday"] = "thursday"
day_df.loc[day_df["weekday"] == 5, "weekday"] = "friday"
day_df.loc[day_df["weekday"] == 6, "weekday"] = "saturday"

day_df.loc[day_df["weathersit"] == 1, "weathersit"] = "clear"
day_df.loc[day_df["weathersit"] == 2, "weathersit"] = "cloudy/mist"
day_df.loc[day_df["weathersit"] == 3, "weathersit"] = "light rain/snow"
day_df.loc[day_df["weathersit"] == 4, "weathersit"] = "heavy rain/snow"

day_df.loc[day_df["season"] == 1, "season"] = "springer"
day_df.loc[day_df["season"] == 2, "season"] = "summer"
day_df.loc[day_df["season"] == 3, "season"] = "fall"
day_df.loc[day_df["season"] == 4, "season"] = "winter"

datetime_columns = ["dteday"]
day_df.sort_values(by="dteday", inplace=True)
day_df.reset_index(inplace=True)
 
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.image("https://raw.githubusercontent.com/anddfian/Dicoding-BADP/main/Submission/dashboard/Capital Bikeshare Logo.png")
    start_date, end_date = st.date_input(
    label="Pilih Rentang Waktu", 
    min_value=min_date, 
    max_value=max_date,
            value=[min_date, max_date],
            )

main_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

byday_df = create_day_df(main_df)
weathersit_df = create_weathersit_df(main_df)
season_df = create_season_df(main_df)



st.subheader("Performa Berdasarkan Hari")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    x="weekday",
    y="sum",
    data=byday_df.sort_values(by="weekday", ascending=False),
    )
plt.xlabel(None)
plt.ylabel(None)
plt.title("Performa Penggunaan Bike Sharing Berdasarkan Hari", loc="center", fontsize=20)
plt.tick_params(axis="x", labelsize=15)
st.pyplot(fig)


st.subheader("Performa Berdasarkan Cuaca")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    x="weathersit",
    y="sum",
    data=weathersit_df.sort_values(by="weathersit", ascending=False),
    ax=ax
)
plt.xlabel(None)
plt.ylabel(None)
plt.title("Performa Penggunaan Bike Sharing Berdasarkan Cuaca", loc="center", fontsize=20)
plt.tick_params(axis="x", labelsize=15)
st.pyplot(fig)


st.subheader("Performa Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    x="season",
    y="sum",
    data=season_df.sort_values(by="season", ascending=False),
    ax=ax
)
plt.xlabel(None)
plt.ylabel(None)
plt.title("Performa Penggunaan Bike Sharing Berdasarkan Musim", loc="center", fontsize=20)
plt.tick_params(axis="x", labelsize=15)
st.pyplot(fig)













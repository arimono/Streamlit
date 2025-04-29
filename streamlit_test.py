import time
from models import selectAll
import streamlit as st
import pandas as pd
import altair as alt
from streamlit_autorefresh import st_autorefresh

st.title('IoT Demo - Real-Time Chart')

# Refresh every 5 seconds
st_autorefresh(interval=5000, key="realtime_chart")

# Fetch data
data, column = selectAll("sensor")
df = pd.DataFrame(data, columns=column)

# Ensure numeric conversion
df['temp'] = df['temp'].astype(float)
df['humidity'] = df['humidity'].astype(float)

# Convert 'time' column to datetime if needed
df['time'] = pd.to_datetime(df['time'])

# Melt data for Altair
df_temp = df.melt(id_vars='time', value_vars=['temp'], var_name='metric', value_name='value')
df_humidity = df.melt(id_vars='time', value_vars=['humidity'], var_name='metric', value_name='value')

# Create charts
temp_chart = alt.Chart(df_temp).mark_line(point=True).encode(
    x=alt.X('time:T', title='Time'),
    y=alt.Y('value:Q', title='Temperature'),
    color='metric:N',
    tooltip=['time:T', 'metric:N', 'value:Q']
).properties(width=800, height=300, title='Temperature Time Series')

humidity_chart = alt.Chart(df_humidity).mark_line(point=True).encode(
    x=alt.X('time:T', title='Time'),
    y=alt.Y('value:Q', title='Humidity'),
    color='metric:N',
    tooltip=['time:T', 'metric:N', 'value:Q']
).properties(width=800, height=300, title='Humidity Time Series')

# Display
st.dataframe(df, hide_index=True)
st.altair_chart(temp_chart, use_container_width=True)
st.altair_chart(humidity_chart, use_container_width=True)
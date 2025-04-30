import time
from models import select100
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

st.title('IoT Demo - Real-Time Chart')

# Container for charts
chart_placeholder = st.empty()

# Refresh interval (seconds)
refresh_interval = 10

# Main loop
while True:
    # Fetch data from your DB
    data, column = select100("sensor")
    
    # Convert to DataFrame
    df = pd.DataFrame(data, columns=column)
    
    # Ensure 'time' is in datetime format
    df['time'] = pd.to_datetime(df['time'])

    # Filter the DataFrame to include only the last hour
    current_time = datetime.now()
    one_hour_ago = current_time - timedelta(hours=1)
    df = df[df['time'] >= one_hour_ago]

    # Convert columns to float for proper charting
    df['temp'] = df['temp'].astype(float)
    df['humidity'] = df['humidity'].astype(float)

    # Melt for Altair
    df_temp = df.melt(id_vars='time', value_vars=['temp'], var_name='metric', value_name='value')
    df_humidity = df.melt(id_vars='time', value_vars=['humidity'], var_name='metric', value_name='value')

    # Create charts
    temp_chart = alt.Chart(df_temp).mark_line(point=False).encode(
        x=alt.X('time:T', title='Time'),
        y=alt.Y('value:Q', title='Temperature'),
        color='metric:N',
        tooltip=['time:T', 'metric:N', 'value:Q']
    ).properties(width=800, height=300, title='Temperature Time Series')

    humidity_chart = alt.Chart(df_humidity).mark_line(point=False).encode(
        x=alt.X('time:T', title='Time'),
        y=alt.Y('value:Q', title='Humidity'),
        color='metric:N',
        tooltip=['time:T', 'metric:N', 'value:Q']
    ).properties(width=800, height=300, title='Humidity Time Series')

    # Update charts in container
    with chart_placeholder.container():
        st.dataframe(df, hide_index=True)
        st.altair_chart(temp_chart, use_container_width=True)
        st.altair_chart(humidity_chart, use_container_width=True)

    # Wait before updating
    print("refreshed")
    time.sleep(refresh_interval)
# File: pages/4_Agriculture2050.py

import streamlit as st
import pandas as pd
import pydeck as pdk

# Set page configuration and title with project theme
st.set_page_config(
    page_title="Agriculture 2050: European Maps Visualization",
    page_icon="🌱",
)
st.markdown("# Agriculture 2050: European Maps Visualization")
st.sidebar.header("Map Settings")

# Map scale selector
scale_options = ["Square Area", "NUTS 1", "NUTS 2", "NUTS 3"]
selected_scale = st.sidebar.selectbox("Select map scale", scale_options)

# Adjust layer settings based on selected scale (example: setting a radius)
if selected_scale == "Square Area":
    radius = 50000
elif selected_scale == "NUTS 1":
    radius = 40000
elif selected_scale == "NUTS 2":
    radius = 30000
elif selected_scale == "NUTS 3":
    radius = 20000

st.sidebar.markdown(f"### Selected Scale: {selected_scale}\nRadius: {radius}")

# Example tabular data – replace with your European agriculture data
data = pd.DataFrame({
    "Country": ["France", "Germany", "Spain", "Italy"],
    "Value": [100, 200, 150, 120],
    "lat": [46.603354, 51.165691, 40.463667, 41.87194],   # approximate center latitudes
    "lon": [1.888334, 10.451526, -3.74922, 12.56738]         # approximate center longitudes
})

st.write("### European Agriculture Data", data)

# Download button for CSV export of the table
csv = data.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Export data as CSV",
    data=csv,
    file_name='european_agriculture_data.csv',
    mime='text/csv',
)

# Create a pydeck scatterplot layer to visualize the data points
scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=data,
    get_position=["lon", "lat"],
    get_color="[0, 100, 200, 160]",
    get_radius=radius,
)

# Set an initial view over Europe
view_state = pdk.ViewState(
    latitude=54.5260,   # roughly the center latitude of Europe
    longitude=15.2551,  # roughly the center longitude of Europe
    zoom=4,
    pitch=0,
)

# Build the deck.gl map
r = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=view_state,
    layers=[scatter_layer],
)

st.pydeck_chart(r)

# Additional project details
st.markdown("## About Agriculture 2050")
st.markdown("""
**Agriculture 2050** is an innovative project aimed at visualizing European agricultural landscapes and production data.
This tool integrates interactive map selections, customizable scales, and data export features to help stakeholders explore and understand
agricultural trends and potential future scenarios across Europe.
""")

import streamlit as st
import pandas as pd
import os
from data_extraction import extract_polygon_data_from_html

# Page Configuration
st.set_page_config(page_title="Dynamic Map Visualization", layout="wide")

# Sidebar Settings
st.sidebar.title("⚙️ Settings")

# Zone Selection
zone = st.sidebar.selectbox("Select Zone:", ["Germany", "France"])

# Scale Selection
scale = st.sidebar.selectbox("Select Scale:", ["Finest", "Grid", "NUTS 3", "NUTS 2", "NUTS 1"])

# Show Grid Toggle
show_grid = st.sidebar.checkbox("Show Grid Overlay", False)

# Variable Selection (This affects which layer or data is displayed on the map)
variable = st.sidebar.selectbox("Select Variable:", ["Temperature", "NDVI", "Crop"])

time = st.sidebar.selectbox("Select Scale:", ["2019", "2020", "2021", "2022", "2023"])

# Title
st.title("🗺️ Interactive Agriculture Map Visualization")

# Function to get the corresponding map file
def get_map_file(zone, scale, grid, variable):
    """Returns the appropriate map file name based on selected settings."""
    var_suffix = f"_{variable.replace(' ', '_')}"  # Replace spaces with underscores for filenames
    filename = f"maps/{zone}_{scale}_{variable}_{time}.html"
    return filename

# Get the selected map file
map_file = get_map_file(zone, scale, show_grid, variable)

# Check if the file exists
if os.path.exists(map_file):
    with open(map_file, "r", encoding="utf-8") as f:
        map_html = f.read()
    st.components.v1.html(map_html, height=500)  # Display the map
else:
    st.error(f"Map file `{map_file}` not found! Please ensure the file exists.")

if scale == "Grid":
    # Data Tables Section
    st.subheader("📊 Data Tables")

    # Sample Data (You can replace this with actual data from a database or CSV file)
    data1 = extract_polygon_data_from_html(map_file)


    # Layout with Two Columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### Tabular Data")
        st.dataframe(data1)

    with col2:
        st.markdown(f"### Data summary")
        st.dataframe(data1.describe())

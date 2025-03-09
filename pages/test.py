import streamlit as st
import boto3
from botocore.exceptions import ClientError
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

# Variable Selection
variable = st.sidebar.selectbox("Select Variable:", ["Crop", "Moisture", "Temperature", "NDVI", "Population"])

# Time/Year Selection
time = st.sidebar.selectbox("Select Year:", ["2019", "2020", "2021", "2022", "2023"])

# Title
st.title("🗺️ Interactive Agriculture Map Visualization")

def get_map_file(zone, scale, grid, variable):
    """
    Constructs the S3 key for the HTML map file based on user selections.
    """
    filename = f"maps/{zone}_{scale}_{variable}_{time}.html"
    return filename

# Get the S3 key for the map file
map_key = get_map_file(zone, scale, show_grid, variable)

# S3 configuration
bucket_name = 'team-emos-ensai'
endpoint_url = 's3.waw3-2.cloudferro.com'
aws_access_key_id = 'YOUR_ACCESS_KEY'
aws_secret_access_key = 'YOUR_SECRET_KEY'

def get_map_from_s3(bucket_name, key):
    """
    Retrieve HTML content from S3 using boto3 with a custom endpoint.
    """
    s3 = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    try:
        response = s3.get_object(Bucket=bucket_name, Key=key)
        map_html = response['Body'].read().decode('utf-8')
        return map_html
    except ClientError as e:
        st.error(f"Error reading map file from S3: {e}")
        return None

# Get the HTML content from S3
map_html = get_map_from_s3(bucket_name, map_key)

if map_html:
    st.components.v1.html(map_html, height=500)
else:
    st.error(f"Map file `{map_key}` not found in bucket `{bucket_name}`!")

# If the selected scale is "Grid", display additional data tables
if scale == "Grid":
    st.subheader("📊 Data Tables")
    
    # Use the HTML content directly if your extraction function supports it.
    data1 = extract_polygon_data_from_html(map_html) if map_html else None

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Tabular Data")
        if data1 is not None:
            st.dataframe(data1)
        else:
            st.write("No data available.")
    with col2:
        st.markdown("### Data Summary")
        if data1 is not None:
            st.dataframe(data1.describe())
        else:
            st.write("No data available.")

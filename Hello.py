import streamlit as st

# Page Configuration
st.set_page_config(page_title="🌱 Agriculture Map App", layout="wide")

# Title
st.title("🌱 Agriculture Mapping & Visualization Platform")

# Subtitle
st.markdown("### Leveraging Data & Maps for Smarter Agriculture")

# Image or Banner (Optional - Replace with an actual file or URL)
st.image("images/EU-Big-Data-Hackathon-2025_horiz.jpg", use_container_width=True)

# Project Overview
st.markdown("""
#### 🌍 About This Project
This platform aims to provide farmers, researchers, and policymakers with interactive maps and data-driven insights for agricultural planning.  
Using geospatial data, users can visualize **soil health**, **crop distribution**, and **climate patterns** to make informed decisions.

#### 📌 Key Features
✅ Interactive **Maps** with satellite imagery  
✅ **Weather & Soil Data** integration  
✅ **Predictive Analytics** for crop yield  
✅ **Customizable Layers** (e.g., irrigation, vegetation)  
✅ **Download Reports** for decision-making  

""")

# Navigation Button
st.write("🚀 **Ready to explore?** Click below to access the interactive map.")
if st.button("Go to Maps 🗺️"):
    st.switch_page("map.py")  # Adjust filename based on actual navigation

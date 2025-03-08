import re
import json
import pandas as pd


def extract_polygon_data_from_html(html_file_path: str) -> pd.DataFrame:
    """
    Extracts polygon data from an HTML file containing a unique 
    <script type="application/json" ...> block. It extracts the 
    agriculture share values and the GRD_ID (detected via a fixed prefix
    'CRS3035RES10000m' followed by 16 characters) from the JSON data.
    
    Parameters:
      html_file_path (str): The path to the HTML file.
    
    Returns:
      pd.DataFrame: A DataFrame with columns 'feature_id', 'agriculture_share', and 'GRD_ID'.
    """
    
    # Read the HTML file.
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Extract the JSON content from the unique <script> tag.
    pattern = r'<script\s+type="application/json"[^>]*>(.*?)</script>'
    match = re.search(pattern, html_content, re.DOTALL)
    if not match:
        raise ValueError("No JSON content found in the provided HTML.")
    json_text = match.group(1)
    
    # Parse the JSON content.
    data = json.loads(json_text)
    
    # Locate the "addPolygons" call in the "calls" array.
    calls = data["x"]["calls"]
    polygon_call = next((call for call in calls if call.get("method") == "addPolygons"), None)
    if polygon_call is None:
        raise ValueError("No 'addPolygons' method found in the JSON calls.")
    
    # The expected structure:
    #   args[4]: List of popup HTML strings (containing GRD_ID information)
    #   args[5]: List of agriculture share values (as strings)
    
    # Detect the correct arguments automatically.
    popup_html_index = None
    agri_shares_index = None
    
    def is_float_list(lst):
        if isinstance(lst, list) and lst:
            try:
                [float(x) for x in lst]
                return True
            except Exception:
                return False
        return False

    for i, arg in enumerate(polygon_call["args"]):
        if isinstance(arg, list):
            # If the first element is a string and contains "GRD_ID", assume it's the popup HTML list.
            if arg and isinstance(arg[0], str):
                if "GRD_ID" in arg[0]:
                    popup_html_index = i
            # Check if this list can be converted to floats.
            if is_float_list(arg):
                agri_shares_index = i

    # Fallback defaults if auto-detection fails.
    if popup_html_index is None:
        popup_html_index = 4
        print("Falling back to default popup HTML index:", popup_html_index)
    if agri_shares_index is None:
        agri_shares_index = 5
        print("Falling back to default agriculture share index:", agri_shares_index)
    
    # Extract agriculture share values.
    agri_shares_str = polygon_call["args"][agri_shares_index]
    agri_shares = [float(val) for val in agri_shares_str]
    
    # Extract GRD_ID values from the popup HTML strings.
    popup_html_list = polygon_call["args"][popup_html_index]
    grd_ids = []
    # Regex to match fixed prefix "CRS3035RES10000m" followed by exactly 16 characters.
    grd_pattern = r'(CRS3035RES10000m.{16})'
    for html_snippet in popup_html_list:
        m = re.search(grd_pattern, html_snippet)
        if m:
            grd_ids.append(m.group(1))
        else:
            grd_ids.append(None)
    
    if len(grd_ids) != len(agri_shares):
        print("Warning: The number of GRD_ID values and agriculture share values do not match.")
    
    # Create and return the DataFrame.
    df = pd.DataFrame({
        "feature_id": range(1, len(agri_shares) + 1),
        "agriculture_share": agri_shares,
        "GRD_ID": grd_ids
    })
    
    return df.drop(columns=["feature_id"])

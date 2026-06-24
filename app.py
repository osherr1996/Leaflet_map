import streamlit as st
import folium
from streamlit_folium import st_folium
from shapely.geometry import Polygon
from pyproj import Geod

st.set_page_config(layout="wide")

st.title("Reservoir Polygon Selector")

# Map
m = folium.Map(
    location=[31.5, 34.9],  # Israel
    zoom_start=8,
    tiles="Esri.WorldImagery"
)

# Draw plugin
from folium.plugins import Draw

Draw(
    draw_options={
        "polyline": False,
        "rectangle": False,
        "circle": False,
        "marker": False,
        "circlemarker": False,
        "polygon": True,
    },
    edit_options={"edit": True},
).add_to(m)

map_data = st_folium(
    m,
    height=700,
    width=None,
)

# Read drawn polygon
if map_data and map_data.get("all_drawings"):
    poly = map_data["all_drawings"][-1]

    coords = poly["geometry"]["coordinates"][0]

    st.subheader("Polygon Coordinates")
    st.code(coords)

    # Area calculation (m²)
    geod = Geod(ellps="WGS84")

    lons = [p[0] for p in coords]
    lats = [p[1] for p in coords]

    area_m2, _ = geod.polygon_area_perimeter(lons, lats)
    area_m2 = abs(area_m2)

    st.subheader("Area")
    st.metric("Area (m²)", f"{area_m2:,.0f}")
    st.metric("Area (ha)", f"{area_m2/10000:,.2f}")
    st.metric("Area (km²)", f"{area_m2/1e6:,.4f}")

    st.subheader("Python Polygon")
    st.code(str(coords))

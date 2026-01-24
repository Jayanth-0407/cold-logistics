import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Risk-Aware Logistics", layout="wide")

st.title("AI-Powered Cold Chain Logistics")
st.markdown("---")

with st.sidebar:
    st.header("Configure Shipment")

    cargo_type = st.selectbox(
        "Select Cargo Type", 
        ["ice cream","milk","vaccines","electronics"]
    )
    
    route_option = st.selectbox(
        "Select Route",
        [
            "Manali -> Leh",
            "Chennai -> Kanchipuram",
            "Delhi -> Agra",
            "Mumbai -> Pune",
            "Jaisalmer -> Jodhpur",
            "Srinagar -> Gulmarg",
            "Bangalore -> Mysore"
        ]
    )
    
    routes = {
        "Manali -> Leh": {
            "start": [32.2432, 77.1892], "end": [34.1526, 77.5770]
        },
        "Chennai -> Kanchipuram": {
            "start": [13.0827, 80.2707], "end": [12.8185, 79.7156]
        },
        "Delhi -> Agra": {
            "start": [28.6139, 77.2090], "end": [27.1767, 78.0081]
        },
        "Mumbai -> Pune": {
            "start": [19.0760, 72.8777], "end": [18.5204, 73.8567]
        },
        "Jaisalmer -> Jodhpur": {
            "start": [26.9157, 70.9083], "end": [26.2389, 73.0243]
        },
        "Srinagar -> Gulmarg": {
            "start": [34.0837, 74.7973], "end": [34.0484, 74.3805]
        },
        "Bangalore -> Mysore": {
            "start": [12.9716, 77.5946], "end": [12.2958, 76.6394]
        }
    }
    
    selected_route=routes[route_option]
    
    analyze_btn=st.button("Analyze Risk", type="primary")

if analyze_btn:
    with st.spinner("Consulting AI Model..."):
        try:
            payload = {
                "start_lat": selected_route["start"][0],
                "start_lon": selected_route["start"][1],
                "end_lat": selected_route["end"][0],
                "end_lon": selected_route["end"][1],
                "cargo_type": cargo_type
            }
            
            #calling Docker API
            response = requests.post("http://localhost:8000/analyse-route", json=payload)
            data = response.json()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Distance", f"{data['route_summary']['distance']/1000:.1f} km")
            with col2:
                st.metric("Est. Duration", f"{data['route_summary']['duration']/3600:.1f} hrs")
            with col3:
                risk_count = sum(1 for x in data['weather_checkpoints'] if x['risk status'] == 'DANGER')
                st.metric("Risk Factors", f"{risk_count} Alerts", delta_color="inverse")

            st.subheader("Route & Checkpoints")
            
            # Convert checkpoints to DataFrame for the Map
            map_data = pd.DataFrame(data['weather_checkpoints'])
            st.map(map_data, zoom=6)

            # 3. Detailed Checkpoint Analysis
            st.subheader(" AI Risk Analysis per Checkpoint")
            
            for i, point in enumerate(data['weather_checkpoints']):
                # Create a card-like look
                with st.expander(f"Checkpoint {i+1} (Temp: {point['temp']}°C)", expanded=True):
                    
                    c1, c2 = st.columns([1, 4])
                    
                    with c1:
                        if point['risk status'] == "DANGER":
                            st.error("DANGER")
                        else:
                            st.success("SAFE")
                            
                    with c2:
                        st.write(f"**Analysis:** {point['warning']}")
                        st.caption(f"Location: {point['lat']:.4f}, {point['lon']:.4f}")

        except Exception as e:
            st.error(f"Error connecting to Backend: {e}")
            st.info("Make sure your Docker Container is running on port 8000!")
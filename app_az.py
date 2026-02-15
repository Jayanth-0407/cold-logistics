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
            
            # calling Docker API
            api_url = "https://cold-logistics-backend-dbdne0hhc5fua9g4.koreacentral-01.azurewebsites.net/analyse-route"
            response = requests.post(api_url, json=payload)
            
            # --- 🚨 THE MAGIC DEBUGGER 🚨 ---
            # If Azure does not return a "200 OK" success code, stop and show the raw error!
            if response.status_code != 200:
                st.error(f"Backend Error: Status Code {response.status_code}")
                st.code(response.text) # This will print the raw HTML or error message!
                st.stop() # Stops the app here so it doesn't crash on response.json()
            # --------------------------------
            
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
            st.subheader("AI Risk Analysis per Checkpoint")
            
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
            st.info("Make sure your Docker Container is running properly on Azure!")

import streamlit as st
import langchain_file

# st.sidebar.title("Food Truck Business Planner")

st.sidebar.text(" ")

cuisine = st.sidebar.selectbox("Pick a cuisine", ("Indian", "American", "Japanese","Korean","Chinese","Arabic", "Italian", "Mexican"))
theme = st.sidebar.selectbox("Pick a theme", ("Diwali", "Holi", "Eid", "Summer Party", "Christmas", "Hawolleen"))
budget = st.sidebar.slider("Select Budget", min_value= 5_00_000, max_value= 20_00_000, value= 5_00_000)
target_location = st.sidebar.selectbox("Select Location", ("Delhi", "Mumbai", "Bengaluru", "Indore", "Chennai", "Hyderabad"))

main_placeholder = st.empty()

if cuisine:

    main_placeholder.text("Loading........")

    response = langchain_file.generate_truckname_menu_location(cuisine, theme, budget, target_location)
   
    main_placeholder.empty()
    
    locations = response['location'].strip().split("\n\n")
    budget = response['budget']

   
    html_code = f"""
    <h1 style = "color:orange;">Food Truck Business Planner</h1>
    """
    st.markdown(html_code, unsafe_allow_html=True)
    st.markdown("---")


    Title = response['truck_name']
    html_code = f"""
    <h2 style = "color:aqua;">{Title}</h2>
    """
    st.markdown(html_code, unsafe_allow_html=True)
    
    
    st.write(response['menu'])

    st.subheader("**Location**")
    for locate in locations:
        st.write(locate)   

    st.subheader("**Budget**")
    st.write(budget)

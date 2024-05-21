import streamlit as st
import requests
from snowflake.snowpark.context import get_active_session
st.set_page_config(layout='wide')
session = get_active_session()

def plan_trip(user_name, budget, preferences, travel_history):

    prompt = (f"{user_name} has a budget of ${budget} and likes {preferences}. "
              f"They have visited {travel_history}. Please suggest a personalized travel plan including destinations, flights, accommodations, and activities.")
    cortex_prompt = "'[INST] " + prompt + " [/INST]'"
    travel_plan = session.sql(f"select snowflake.cortex.complete('snowflake-arctic',{cortex_prompt}) as response").to_pandas().iloc[0]['RESPONSE']
    st.subheader("Personalized Travel Plan")
    st.write(travel_plan)

def plan_trip1(user_name, budget, preferences, travel_history, starting_location, end_locations):

    prompt = (f"{user_name} has a budget of ${budget} and likes {preferences}. "
              f"They have visited {travel_history}. They are starting their journey from {starting_location} "
              f"and wish to visit {end_locations}. Please suggest a personalized travel plan including destinations, flights, accommodations, and activities.")
    cortex_prompt = "'[INST] " + prompt + " [/INST]'"
    travel_plan = session.sql(f"select snowflake.cortex.complete('snowflake-arctic',{cortex_prompt}) as response").to_pandas().iloc[0]['RESPONSE']
    st.subheader("Personalized Travel Plan")
    st.write(travel_plan)

st.title("Travel Assistant")
st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRUhrPBzu1YF1bVxLP6zH7U60V-l9ydFxTfpUm5cFz_Pg&s")

st.header("Plan Your Travel")
user_name = st.text_input("Your Name", "")
budget = st.number_input("Budget ($)", min_value=0, step=100)
preferences = st.text_area("Preferences (e.g., beach, mountains, city)")
travel_history = st.text_area("Travel History (places you've visited)")
starting_location = st.text_area("Starting Location")
end_locations = st.text_area("Cities or Countries You Want to Visit (multiple)")

if st.button("Plan My Trip"):
    if not user_name or not budget or not preferences or not travel_history:
        st.error("Please fill in all the details.")
    else:
        if not starting_location or not end_locations:
            plan_trip(user_name, budget, preferences, travel_history)
        else:
            plan_trip1(user_name, budget, preferences, travel_history, starting_location, end_locations)


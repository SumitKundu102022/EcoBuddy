import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import calendar
from utils.chart_animations import create_animated_pie_chart

# Set unique title and layout for app.py
#st.set_page_config(page_title="EcoBuddy Dashboard", page_icon="🌍", layout="wide")

def run_app():
    # Function to get dynamic month names
    
    def get_dynamic_months():
        current_month = datetime.now().month
        current_year = datetime.now().year

        months = []
        years = []

        # Last three months and the current month
        for i in range(-3, 1):  # Include the current month and the previous two months
            month = (current_month + i - 1) % 12 + 1
            year = current_year + (current_month + i - 1) // 12
            months.append(calendar.month_name[month])
            years.append(year)

        # Check lengths of months and years
        if len(months) != len(years):
            print(f"Error: Length mismatch between months ({len(months)}) and years ({len(years)})")

        return months, years

    # Dynamic months and years for display
    dynamic_months, dynamic_years = get_dynamic_months()

    # Ensure that both lists have the same length
    assert len(dynamic_months) == len(dynamic_years), "Mismatch in lengths of months and years."

    # Initialize session state for visibility and form reset
    if "submitted" not in st.session_state:
        st.session_state.submitted = False

    if "reset_triggered" not in st.session_state:
        st.session_state.reset_triggered = False

    # Reset function
    def reset_data():
        st.session_state.submitted = False
        st.session_state.reset_triggered = True

    # Set wide layout and page name
    #st.set_page_config(layout="wide", page_title="EcoBuddy: Personalized Carbon Footprint Tracker", page_icon="🌍")

    # Title and Introduction
    st.title("EcoBuddy: Personalized Carbon Footprint Tracker")
    st.markdown("""
    Welcome to EcoBuddy! Calculate your carbon footprint, track your progress, and get actionable tips to reduce your environmental impact.

    Fill in the details below to get started.
    """)

    # Carbon Footprint Calculator
    st.header("Calculate Your Carbon Footprint")

    # Country Selection
    st.subheader("Select Your Country")
    # st.markdown("<h4 style='font-size:18px;'>Select Your Country</h4>", unsafe_allow_html=True)
    countries = {
        "China": {"transport": 0.45, "electricity": 1.0, "diet": {"Meat-heavy": 2.7, "Vegetarian": 1.9, "Vegan": 1.1}},
        "United States": {"transport": 0.411, "electricity": 0.92, "diet": {"Meat-heavy": 2.5, "Vegetarian": 1.7, "Vegan": 1.0}},
        "India": {"transport": 0.35, "electricity": 0.82, "diet": {"Meat-heavy": 2.3, "Vegetarian": 1.5, "Vegan": 0.9}, "waste": 0.1},
        "Russia": {"transport": 0.42, "electricity": 1.2, "diet": {"Meat-heavy": 2.6, "Vegetarian": 1.8, "Vegan": 1.0}}
    }
    selected_country = st.selectbox("Choose your country:", list(countries.keys()))

    # Retrieve emission factors for the selected country
    EMISSION_FACTORS = countries[selected_country]

    # Input Form
    with st.form("footprint_form"):
        st.subheader("Daily Habits")

        # Unit for distance based on the country
        distance_unit = "km" if selected_country == "India" else "miles"
        transportation = st.selectbox(
            f"How do you usually commute? ({distance_unit})",
            ("Car", "Public Transport", "Bike", "Walk", "Electric Vehicle")
        )
        distance = st.slider(f"Average distance traveled per day ({distance_unit}):", 0, 100, 10)

        electricity = st.slider("Monthly electricity usage (kWh):", 0, 2000, 500)
        diet = st.selectbox(
            "What is your primary diet type?",
            ("Meat-heavy", "Vegetarian", "Vegan")
        )

        # Additional input for waste, only for India
        waste_input = 0
        if selected_country == "India":
            waste_input = st.slider("Average monthly waste generated (kg):", 0, 100, 10)

        submitted = st.form_submit_button("Calculate")
        if submitted:
            st.session_state.submitted = True

    # Display Results if Submitted
    if st.session_state.submitted:
        # Adjust distance for kilometers if India is selected
        distance_conversion_factor = 1.609 if selected_country != "India" else 1  # Convert miles to km for non-India
        adjusted_distance = distance * distance_conversion_factor

        # Calculate Carbon Footprint
        transport_footprint = adjusted_distance * EMISSION_FACTORS["transport"] * 30 / 1000  # Monthly
        electricity_footprint = electricity * EMISSION_FACTORS["electricity"] / 1000
        diet_footprint = EMISSION_FACTORS["diet"][diet] * 30
        waste_footprint = 0

        if selected_country == "India":
            waste_footprint = waste_input * EMISSION_FACTORS["waste"] / 1000  # Waste emissions in tons

        total_footprint = transport_footprint + electricity_footprint + diet_footprint + waste_footprint

        # Create two columns for displaying results
        col1, col2 = st.columns(2)

        with col1:
            # Step 1: Display Results
            st.header("Your Results")
            st.metric("Your Monthly Carbon Footprint (tons)", f"{total_footprint:.2f}")

            # Visualize Contributions
            categories = ["Transportation", "Electricity", "Diet"]
            footprints = [transport_footprint, electricity_footprint, diet_footprint]

            if selected_country == "India":
                categories.append("Waste")
                footprints.append(waste_footprint)

            df = pd.DataFrame({
                "Category": categories,
                "Footprint (tons)": footprints
            })
            fig = px.pie(df, values="Footprint (tons)", names="Category", title="Carbon Footprint Breakdown")
            st.plotly_chart(fig)

        with col2:
            # Step 2: Recommendations
            st.header("Reduce Your Carbon Footprint")
            st.subheader("Personalized Tips")
            tips = []

            if transportation == "Car":
                tips.append("Carpool or switch to public transport to reduce emissions.")
            if electricity > 500:
                tips.append("Consider using energy-efficient appliances or solar panels.")
            if diet == "Meat-heavy":
                tips.append("Try incorporating more plant-based meals into your diet.")
            if selected_country == "India" and waste_input > 50:
                tips.append("Reduce waste by recycling and composting.")

            if not tips:
                st.write("Great job! You're already leading an eco-friendly lifestyle.")
            else:
                for tip in tips:
                    st.write(f"- {tip}")

        # Step 3: Progress Tracker
        st.header("Track Your Progress")
        st.subheader("Your Carbon Footprint Over Time")
        # Simulated Data for the Dynamic Months
        progress_data = {
            "Month": dynamic_months,
            "Year": dynamic_years,
            "Carbon Footprint (tons)": [
                total_footprint * 0.95,  # Simulate last month's reduction
                total_footprint,        # Current month
                total_footprint * 1.05, # Simulate potential increase next month
                total_footprint * 1.1   # Simulate future projection
            ],
        }

        df_progress = pd.DataFrame(progress_data)

        # Display Progress Chart
        fig = px.bar(
            df_progress,
            x="Month",
            y="Carbon Footprint (tons)",
            color="Year",
            title="Carbon Footprint Progress",
            text="Carbon Footprint (tons)",
        )
        st.plotly_chart(fig)

        # Reset Button
        if st.button("Reset"):
            reset_data()


# # Ensure `st.set_page_config` is only run when app.py is executed directly
# if __name__ == "__main__":
#     st.set_page_config(page_title="EcoBuddy: Personalized Carbon Footprint Tracker", page_icon="🌍", layout="wide")
#     run_app()
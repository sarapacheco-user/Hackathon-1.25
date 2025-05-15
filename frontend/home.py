import streamlit as st

# Defines page layout
st.set_page_config(page_title="Main App", layout="centered")

# Sidebar setup
with st.sidebar:
    st.title("App Navegation")
    st.markdown("This application validates donations and exposes statistics on the excedent food")
    st.image("frontend/shareBiteLogo.png", caption=" ", use_container_width=True)
    
# Main content of the page
st.title("Welcome to ShareBite!")

st.markdown("""
    This application was developed to assist in the validation of food donations and in visualizing data on the quantity of products available for donation.

    Navigate using the side menu to access the Feasibility Form or the Statistics Dashboard pages.

    **When to use the Dashboard?** Use the dashboard when you want to view data on leftover food items.

    **When to use the Form?** Use the form when you want to add food items to the database, verifying whether they are validated by ANVISA.
            
""")

st.image("frontend/shareBiteLogo.png", caption="", use_container_width=True)

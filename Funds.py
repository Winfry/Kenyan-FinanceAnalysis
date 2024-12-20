import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# Load the datasets
credits_df = pd.read_csv('Credits_Kenya.csv')
investments_df = pd.read_csv('Investment_Projects_Kenya.csv')
loans_df = pd.read_csv('Loans_Kenya.csv')

# Streamlit App
st.title("Kenya Financial Insights")
st.sidebar.header("🔍 Filters")

# Sidebar filters
view_option = st.sidebar.radio("Choose a view:", ["All Data", "Credits", "Investments", "Loans", "Insights Panel"])

# All Data View
if view_option == "All Data":
    st.header("All Datasets Overview")
    st.subheader("Credits Dataset")
    st.dataframe(credits_df)

    st.subheader("Investments Dataset")
    st.dataframe(investments_df)

    st.subheader("Loans Dataset")
    st.dataframe(loans_df)

# Credits View
if view_option == "Credits":
    st.header("Credits Dataset")
    st.dataframe(credits_df)
    
    # Filter by year and facility type
    year = st.sidebar.selectbox("Select Year", sorted(credits_df['Year'].dropna().unique()))
    facility_type = st.sidebar.selectbox("Select Facility Type", credits_df['Credit Facility Type'].dropna().unique())
    
    filtered_credits = credits_df[(credits_df['Year'] == year) & (credits_df['Credit Facility Type'] == facility_type)]
    st.subheader(f"Credits Data for {facility_type} in {year}")
    st.dataframe(filtered_credits)

# Investments View
if view_option == "Investments":
    st.header("Investments Dataset")
    st.dataframe(investments_df)
    
    # Filter by sector or county
    sector = st.sidebar.selectbox("Select Sector", investments_df['Sector'].dropna().unique())
    county = st.sidebar.selectbox("Select County", investments_df['County'].dropna().unique())
    
    filtered_investments = investments_df[(investments_df['Sector'] == sector) & (investments_df['County'] == county)]
    st.subheader(f"Investment Projects in {sector} Sector, {county}")
    st.dataframe(filtered_investments)

# Loans View
if view_option == "Loans":
    st.header("Loans Dataset")
    st.dataframe(loans_df)
    
    # Filter by year
    loan_year = st.sidebar.selectbox("Select Year", sorted(loans_df['Year'].dropna().unique()))
    
    filtered_loans = loans_df[loans_df['Year'] == loan_year]
    st.subheader(f"Loans Data for {loan_year}")
    st.dataframe(filtered_loans)

# Insights Panel
if view_option == "Insights Panel":
    st.header("Insights Panel")

    # Total statistics
    total_credits = credits_df['Amount'].sum()
    total_investments = investments_df['Investment Amount'].sum()
    total_loans = loans_df['Loan Amount'].sum()
    
    st.subheader("Overall Financial Totals")
    st.write(f"**Total Credits:** KES {total_credits:,.2f}")
    st.write(f"**Total Investments:** KES {total_investments:,.2f}")
    st.write(f"**Total Loans:** KES {total_loans:,.2f}")

    # Comparative Trends
    st.subheader("Yearly Trends")
    credits_yearly = credits_df.groupby('Year')['Amount'].sum().reset_index()
    investments_yearly = investments_df.groupby('Start Year')['Investment Amount'].sum().reset_index()
    loans_yearly = loans_df.groupby('Year')['Loan Amount'].sum().reset_index()

    credits_chart = alt.Chart(credits_yearly).mark_line().encode(
        x='Year:O', y='Amount:Q', tooltip=['Year', 'Amount']
    ).properties(title="Credits Over Years")

    investments_chart = alt.Chart(investments_yearly).mark_line().encode(
        x='Start Year:O', y='Investment Amount:Q', tooltip=['Start Year', 'Investment Amount']
    ).properties(title="Investments Over Years")

    loans_chart = alt.Chart(loans_yearly).mark_line().encode(
        x='Year:O', y='Loan Amount:Q', tooltip=['Year', 'Loan Amount']
    ).properties(title="Loans Over Years")

    st.altair_chart(credits_chart, use_container_width=True)
    st.altair_chart(investments_chart, use_container_width=True)
    st.altair_chart(loans_chart, use_container_width=True)



import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import plotly.express as px
import plotly.graph_objects as go

# Title of the web app
st.title("Kenya Loans Prediction and Recommendation System")

# File uploader
uploaded_file = st.file_uploader("Upload the Loans Dataset (CSV format)", type=["csv"])

if uploaded_file is not None:
    # Load the dataset
    loans_df = pd.read_csv(uploaded_file)

    # Check if 'Year' column exists, add it if missing
    if 'Year' not in loans_df.columns:
        loans_df['Year'] = 2020  # Default value (or customize as needed)

    # Display a description of the dataset
    st.write("This app predicts loan repayment and recommends loan types based on your input.")

    # Show the dataset and basic stats
    if st.checkbox('Show raw data'):
        st.write(loans_df)

    st.write("Summary of the dataset:")
    st.write(loans_df.describe())

    # Section 1: Loan Prediction
    st.header("Loan Repayment Prediction")

    # User inputs for prediction
    principal_amount = st.number_input("Enter principal loan amount", min_value=0, step=1000)
    interest_rate = st.number_input("Enter annual interest rate (in %)", min_value=0.0, step=0.1)
    years = st.number_input("Enter loan term in years", min_value=1, step=1)

    # Prediction logic: Simple loan repayment calculation
    if st.button("Predict Total Repayment"):
        total_repayment = principal_amount * (1 + (interest_rate / 100) * years)
        st.write(f"The total repayment amount is: ${total_repayment:,.2f}")

    # Section 2: Loan Recommendation
    st.header("Loan Type Recommendation")

    # User input for recommendation
    loan_purpose = st.selectbox("Select the purpose of the loan", ['Education', 'Business', 'Personal', 'Housing'])
    loan_term = st.number_input("Enter desired loan term in years", min_value=1, step=1)

    # Simple recommendation logic (example)
    recommended_loan_type = None
    if loan_purpose == 'Education':
        recommended_loan_type = 'Student Loan'
    elif loan_purpose == 'Business':
        recommended_loan_type = 'Business Loan'
    elif loan_purpose == 'Personal':
        recommended_loan_type = 'Personal Loan'
    elif loan_purpose == 'Housing':
        recommended_loan_type = 'Mortgage'

    st.write(f"Recommended Loan Type: {recommended_loan_type}")

    # Section 3: Interactive Data Visualization
    st.header("Loan Data Insights")

    # Display loan distribution
    st.subheader("Loan Amount Distribution")
    if 'Original Principal Amount (US$)' in loans_df.columns:
        st.bar_chart(loans_df['Original Principal Amount (US$)'])
        fig = px.histogram(loans_df, x='Original Principal Amount (US$)', title="Loan Amount Distribution", nbins=20)
        st.plotly_chart(fig)
    else:
        st.warning("'Original Principal Amount (US$)' column not found for distribution visualization.")

    # Display project name insights with Plotly
    st.subheader("Project Names and Signing Dates")
    if 'Project Name' in loans_df.columns and 'Agreement Signing Date' in loans_df.columns:
        fig = px.scatter(loans_df, x='Agreement Signing Date', y='Original Principal Amount (US$)',
                         color='Project Name', title="Project Signing Dates and Loan Amounts")
        st.plotly_chart(fig)
    else:
        st.warning("Required columns 'Project Name' or 'Agreement Signing Date' not found.")

    # Additional Visualizations
    st.subheader("Loan Amount Over Time")
    if 'Year' in loans_df.columns and 'Original Principal Amount (US$)' in loans_df.columns:
        fig = px.line(loans_df, x='Year', y='Original Principal Amount (US$)', title="Loan Amount Over Years")
        st.plotly_chart(fig)
    else:
        st.warning("Columns 'Year' or 'Original Principal Amount (US$)' not found for time series visualization.")
else:
    st.warning("Please upload the dataset to proceed.")

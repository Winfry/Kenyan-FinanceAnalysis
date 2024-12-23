import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
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

    # Enhanced prediction logic
    if principal_amount > 0 and interest_rate > 0 and years > 0:
         if st.button("Predict Total Repayment"):
            # Simple interest formula
            total_interest = (principal_amount * interest_rate * years) / 100
            total_repayment = principal_amount + total_interest
            # Breakdown display
            st.subheader("Prediction Results")
            st.write(f"### Principal Amount: ${principal_amount:,.2f}")
            st.write(f"### Total Interest: ${total_interest:,.2f}")
            st.write(f"### Total Repayment Amount: ${total_repayment:,.2f}")

            # Visualization of repayment breakdown
            repayment_fig = px.pie(
                names=["Principal", "Interest"],
                values=[principal_amount, total_interest],
                title="Repayment Breakdown",
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(repayment_fig)    

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
    
    # Filters for interactivity
    borrower = st.selectbox("Select Borrower", options=loans_df['Borrower'].unique())
    loan_type = st.selectbox("Select Loan Type", options=loans_df['Loan Type'].unique())
    guarantor = st.selectbox("Select Guarantor", options=loans_df['Guarantor'].unique())

    # Filter the dataframe based on user selections
    filtered_df = loans_df[(loans_df['Borrower'] == borrower) & 
                       (loans_df['Loan Type'] == loan_type) & 
                       (loans_df['Guarantor'] == guarantor)]

    # Display loan distribution
    st.subheader("Loan Amount Distribution")
    if 'Original Principal Amount (US$)' in filtered_df.columns:
        st.bar_chart(filtered_df['Original Principal Amount (US$)'])
        fig = px.histogram(filtered_df, x='Original Principal Amount (US$)', title="Loan Amount Distribution", nbins=20)
        st.plotly_chart(fig)
    else:
        st.warning("'Original Principal Amount (US$)' column not found for distribution visualization.")

    # Display project name insights with Plotly
    st.subheader("Project Names and Signing Dates")
    if 'Project Name' in filtered_df.columns and 'Agreement Signing Date' in filtered_df.columns:
        fig = px.scatter(filtered_df, x='Agreement Signing Date', y='Original Principal Amount (US$)',
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
        
     # Correlation heatmap
    st.subheader("Correlation Heatmap")
    numerical_data = loans_df.select_dtypes(include=[np.number])

    if numerical_data.shape[1] > 1:
        corr = numerical_data.corr()
        fig = px.imshow(
            corr,
            text_auto=True,
            title="Correlation Heatmap",
            color_continuous_scale="Viridis"
        )
        for i in range(len(corr.columns)):
            for j in range(len(corr.columns)):
                fig.add_annotation(
                    text=f"{corr.iloc[i, j]:.2f}",
                    x=j,
                    y=i,
                    showarrow=False,
                    font=dict(color="white" if abs(corr.iloc[i, j]) > 0.5 else "black")
                )
        st.plotly_chart(fig)
    else:
        st.warning("Not enough numerical columns for correlation heatmap.")   
        
else:
    st.warning("Please upload the dataset to proceed.")

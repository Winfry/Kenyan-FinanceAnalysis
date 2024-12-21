import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Title of the web app
st.title("Kenya Loans Prediction and Recommendation System")

# File uploader
uploaded_file = st.file_uploader("Upload the Loans Dataset (CSV format)", type=["csv"])

if uploaded_file is not None:
    # Load the dataset
    loans_df = pd.read_csv("FundsData/Updated_Loans_Kenya.csv")

    # Check if 'Year' column exists, add it if missing
    if 'Year' not in loans_df.columns:
        loans_df['Year'] = 2020  # Default value (or customize as needed)

    # Display a description of the dataset
    st.write("This app predicts loan approval and recommends loan types based on your input.")

    # Show the dataset and basic stats
    if st.checkbox('Show raw data'):
        st.write(loans_df)

    st.write("Summary of the dataset:")
    st.write(loans_df.describe())

    # Section 1: Loan Prediction
    st.header("Loan Prediction")

    # User inputs for prediction
    loan_amount = st.number_input("Enter loan amount", min_value=0, step=1000)
    income = st.number_input("Enter annual income", min_value=0)
    loan_type = st.selectbox("Select loan type", loans_df['Loan Type'].unique())

    # Preprocess the data
    X = loans_df[['Original Principal Amount (US$)', 'Income', 'Loan Type']]  # Modify based on your dataset columns
    y = loans_df['Loan Status']  # 0 for rejected, 1 for approved

    # Convert categorical to numeric
    X = pd.get_dummies(X)

    # Train the model (just for illustration, should be done outside the app for efficiency)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    # Make a prediction based on user input
    user_input = pd.DataFrame([[loan_amount, income, loan_type]], columns=['Original Principal Amount (US$)', 'Income', 'Loan Type'])
    user_input = pd.get_dummies(user_input)  # Ensure same format as training data
    user_input = user_input.reindex(columns=X.columns, fill_value=0)  # Align columns with training data
    user_prediction = model.predict(user_input)

    # Display prediction result
    if user_prediction[0] == 1:
        st.success("Loan Approved!")
    else:
        st.error("Loan Rejected")

    # Section 2: Loan Recommendation
    st.header("Loan Type Recommendation")

    # User input for recommendation
    user_income = st.number_input("Enter your income for loan recommendation", min_value=0)
    user_credit_history = st.selectbox("Select your credit history", ['Good', 'Average', 'Poor'])

    # Simple recommendation logic (example)
    if user_income < 20000:
        recommended_loan_type = 'Personal Loan'
    elif user_income < 50000:
        recommended_loan_type = 'Business Loan'
    else:
        recommended_loan_type = 'Mortgage'

    st.write(f"Recommended Loan Type: {recommended_loan_type}")

    # Section 3: Interactive Data Visualization
    st.header("Loan Data Insights")

    # Display loan distribution
    st.subheader("Loan Amount Distribution")
    if 'Original Principal Amount (US$)' in loans_df.columns:
        st.bar_chart(loans_df['Original Principal Amount (US$)'])
    else:
        st.warning("'Original Principal Amount (US$)' column not found for distribution visualization.")
else:
    st.warning("Please upload the dataset to proceed.")


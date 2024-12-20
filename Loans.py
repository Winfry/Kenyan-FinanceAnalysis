import streamlit as st
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# Load your dataset
df = pd.read_csv("loan_data.csv")

# Display a description of the dataset
st.title("Loan Prediction and Recommendation System")
st.write("This app predicts loan approval and recommends loan types based on your input.")

# Show the dataset and basic stats
if st.checkbox('Show raw data'):
    st.write(df)

st.write("Summary of the dataset:")
st.write(df.describe())

# Section 1: Loan Prediction
st.header("Loan Prediction")

# User inputs for prediction
loan_amount = st.number_input("Enter loan amount", min_value=0, step=1000)
income = st.number_input("Enter annual income", min_value=0)
loan_type = st.selectbox("Select loan type", df['Loan Type'].unique())

# Preprocess the data
X = df[['loan_amount', 'income', 'loan_type']]  # Modify based on your dataset columns
y = df['loan_status']  # 0 for rejected, 1 for approved

# Convert categorical to numeric
X = pd.get_dummies(X)

# Train the model (just for illustration, should be done outside the app for efficiency)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Make a prediction based on user input
user_input = pd.DataFrame([[loan_amount, income, loan_type]], columns=X.columns)
user_input = pd.get_dummies(user_input)  # Ensure same format as training data
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
st.bar_chart(df['loan_amount'])

# Other charts can be added depending on the columns in your dataset

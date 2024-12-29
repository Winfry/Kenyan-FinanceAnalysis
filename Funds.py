import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Streamlit App
st.title("Kenya Financial Insights")
st.sidebar.title("🔍 Filter What Kenyan Data You would Like To Interact With")

# Upload the datasets
st.sidebar.header("Upload Datasets")
credits_file = st.sidebar.file_uploader("Upload Credits Dataset", type="csv")
investments_file = st.sidebar.file_uploader("Upload Investments Dataset", type="csv")
loans_file = st.sidebar.file_uploader("Upload Loans Dataset", type="csv")


def check_columns(df, required_columns):
    missing = [col for col in required_columns if col not in df.columns]
    return missing

if credits_file or investments_file or loans_file:
    try:
        credits_df = pd.read_csv(credits_file) if credits_file else None
        investments_df = pd.read_csv(investments_file) if investments_file else None
        loans_df = pd.read_csv(loans_file) if loans_file else None

        # Choose dataset to interact with
        dataset_option = st.sidebar.selectbox("Choose a dataset to interact with:", ["Credits", "Investments", "Loans"])

        if dataset_option == "Credits" and credits_df is not None:
            st.header("Credits Dataset")
            st.dataframe(credits_df)

            required_columns = ['Year', 'Credit Facility Type']
            missing_columns = check_columns(credits_df, required_columns)

            if not missing_columns:
                year = st.sidebar.selectbox("Select Year", sorted(credits_df['Year'].dropna().unique()))
                facility_type = st.sidebar.selectbox("Select Facility Type", credits_df['Credit Facility Type'].dropna().unique())

                filtered_credits = credits_df[(credits_df['Year'] == year) & (credits_df['Credit Facility Type'] == facility_type)]
                st.subheader(f"Credits Data for {facility_type} in {year}")
                st.dataframe(filtered_credits)

                # Interactive Prediction System for Credits
                st.subheader("Credits Recommendation System")
                if 'Credit Amount' in credits_df.columns and 'Interest Rate' in credits_df.columns and 'Duration' in credits_df.columns:
                    st.write("Provide input for credit recommendations:")

                    input_credit_amount = st.number_input("Credit Amount (Ksh)", min_value=0.0, value=100000.0, step=10000.0)
                    input_credit_rate = st.number_input("Interest Rate (%)", min_value=0.0, value=12.0, step=0.5)
                    input_credit_duration = st.number_input("Duration (Years)", min_value=1, value=5, step=1)

                    # Prepare data for prediction
                    credits_df = credits_df.dropna(subset=['Credit Amount', 'Interest Rate', 'Duration'])
                    X = credits_df[['Credit Amount', 'Interest Rate', 'Duration']]
                    y = credits_df['Year']

                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                    model = LinearRegression()
                    model.fit(X_train, y_train)

                    # Predict
                    prediction = model.predict(np.array([[input_credit_amount, input_credit_rate, input_credit_duration]]))

                    st.write(f"Predicted Year for Credit Approval: {int(prediction[0])}")

                    # Display model performance
                    y_pred = model.predict(X_test)
                    mse = mean_squared_error(y_test, y_pred)
                    st.write(f"Model Mean Squared Error: {mse:.2f}")
                else:
                    st.error("The Credits dataset is missing required columns 'Credit Amount', 'Interest Rate', or 'Duration'.")
            else:
                st.error(f"The Credits dataset is missing required columns: {', '.join(missing_columns)}")

        elif dataset_option == "Investments" and investments_df is not None:
            st.header("Investments Dataset")
            st.dataframe(investments_df)

            required_columns = ['Sector', 'County']
            missing_columns = check_columns(investments_df, required_columns)

            if not missing_columns:
                sector = st.sidebar.selectbox("Select Sector", investments_df['Sector'].dropna().unique())
                county = st.sidebar.selectbox("Select County", investments_df['County'].dropna().unique())

                filtered_investments = investments_df[(investments_df['Sector'] == sector) & (investments_df['County'] == county)]
                st.subheader(f"Investment Projects in {sector} Sector, {county}")
                st.dataframe(filtered_investments)

                # Interactive Prediction System for Investments
                st.subheader("Investments Recommendation System")
                if 'Investment Amount' in investments_df.columns and 'Return Rate' in investments_df.columns and 'Duration' in investments_df.columns:
                    st.write("Provide input for investment recommendations:")

                    input_investment_amount = st.number_input("Investment Amount (Ksh)", min_value=0.0, value=200000.0, step=10000.0)
                    input_return_rate = st.number_input("Return Rate (%)", min_value=0.0, value=8.0, step=0.5)
                    input_investment_duration = st.number_input("Duration (Years)", min_value=1, value=10, step=1)

                    # Prepare data for prediction
                    investments_df = investments_df.dropna(subset=['Investment Amount', 'Return Rate', 'Duration'])
                    X = investments_df[['Investment Amount', 'Return Rate', 'Duration']]
                    y = investments_df['Year']  # Assuming 'Year' is a target variable for illustration

                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                    model = LinearRegression()
                    model.fit(X_train, y_train)

                    # Predict
                    prediction = model.predict(np.array([[input_investment_amount, input_return_rate, input_investment_duration]]))

                    st.write(f"Predicted Year for Investment Return: {int(prediction[0])}")

                    # Display model performance
                    y_pred = model.predict(X_test)
                    mse = mean_squared_error(y_test, y_pred)
                    st.write(f"Model Mean Squared Error: {mse:.2f}")
                else:
                    st.error("The Investments dataset is missing required columns 'Investment Amount', 'Return Rate', or 'Duration'.")
            else:
                st.error(f"The Investments dataset is missing required columns: {', '.join(missing_columns)}")

        elif dataset_option == "Loans" and loans_df is not None:
            st.header("Loans Dataset")
            st.dataframe(loans_df)

            required_columns = ['Year']
            missing_columns = check_columns(loans_df, required_columns)
            # Check if 'Year' column exists, add it if missing
            if 'Year' not in loans_df.columns:
                loans_df['Year'] = 2020  # Default value (or customize as needed)

            # Save the updated dataset
            loans_df.to_csv("FundsData/Updated_Loans_Kenya.csv", index=False)


            if not missing_columns:
                loan_year = st.sidebar.selectbox("Select Year", sorted(loans_df['Year'].dropna().unique()))

                filtered_loans = loans_df[loans_df['Year'] == loan_year]
                st.subheader(f"Loans Data for {loan_year}")
                st.dataframe(filtered_loans)

                # Interactive Prediction System for Loans
                st.subheader("Loan Recommendation System")
                if 'Loan Amount' in loans_df.columns and 'Interest Rate' in loans_df.columns and 'Duration' in loans_df.columns:
                    st.write("Provide input for loan recommendations:")

                    input_amount = st.number_input("Loan Amount (Ksh)", min_value=0.0, value=50000.0, step=5000.0)
                    input_rate = st.number_input("Interest Rate (%)", min_value=0.0, value=10.0, step=0.5)
                    input_duration = st.number_input("Duration (Years)", min_value=1, value=5, step=1)

                    # Prepare data for prediction
                    loans_df = loans_df.dropna(subset=['Loan Amount', 'Interest Rate', 'Duration'])
                    X = loans_df[['Loan Amount', 'Interest Rate', 'Duration']]
                    y = loans_df['Year']  # Assuming 'Year' is a target variable for illustration

                    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                    model = LinearRegression()
                    model.fit(X_train, y_train)

                    # Predict
                    prediction = model.predict(np.array([[input_amount, input_rate, input_duration]]))

                    st.write(f"Predicted Year for Loan Approval: {int(prediction[0])}")

                    # Display model performance
                    y_pred = model.predict(X_test)
                    mse = mean_squared_error(y_test, y_pred)
                    st.write(f"Model Mean Squared Error: {mse:.2f}")
                else:
                    st.error("The Loans dataset is missing required columns 'Loan Amount', 'Interest Rate', or 'Duration'.")

            else:
                st.error(f"The Loans dataset is missing required columns: {', '.join(missing_columns)}")

        else: 
            st.warning(f"Please upload the {dataset_option} dataset to interact with it.")

    except Exception as e:
        st.error(f"An error occurred while processing the files: {e}")




 
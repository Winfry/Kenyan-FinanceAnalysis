import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load datasets
def load_data():
    loans = pd.read_csv('FundsData\Loans_Kenya.csv')
    projects = pd.read_csv('FundsData\Investment_Projects_Kenya.csv')
    credits = pd.read_csv('FundsData\Credits_Kenya.csv')
    return loans, projects, credits

# App title
st.title("Kenyan Finance Analytics Dashboard")
st.markdown("Analyze loans, Investment projects, and credits across different locations.")

# Load data
df_loans, df_investments , df_credits = load_data()

# Filter by Location
st.sidebar.header("🔍 Filters")
# Check if 'Location' column exists and handle missing values
locations = set()
if 'Location' in df_loans.columns:
    locations.update(df_loans['Location'].dropna().unique())

if 'Location' in df_investments.columns:
    locations.update(df_investments['Location'].dropna().unique())

if 'Location' in df_credits.columns:
    locations.update(df_credits['Location'].dropna().unique())

# Convert to a sorted list before passing to the selectbox
selected_location = st.sidebar.selectbox("Select a Location:", sorted(locations))

# Convert to a sorted list before passing to the selectbox
selected_location = st.sidebar.selectbox("Select a Location:", sorted(locations))

# Filter datasets based on location
filtered_loans = loans_df[loans_df['Location'] == selected_location]
filtered_projects = projects_df[projects_df['Location'] == selected_location]
filtered_credits = credits_df[credits_df['Location'] == selected_location]

# Display Loans Dataset
st.header("Loans Data")
st.dataframe(filtered_loans)
st.write(f"Total Loans in {selected_location}: {len(filtered_loans)}")

# Visualization: Loan Amounts
if not filtered_loans.empty:
    st.subheader("Loan Amount Distribution")
    fig, ax = plt.subplots()
    filtered_loans['Amount'].plot(kind='hist', bins=20, ax=ax, color='skyblue', edgecolor='black')
    ax.set_title("Loan Amount Distribution")
    ax.set_xlabel("Amount")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

# Display Investment Projects Dataset
st.header("Investment Projects Data")
st.dataframe(filtered_projects)
st.write(f"Total Projects in {selected_location}: {len(filtered_projects)}")

# Visualization: Budget by Sector
if not filtered_projects.empty:
    st.subheader("Project Budget by Sector")
    sector_budget = filtered_projects.groupby('Sector')['Budget'].sum()
    fig, ax = plt.subplots()
    sector_budget.plot(kind='bar', ax=ax, color='orange', edgecolor='black')
    ax.set_title("Total Budget by Sector")
    ax.set_xlabel("Sector")
    ax.set_ylabel("Total Budget")
    st.pyplot(fig)

# Display Credits Dataset
st.header("Credits Data")
st.dataframe(filtered_credits)
st.write(f"Total Credits in {selected_location}: {len(filtered_credits)}")

# Visualization: Credit Approval Status
if not filtered_credits.empty:
    st.subheader("Credit Approval Status")
    approval_status = filtered_credits['Approval_Status'].value_counts()
    fig, ax = plt.subplots()
    approval_status.plot(kind='pie', ax=ax, autopct='%1.1f%%', colors=['lightgreen', 'salmon'], startangle=90)
    ax.set_ylabel("")
    ax.set_title("Credit Approval Status")
    st.pyplot(fig)

# Download Filtered Data
st.sidebar.header("Download Filtered Data")
if st.sidebar.button("Download Loans Data"):
    filtered_loans.to_csv("Filtered_Loans.csv", index=False)
    st.sidebar.success("Loans data downloaded!")

if st.sidebar.button("Download Projects Data"):
    filtered_projects.to_csv("Filtered_Projects.csv", index=False)
    st.sidebar.success("Projects data downloaded!")

if st.sidebar.button("Download Credits Data"):
    filtered_credits.to_csv("Filtered_Credits.csv", index=False)
    st.sidebar.success("Credits data downloaded!")

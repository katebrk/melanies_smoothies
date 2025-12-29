import streamlit as st

st.title("Central Bank Interest Rates")

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# User Inputs
central_bank = st.selectbox("Choose Central Bank", ("ECB", "BoE"))
interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, value=2.15, step=0.01, format="%.2f")
last_change_date = st.date_input("Last Change Date")

# Submit Button
if st.button("Submit Rate"):
    # Insert into Snowflake
    try:
        # We'll use a parametrized query for security (SQL injection prevention)
        insert_query = """
            INSERT INTO INTEREST_RATES.PUBLIC.CENTRAL_BANK_RATES (CENTRAL_BANK, INTEREST_RATE, RATE_DATE)
            VALUES (?, ?, ?)
        """
        session.sql(insert_query, params=[central_bank, interest_rate, last_change_date]).collect()

        st.success(f"Successfully inserted: {central_bank}, {interest_rate}%, {last_change_date}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

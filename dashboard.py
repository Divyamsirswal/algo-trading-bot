import streamlit as st
import json
import os

ORDERS_FILE = "app/orders.json"

def load_orders():
    try:
        with open(ORDERS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def main():
    st.title("Trading Bot Dashboard")

    orders = load_orders()
    if orders:
        st.write("### Recent Orders")
        for order in sorted(orders, key=lambda x: x["price"]):
            st.json(order)
    else:
        st.write("No orders found.")

if __name__ == "__main__":
    st.set_page_config(page_title="Trading Bot Dashboard", layout="wide")
    main()

import streamlit as st
import json
import time

ORDERS_FILE = "app/orders.json"

def load_orders():
    try:
        with open(ORDERS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

st.title("📊 Trading Bot Dashboard")

while True:
    orders = load_orders()
    
    st.write("### Recent Orders")
    if orders:
        for order in sorted(orders, key=lambda x: x["price"]):
            st.json(order)
    else:
        st.write("⚠️ No orders yet. Waiting for stock prices...")

    time.sleep(2)  # Refresh every 2 seconds

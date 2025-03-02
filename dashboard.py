import time
import streamlit as st
import redis
import json
import pandas as pd
import matplotlib.pyplot as plt

REFRESH_INTERVAL = 10 
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

st.set_page_config(page_title="Trading Bot Dashboard", layout="wide")

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

current_time = time.time()
if current_time - st.session_state.last_refresh >= REFRESH_INTERVAL:
    st.session_state.last_refresh = current_time
    
    st.set_query_params(refresh=str(current_time))
    
    st.experimental_rerun()

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

st.title("Trading Bot Dashboard")
st.write(f"Auto-refresh interval: {REFRESH_INTERVAL} seconds")

keys = r.keys("order:*")
orders = []

for key in keys:
    data = json.loads(r.get(key))
    orders.append(data)

if orders:
    st.subheader("Recent Orders")
    
    orders = sorted(orders, key=lambda x: x.get("timestamp", 0))
    
    for order in orders:
        st.json(order)
    
    df = pd.DataFrame(orders)
    
    if "price" in df.columns and "timestamp" in df.columns:
        try:
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
        except ValueError:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        
        df.sort_values("timestamp", inplace=True)
        
        fig, ax = plt.subplots()
        ax.plot(df["timestamp"], df["price"], marker="o")
        ax.set_title("Price Over Time")
        ax.set_xlabel("Timestamp")
        ax.set_ylabel("Price")
        st.pyplot(fig)
    else:
        st.write("No valid price/timestamp data to plot.")
else:
    st.write("No orders found in Redis.")

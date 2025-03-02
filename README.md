# Algorithmic Trading Bot

## Overview
The Algorithmic Trading Bot is a full-stack project designed to simulate real-time trading using a moving average crossover strategy with built-in risk management. The project integrates multiple technologies including FastAPI for the backend, Kafka for messaging, Redis for caching and order logging, and Streamlit for interactive dashboard visualization. A backtesting module is also provided to simulate and evaluate strategy performance against historical data.

## Features
- **Real-Time Data Ingestion:**  
  Connects to a dummy WebSocket server (or a real API) for live stock price data.
- **Trading Strategy:**  
  Implements a moving average crossover strategy with risk management (including stop-loss).
- **Order Processing:**  
  Uses Kafka to simulate order execution and Redis to log orders.
- **Interactive Dashboard:**  
  Built with Streamlit for real-time visualization of trade orders and price trends.
- **Backtesting Module:**  
  Simulates strategy performance using historical data stored in CSV format.
- **Containerization:**  
  Docker and Docker Compose support for seamless deployment.
- **Robust Error Handling & Monitoring:**  
  Advanced logging, reconnection logic, and health-check endpoints.

## Technologies Used
- **Backend:** Python, FastAPI, Uvicorn
- **Real-Time Data:** WebSockets
- **Messaging:** Kafka (kafka-python)
- **Caching & Logging:** Redis
- **Dashboard & Visualization:** Streamlit, Pandas, Matplotlib
- **Containerization:** Docker, Docker Compose
- **Backtesting:** CSV-based data simulation

## Project Structure
```plaintext
algo-trading-bot/
├── app/
│   ├── __init__.py           
│   ├── main.py                
│   ├── websocket_client.py   
│   ├── trading_logic.py      
│   ├── kafka_producer.py     
│   └── redis_client.py       
├── dashboard.py              
├── backtesting.py             
├── historical_data.csv        
├── docker-compose.yml        
├── Dockerfile                
├── requirements.txt          
└── README.md                 
```

## Installation

### Prerequisites
- Python 3.8 or higher
- Docker and Docker Compose (for containerized deployment)
- Virtual Environment (optional but recommended)

### Steps
1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd algo-trading-bot
   ```

2. **Set Up Virtual Environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate    # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Start the Dummy Stock Server
This server simulates real-time stock price data.
```bash
python dummy_stock_server.py
```
You should see output indicating the server is running on `ws://localhost:6789`.

### 2. Start the FastAPI Server
This server runs the trading bot which processes live data.
```bash
uvicorn app.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### 3. Run the Streamlit Dashboard
To view real-time trade orders and visualizations:
```bash
streamlit run dashboard.py
```
Open your browser at [http://localhost:8501](http://localhost:8501).

### 4. Run the Backtesting Module
To simulate trading strategy performance on historical data:
```bash
python backtesting.py
```
The output will display generated BUY/SELL signals based on historical price data.

## Docker Deployment

### Build and Run Containers
Make sure Docker and Docker Compose are installed, then run:
```bash
docker-compose up --build
```
This command builds the FastAPI app image and starts all required services (Kafka, Zookeeper, Redis, etc.).

## API Endpoints
- **GET /**  
  Returns a welcome message indicating the trading bot is running.
- **GET /health**  
  Returns a simple health check status, e.g., `{"status": "ok"}`.

## Configuration
- **WebSocket Endpoint:** Configured in `app/main.py` and `app/websocket_client.py` as `ws://localhost:6789`.
- **Kafka, Redis, and Zookeeper:** Managed via Docker Compose.
- **Trading Strategy Parameters:** Adjust `short_window`, `long_window`, and `stop_loss_pct` in `app/trading_logic.py` as needed.

## Future Enhancements
- Additional risk management and position sizing features.
- Enhanced dashboard with auto-refresh and more visualizations.
- Improved backtesting metrics (profit/loss calculations, win rate, maximum drawdown).
- Integration with Prometheus and Grafana for monitoring.
- Production-level security improvements (CORS, environment variable management).

## License
This project is licensed under the MIT License.

## Acknowledgements
- **FastAPI & Uvicorn:** For building high-performance APIs.
- **Kafka, Redis, Docker:** For their robust messaging, caching, and containerization solutions.
- **Streamlit:** For simplifying interactive data visualization.
- **Python Community:** For extensive libraries and tools that made this project possible.

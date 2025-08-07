Python 3.13.5 (v3.13.5:6cb20a219a8, Jun 11 2025, 12:23:45) [Clang 16.0.0 (clang-1600.0.26.6)] on darwin
Enter "help" below or click "Help" above for more information.
>>> mport streamlit as st
... import pandas as pd
... import requests
... import plotly.express as px
... import time
... 
... st.set_page_config(page_title="MOEX Signal Advisor", layout="wide")
... st.title("📈 MOEX Signal Advisor")
... 
... tickers = ["SBER", "GAZP", "LKOH", "GMKN", "RTSI", "Si", "BR"]
... selected_tickers = st.multiselect("Выберите инструменты", tickers, default=tickers)
... signal_filter = st.selectbox("Фильтр по сигналу", ["Все", "BUY", "SELL", "HOLD"])
... 
... def get_price(ticker):
...     url = f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticker}.json"
...     try:
...         data = requests.get(url).json()
...         price = float(data["marketdata"]["data"][0][12])
...         return price
...     except:
...         return None
... 
... def generate_signal(price):
...     if price is None:
...         return "Нет данных", "-", "-", "-", "-"
...     elif price < 100:
...         return "BUY", round(price, 2), round(price * 0.97, 2), round(price * 1.05, 2), "Цена ниже 100 ₽"
...     elif price > 200:
...         return "SELL", round(price, 2), round(price * 1.03, 2), round(price * 0.95, 2), "Цена выше 200 ₽"
...     else:
...         return "HOLD", "-", "-", "-", "Нет сигнала"
... 
st.subheader("📊 Сигналы на текущий момент")
table = []
for ticker in selected_tickers:
    price = get_price(ticker)
    signal, entry, stop, take, comment = generate_signal(price)
    if signal_filter == "Все" or signal == signal_filter:
        table.append({
            "Инструмент": ticker,
            "Сигнал": signal,
            "Вход": entry,
            "Стоп-лосс": stop,
            "Тейк-профит": take,
            "Комментарий": comment
        })

df = pd.DataFrame(table)
st.dataframe(df, use_container_width=True)

if selected_tickers:
    ticker = selected_tickers[0]
    st.subheader(f"📉 Исторический график: {ticker}")
    url = f"https://iss.moex.com/iss/history/engines/stock/markets/shares/securities/{ticker}.json"
    try:
        data = requests.get(url).json()
        candles = data["history"]["data"]
        columns = data["history"]["columns"]
        df_hist = pd.DataFrame(candles, columns=columns)
        df_hist = df_hist[["TRADEDATE", "CLOSE"]]
        fig = px.line(df_hist, x="TRADEDATE", y="CLOSE", title=f"Цена {ticker}")
        st.plotly_chart(fig, use_container_width=True)
    except:

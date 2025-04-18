import streamlit as st
from yahooquery import Ticker
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

# ページの設定
st.set_page_config(layout="wide")

# データ
stock_data = {
    "証券番号": [3097, 1952, 8876],
    "購入価格": [3230.0, 1680, 1771],
    "購入数": [100, 300, 100]
}
df = pd.DataFrame(stock_data)
df["symbol"] = df["証券番号"].astype(str) + ".T"

company_names = {
    3097: "物語コーポレーション",
    1952: "新日本空調",
    8876: "リログループ"
}

st.title("株式損益確認")

# 合計計算
df["購入金額"] = df["購入価格"] * df["購入数"]
df["現在価格"] = 0.0
df["損益"] = 0.0

total_purchase_amount = 0
total_profit_loss = 0

for i, row in df.iterrows():
    symbol = row["symbol"]
    purchase_price = row["購入価格"]
    quantity = row["購入数"]

    ticker = Ticker(symbol)
    try:
        last_price = ticker.price[symbol]['regularMarketPrice']
        price_diff = last_price - purchase_price
        profit_loss = price_diff * quantity

        df.loc[i, "現在価格"] = last_price
        df.loc[i, "損益"] = profit_loss

        total_purchase_amount += purchase_price * quantity
        total_profit_loss += profit_loss
    except Exception as e:
        st.error(f"{symbol} のデータ取得に失敗しました: {e}")

# --- 表示エリア ---

st.header("現在の投資状況")

# スタイル付き表示
st.markdown(f"<div style='font-size:28px; color:#2E8B57;'>購入金額の総計: ¥{total_purchase_amount:,.0f}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='font-size:28px; color:#1E90FF;'>現在の収益額: ¥{total_profit_loss:,.0f}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='font-size:28px; color:#DAA520;'>総評価額: ¥{(total_purchase_amount + total_profit_loss):,.0f}</div>", unsafe_allow_html=True)
st.markdown("---")

# 銘柄表示をレスポンシブに
cols = st.columns(len(df))

for i, row in df.iterrows():
    symbol = row["symbol"]
    company_name = company_names.get(row["証券番号"], "会社名不明")
    purchase_price = row["購入価格"]
    last_price = row["現在価格"]
    price_diff = last_price - purchase_price
    quantity = row["購入数"]
    total_eval = last_price * quantity
    profit_loss = row["損益"]

    ticker = Ticker(symbol)
    try:
        # 株価推移取得
        end = datetime.now()
        start = end - timedelta(days=10)
        hist = ticker.history(start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'), interval='1d')
        hist = hist.reset_index()

        # 表示
        with cols[i]:
            st.markdown(
                f"""
                <div style='background-color:#F0F8FF; padding:15px; border-radius:12px;'>
                    <h3>{company_name}（{row['証券番号']}）</h3>
                    <p style='font-size:18px;'>購入価格: ¥{purchase_price:,.0f}</p>
                    <p style='font-size:18px;'>現在価格: ¥{last_price:,.0f}</p>
                    <p style='font-size:18px;'>差額: ¥{price_diff:,.2f}</p>
                    <p style='font-size:18px;'>評価額: ¥{total_eval:,.2f}</p>
                    <p style='font-size:18px;'>損益: ¥{profit_loss:,.2f}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            fig = go.Figure(data=[go.Candlestick(
                x=hist['date'], open=hist['open'], high=hist['high'], low=hist['low'], close=hist['close']
            )])
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"{symbol} のデータ取得に失敗しました: {e}")

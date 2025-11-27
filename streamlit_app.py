import streamlit as st
from yahooquery import Ticker
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("株式損益確認")

# 現在のテーマ判定（light / dark）
theme_base = st.get_option("theme.base")
is_dark = theme_base == "dark"

# 色設定（テーマごとに変更）
color_bg = "#1e1e1e" if is_dark else "#F0F8FF"
color_text = "#ffffff" if is_dark else "#000000"
color_highlight1 = "#00FF7F" if is_dark else "#2E8B57"
color_highlight2 = "#1E90FF"
color_highlight3 = "#FFD700"

# ★ 株データにニトリホールディングス（9843）追加
stock_data = {
    "証券番号": [3097, 1952, 8876, 9843],
    "購入価格": [3230.0, 1680, 1771, 2727],
    "購入数": [100, 300, 100, 300]
}
df = pd.DataFrame(stock_data)
df["symbol"] = df["証券番号"].astype(str) + ".T"

# ★ 会社名辞書にニトリ追加
company_names = {
    3097: "物語コーポレーション",
    1952: "新日本空調",
    8876: "リログループ",
    9843: "ニトリホールディングス"
}

# 計算準備
df["購入金額"] = df["購入価格"] * df["購入数"]
df["現在価格"] = 0.0
df["損益"] = 0.0

total_purchase_amount = 0
total_profit_loss = 0

# 株価取得
for i, row in df.iterrows():
    symbol = row["symbol"]
    purchase_price = row["購入価格"]
    quantity = row["購入数"]

    ticker = Ticker(symbol)
    try:
        last_price = ticker.price[symbol]['regularMarketPrice']
        profit_loss = (last_price - purchase_price) * quantity

        df.loc[i, "現在価格"] = last_price
        df.loc[i, "損益"] = profit_loss

        total_purchase_amount += purchase_price * quantity
        total_profit_loss += profit_loss

    except Exception as e:
        st.error(f"{symbol} のデータ取得に失敗しました: {e}")

# 合計表示
st.header("現在の投資状況")

st.markdown(f"<div style='font-size:26px; color:{color_highlight1};'>購入金額の総計: ¥{total_purchase_amount:,.0f}</div>", unsafe_allow_html=True)
st.markdown(f"<div style='font-size:26px; color:{color_highlight2};'>現在の収益額: ¥{total_profit_loss:,.0f}</div>", unsafe_allow_env=True)
st.markdown(f"<div style='font-size:26px; color:{color_highlight3};'>総評価額: ¥{(total_purchase_amount + total_profit_loss):,.0f}</div>", unsafe_allow_html=True)

st.markdown("---")

# レスポンシブ表示
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
        end = datetime.now()
        start = end - timedelta(days=10)
        hist = ticker.history(start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'), interval='1d')
        hist = hist.reset_index()

        with cols[i]:
            st.markdown(
                f"""
                <div style='background-color:{color_bg}; color:{color_text}; padding:15px; border-radius:12px;'>
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
            fig.update_layout(paper_bgcolor=color_bg, plot_bgcolor=color_bg, font_color=color_text)
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"{symbol} のデータ取得に失敗しました: {e}")

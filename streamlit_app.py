import streamlit as st
from yahooquery import Ticker
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go

# 銘柄データを追加
stock_data = {
    "証券番号": [3097, 1952, 8876],
    "購入価格": [3230.0, 1680, 1771],
    "購入数": [100, 300, 100]
}
df = pd.DataFrame(stock_data)

# Yahoo Financeの証券コードに変換
df["symbol"] = df["証券番号"].astype(str) + ".T"

# 証券コードと会社名のマッピング（必要に応じて更新してください）
company_names = {
    3097: "物語コーポレーション",
    1952: "新日本空調",
    8876: "リログループ"
}

st.title("株式損益確認ページ")

# 購入金額の総計と損益額の初期化
total_purchase_amount = 0
total_profit_loss = 0

# 画面を横並びに3分割
col1, col2, col3 = st.columns(3)

# 各銘柄の情報を横並びに表示
for i, row in df.iterrows():
    symbol = row["symbol"]
    purchase_price = row["購入価格"]
    quantity = row["購入数"]

    ticker = Ticker(symbol)
    
    try:
        # 株価情報取得
        last_price = ticker.price[symbol]['regularMarketPrice']
        price_diff = last_price - purchase_price
        total_eval = last_price * quantity
        profit_loss = price_diff * quantity

        # 購入金額と損益額の計算
        total_purchase_amount += purchase_price * quantity
        total_profit_loss += profit_loss
        
        # 会社名取得
        company_name = company_names.get(row["証券番号"], "会社名不明")

        # 株価推移取得（過去10日間）
        end = datetime.now()
        start = end - timedelta(days=10)
        hist = ticker.history(start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'), interval='1d')
        hist = hist.reset_index()

        # 横並びの列に情報を表示
        if i == 0:
            with col1:
                st.subheader(f"証券番号: {row['証券番号']} ({company_name})")
                st.write(f"購入価格: ¥{purchase_price}")
                st.write(f"現在価格: ¥{last_price}")
                st.write(f"差額: ¥{price_diff:.2f}")
                st.write(f"評価額: ¥{total_eval:.2f}")
                st.write(f"損益: ¥{profit_loss:.2f}")
                fig = go.Figure(data=[go.Candlestick(x=hist['date'], open=hist['open'], high=hist['high'], low=hist['low'], close=hist['close'])])
                st.plotly_chart(fig)
        elif i == 1:
            with col2:
                st.subheader(f"証券番号: {row['証券番号']} ({company_name})")
                st.write(f"購入価格: ¥{purchase_price}")
                st.write(f"現在価格: ¥{last_price}")
                st.write(f"差額: ¥{price_diff:.2f}")
                st.write(f"評価額: ¥{total_eval:.2f}")
                st.write(f"損益: ¥{profit_loss:.2f}")
                fig = go.Figure(data=[go.Candlestick(x=hist['date'], open=hist['open'], high=hist['high'], low=hist['low'], close=hist['close'])])
                st.plotly_chart(fig)
        else:
            with col3:
                st.subheader(f"証券番号: {row['証券番号']} ({company_name})")
                st.write(f"購入価格: ¥{purchase_price}")
                st.write(f"現在価格: ¥{last_price}")
                st.write(f"差額: ¥{price_diff:.2f}")
                st.write(f"評価額: ¥{total_eval:.2f}")
                st.write(f"損益: ¥{profit_loss:.2f}")
                fig = go.Figure(data=[go.Candlestick(x=hist['date'], open=hist['open'], high=hist['high'], low=hist['low'], close=hist['close'])])
                st.plotly_chart(fig)

    except Exception as e:
        st.error(f"{symbol} のデータ取得に失敗しました: {e}")

# 購入金額の総計と損益額を表示
st.header(f"購入金額の総計: ¥{total_purchase_amount:.2f}")
st.header(f"損益額: ¥{total_profit_loss:.2f}")
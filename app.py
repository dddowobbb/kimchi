import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# 데이터 불러오기
url_exchange = "https://raw.githubusercontent.com/dddowobbb/kimchi/main/USD_KRW.csv"
url_kospi = "https://raw.githubusercontent.com/dddowobbb/kimchi/main/kospi.csv"

df_exchange = pd.read_csv(url_exchange)
df_kospi = pd.read_csv(url_kospi)

# 날짜 포맷 정리
df_exchange['Date'] = pd.to_datetime(df_exchange['Date'])
df_kospi['Date'] = pd.to_datetime(df_kospi['Date'])

# 병합
df = pd.merge(df_exchange, df_kospi, on='Date', how='inner')

# 컬럼명 정리 (예시: 'USD/KRW', 'KOSPI')
df.columns = ['Date', 'Exchange', 'KOSPI']

# 인터페이스
st.title("원/달러 환율과 코스피 지수의 관계 분석")

# 날짜 선택
start_date = st.date_input("시작 날짜", df['Date'].min().date())
end_date = st.date_input("종료 날짜", df['Date'].max().date())

# 날짜 필터링
df_filtered = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

# 시각화
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_filtered['Date'], y=df_filtered['Exchange'], name='USD/KRW 환율', yaxis='y1'))
fig.add_trace(go.Scatter(x=df_filtered['Date'], y=df_filtered['KOSPI'], name='KOSPI 지수', yaxis='y2'))

# 이중 y축
fig.update_layout(
    title="USD/KRW 환율과 KOSPI 지수",
    xaxis=dict(title='날짜'),
    yaxis=dict(title='USD/KRW', side='left'),
    yaxis2=dict(title='KOSPI', overlaying='y', side='right'),
    legend=dict(x=0.01, y=0.99)
)

st.plotly_chart(fig)

# 상관계수
corr = df_filtered['Exchange'].corr(df_filtered['KOSPI'])
st.markdown(f"### 📊 선택 기간의 상관계수: `{corr:.4f}`")

# 변화량
st.write("📈 기간 내 환율 변화율: {:.2f}%".format(
    100 * (df_filtered['Exchange'].iloc[-1] - df_filtered['Exchange'].iloc[0]) / df_filtered['Exchange'].iloc[0]
))
st.write("📉 기간 내 코스피 변화율: {:.2f}%".format(
    100 * (df_filtered['KOSPI'].iloc[-1] - df_filtered['KOSPI'].iloc[0]) / df_filtered['KOSPI'].iloc[0]
))

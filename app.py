import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# 데이터 불러오기 (csv URL)
url_exchange = "https://raw.githubusercontent.com/dddowobbb/kimchi/main/USD_KRW.csv"
url_kospi = "https://raw.githubusercontent.com/dddowobbb/kimchi/main/kospi.csv"

df_exchange = pd.read_csv(url_exchange)
df_kospi = pd.read_csv(url_kospi)

# 칼럼 개수 및 이름 출력 (디버깅용, 필요 없으면 주석 처리 가능)
st.write("=== Exchange 데이터 ===")
st.write("칼럼 개수:", len(df_exchange.columns))
st.write("칼럼명:", list(df_exchange.columns))

st.write("=== Kospi 데이터 ===")
st.write("칼럼 개수:", len(df_kospi.columns))
st.write("칼럼명:", list(df_kospi.columns))

# 필요한 칼럼만 선택 ('날짜'와 '종가')
df_exchange = df_exchange[['날짜', '종가']]
df_kospi = df_kospi[['날짜', '종가']]

# 칼럼명 변경 (구분하기 위해)
df_exchange.columns = ['날짜', 'Exchange']
df_kospi.columns = ['날짜', 'KOSPI']

# 날짜 형식 변환
df_exchange['날짜'] = pd.to_datetime(df_exchange['날짜'])
df_kospi['날짜'] = pd.to_datetime(df_kospi['날짜'])

# 데이터 병합 (날짜 기준)
df = pd.merge(df_exchange, df_kospi, on='날짜', how='inner')

# 스트림릿 인터페이스
st.title("원/달러 환율과 코스피 지수의 관계 분석")

# 날짜 선택 (범위 지정)
start_date = st.date_input("시작 날짜", df['날짜'].min().date())
end_date = st.date_input("종료 날짜", df['날짜'].max().date())

# 날짜 필터링
df_filtered = df[(df['날짜'] >= pd.to_datetime(start_date)) & (df['날짜'] <= pd.to_datetime(end_date))]

# 시각화
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_filtered['날짜'], y=df_filtered['Exchange'], name='USD/KRW 환율', yaxis='y1'))
fig.add_trace(go.Scatter(x=df_filtered['날짜'], y=df_filtered['KOSPI'], name='KOSPI 지수', yaxis='y2'))

# 이중 y축 설정
fig.update_layout(
    title="USD/KRW 환율과 KOSPI 지수",
    xaxis=dict(title='날짜'),
    yaxis=dict(title='USD/KRW', side='left'),
    yaxis2=dict(title='KOSPI', overlaying='y', side='right'),
    legend=dict(x=0.01, y=0.99)
)

st.plotly_chart(fig)

# 상관계수 계산 및 출력
corr = df_filtered['Exchange'].corr(df_filtered['KOSPI'])
st.markdown(f"### 📊 선택 기간의 상관계수: `{corr:.4f}`")

# 변화율 계산 및 출력
exchange_change = 100 * (df_filtered['Exchange'].iloc[-1] - df_filtered['Exchange'].iloc[0]) / df_filtered['Exchange'].iloc[0]
kospi_change = 100 * (df_filtered['KOSPI'].iloc[-1] - df_filtered['KOSPI'].iloc[0]) / df_filtered['KOSPI'].iloc[0]

st.write(f"📈 기간 내 환율 변화율: {exchange_change:.2f}%")
st.write(f"📉 기간 내 코스피 변화율: {kospi_change:.2f}%")

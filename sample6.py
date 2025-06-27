import streamlit as st
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# 한글 폰트 설정 (MacOS용)
matplotlib.rc('font', family='AppleGothic')
matplotlib.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="365일 트레이딩 시뮬레이션", layout="centered")
st.title("트레이딩 시뮬레이션")

# 시뮬레이션 함수
def run_simulation(win_rate, risk_percent, fee_percent, n_days=365, start_balance=100.0):
    balance = start_balance
    balances = []
    results = []

    for _ in range(n_days):
        is_win = np.random.rand() < win_rate
        if is_win:
            balance = (balance * (1 - fee_percent)) * (1 + risk_percent) * (1 - fee_percent)
            results.append("승")
        else:
            balance = (balance * (1 - fee_percent)) * (1 - risk_percent) * (1 - fee_percent)
            results.append("패")
        balances.append(balance)

    return pd.DataFrame({
        "Trial Number": np.arange(1, n_days + 1),
        "Balance": balances,
        "Result": results
    })

# 기본값
default_win_rate = 55  # %
default_risk_percent = 5  # %
default_fee_percent = 0.1  # %
default_balance = 100.0
tryal = 1000

# 입력값 초기화
if "win_rate" not in st.session_state:
    st.session_state.win_rate = default_win_rate
if "risk_percent" not in st.session_state:
    st.session_state.risk_percent = default_risk_percent
if "fee_percent" not in st.session_state:
    st.session_state.fee_percent = default_fee_percent

# 설정 입력
st.subheader("⚙️ 시뮬레이션 설정")

initial_balance = st.number_input("시작 잔고 ($)", min_value=1.0, max_value=1_000_000.0, value=default_balance, step=100.0)
new_win_rate = st.number_input("승률 (%)", min_value=0, max_value=100, step=1, value=st.session_state.win_rate)
new_risk_percent = st.number_input("리스크 비율 (%)", min_value=1, max_value=100, step=1, value=st.session_state.risk_percent)
new_fee_percent = st.number_input("수수료 (%)", min_value=0.0, max_value=5.0, step=0.01, value=st.session_state.fee_percent)

# 값 보정 및 적용
if (
    new_win_rate != st.session_state.win_rate or
    new_risk_percent != st.session_state.risk_percent or
    new_fee_percent != st.session_state.fee_percent
):
    st.session_state.win_rate = new_win_rate
    st.session_state.risk_percent = new_risk_percent
    st.session_state.fee_percent = new_fee_percent
    st.rerun()

# 시뮬레이션 실행
win_rate = st.session_state.win_rate / 100
risk_percent = st.session_state.risk_percent / 100
fee_percent = st.session_state.fee_percent / 100

df = run_simulation(win_rate, risk_percent, fee_percent, tryal, initial_balance)

# 결과 표
st.subheader("📋 결과 테이블")
st.dataframe(df, use_container_width=True)

# 잔고 그래프
st.subheader("📈 잔고 변화 그래프")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df["Trial Number"], df["Balance"], color='blue')
ax.set_title("Balance Trend", fontsize=14)
ax.set_xlabel("Trial Number")
ax.set_ylabel("Balance ($)")
ax.grid(True)

ymin = st.number_input("📉 Y축 최소값", value=0.0, min_value=0.0, key="ymin")
ymax = st.number_input("📈 Y축 최대값", value=100000.0, min_value=0.0, key="ymax")
ax.set_ylim([ymin, ymax])
st.pyplot(fig)

# 최종 잔고 표시
st.write(f"💰 최종 잔고: ${df['Balance'].iloc[-1]:,.2f}")

# 켈리 공식 (수수료 미반영)
st.subheader("🧮 캘리 공식 추천 리스크 비율 (수수료 미반영)")
b = 1.0  # 손익비 고정
q = 1 - win_rate
kelly_raw = (b * win_rate - q) / b
kelly_percent_raw = max(0.0, round(kelly_raw * 100, 2))
st.write(f"📊 수수료 미반영 최적 리스크 비율: **{kelly_percent_raw}%**")

# 켈리 공식 (수수료 반영)
st.subheader("🧮 캘리 공식 추천 리스크 비율 (수수료 반영)")

gain_eff = (1 - fee_percent) * (1 + b) * (1 - fee_percent) - 1
loss_eff = 1 - (1 - fee_percent) * (1 - b) * (1 - fee_percent)

kelly_adj = (win_rate * gain_eff - q * loss_eff) / (gain_eff + loss_eff)
kelly_percent_adj = max(0.0, round(kelly_adj * 100, 2))

st.write(f"📊 수수료 반영 최적 리스크 비율: **{kelly_percent_adj}%**")

# 재실행 버튼
if st.button("🎲 시뮬레이션 다시 실행"):
    st.rerun()
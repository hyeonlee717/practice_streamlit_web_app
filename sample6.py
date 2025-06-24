import streamlit as st
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
# 한글 폰트 설정
matplotlib.rcParams['font.family'] = 'NanumGothic'

# 마이너스 기호 깨짐 방지
matplotlib.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="365일 트레이딩 시뮬레이션", layout="centered")
st.title("트레이딩 시뮬레이션")

# 시뮬레이션 함수
def run_simulation(win_rate, risk_percent, n_days=365):
    balance = 100.0
    fee_percent = 0.001
    reward_risk_ratio = 1.0

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
        "시행횟수": np.arange(1, tryal + 1),
        "잔고": balances,
        "결과": results
    })

# 기본값
default_win_rate = 55  # % 단위
default_risk_percent = 5  # % 단위
tryal = 1000

# 입력값 초기화
if "win_rate" not in st.session_state:
    st.session_state.win_rate = default_win_rate
if "risk_percent" not in st.session_state:
    st.session_state.risk_percent = default_risk_percent

# 시뮬레이션 실행
df = run_simulation(st.session_state.win_rate / 100, st.session_state.risk_percent / 100, tryal)

# 1. 결과 표
st.subheader("📋 결과 테이블")
st.dataframe(df, use_container_width=True)


# 2. 잔고 그래프
st.subheader("📈 잔고 변화 그래프")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df["시행횟수"], df["잔고"], color='blue')
ax.set_title("잔고 변화 추이", fontsize=14)
ax.set_xlabel("시행 횟수")
ax.set_ylabel("잔고 ($)")
ax.grid(True)

# Y축 범위 수동 조절 (기본값: 최소 0, 최대 50000)
ymin = st.number_input("📉 Y축 최소값", value=0.0, min_value=0.0, key="ymin")
ymax = st.number_input("📈 Y축 최대값", value=100000.0, min_value=0.0, key="ymax")
ax.set_ylim([ymin, ymax])
st.pyplot(fig)

st.write(f"💰 최종 잔고: ${df['잔고'].iloc[-1]:,.2f}")

# 3. 설정 입력 (맨 아래에 배치)
st.subheader("⚙️ 시뮬레이션 설정")

# 시작 잔고 입력
initial_balance = st.number_input("시작 잔고 ($)", min_value=1.0, max_value=1000000.0, value=100.0, step=100.0, key="initial_balance")

# 값 보정
st.session_state.win_rate = int(np.clip(st.session_state.win_rate, 30, 90))
st.session_state.risk_percent = int(np.clip(st.session_state.risk_percent, 1, 50))

# 위젯
new_win_rate = st.number_input("승률 (%)", min_value=0, max_value=100, step=1, value=st.session_state.win_rate, key="win_input")
new_risk_percent = st.number_input("리스크 비율 (%)", min_value=1, max_value=100, step=1, value=st.session_state.risk_percent, key="risk_input")

# 값이 바뀌면 자동 반영
if new_win_rate != st.session_state.win_rate or new_risk_percent != st.session_state.risk_percent:
    st.session_state.win_rate = new_win_rate
    st.session_state.risk_percent = new_risk_percent
    st.rerun()

# 4. 시뮬레이션 수동 재실행 버튼
if st.button("🎲 시뮬레이션 다시 실행"):
    st.rerun()

# 5. 캘리 기준 최적 리스크 비율 계산
st.subheader("🧮 캘리 공식 추천 리스크 비율(수수료 미반영)")

p = st.session_state.win_rate / 100
b = 1.0  # 손익비 고정
q = 1 - p

kelly = (b * p - q) / b
kelly_percent = max(0.0, round(kelly * 100, 2))  # 음수 방지

st.write(f"📊 현재 승률 기준 캘리 최적 리스크 비율: **{kelly_percent}%**")

# 6. 캘리 기준 최적 리스크 비율 계산
st.subheader("🧮 캘리 공식 추천 리스크 비율 (수수료 반영)")

p = st.session_state.win_rate / 100
q = 1 - p
fee = 0.001
r = 1.0  # 손익비 고정

# 실질 수익률과 손실률
gain_eff = (1 - fee) * (1 + r) * (1 - fee) - 1
loss_eff = 1 - (1 - fee) * (1 - r) * (1 - fee)

# 보정된 kelly
kelly_adj = (p * gain_eff - q * loss_eff) / (gain_eff + loss_eff)
kelly_percent = max(0.0, round(kelly_adj * 100, 2))

st.write(f"📊 수수료 반영 최적 리스크 비율: **{kelly_percent}%**")
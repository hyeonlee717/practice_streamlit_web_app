import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("🎲 정규분포 수렴 시뮬레이션 (Galton Board 원리)")

# 사용자 입력: 시도 횟수 및 핀 층 수
num_trials = st.slider("구슬 개수 (시도 횟수)", 100, 200000, 100000, step=100)
num_layers = st.slider("핀 층 수", 5, 100, 10)

# 구슬 시뮬레이션: 이항 분포 기반
# 구슬은 각 층마다 좌우 중 하나로 랜덤 이동
balls = np.random.binomial(num_layers, 0.5, size=num_trials)

# 결과 시각화
fig, ax = plt.subplots()
ax.hist(balls, bins=np.arange(num_layers + 2) - 0.5, rwidth=0.8, color='skyblue', edgecolor='black')
ax.set_title("갈톤 보드 결과 히스토그램")
ax.set_xlabel("오른쪽으로 이동한 횟수")
ax.set_ylabel("구슬 수")
ax.set_xticks(range(num_layers + 1))
st.pyplot(fig)

st.markdown("""
- 구슬은 각 핀에서 좌우로 **50% 확률로 이동**  
- 이동이 누적되며 **이항분포**를 따름  
- 핀의 수가 많아질수록 **정규분포로 수렴** (중심극한정리)
""")
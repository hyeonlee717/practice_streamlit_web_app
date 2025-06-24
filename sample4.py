import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title("선거 시뮬레이션: 유권자수 기반 사전 vs 본투표 결과 분석")

# 선거구 수
n = 250
np.random.seed(42)

# 유권자 수: 지수분포 기반 생성 (3천 ~ 20만 사이)
raw = np.random.exponential(scale=1.0, size=n)
scaled = (raw - raw.min()) / (raw.max() - raw.min())
voters = (scaled * (200_000 - 3_000) + 3_000).astype(int)

# 사전/본투표 유권자 분할
early_voters = (voters * 0.3).astype(int)   # 30% 사전투표
main_voters = voters - early_voters         # 나머지 본투표

# 사전투표: 1번 후보 평균 60% 정규분포
early_rate_1 = np.clip(np.random.normal(loc=0.6, scale=0.05, size=n), 0, 1)
early_vote_1 = (early_voters * early_rate_1).astype(int)
early_vote_2 = early_voters - early_vote_1

# 본투표: 2번 후보 평균 60% 정규분포
main_rate_2 = np.clip(np.random.normal(loc=0.6, scale=0.05, size=n), 0, 1)
main_vote_2 = (main_voters * main_rate_2).astype(int)
main_vote_1 = main_voters - main_vote_2

# 총합
total_vote_1 = early_vote_1 + main_vote_1
total_vote_2 = early_vote_2 + main_vote_2

# 데이터프레임
df = pd.DataFrame({
    "선거구": [f"선거구{i+1}" for i in range(n)],
    "유권자수": voters,
    "사전_1번": early_vote_1,
    "사전_2번": early_vote_2,
    "본_1번": main_vote_1,
    "본_2번": main_vote_2,
    "총_1번": total_vote_1,
    "총_2번": total_vote_2,
})

# 득표율 계산
df["사전_1번_득표율"] = df["사전_1번"] / (df["사전_1번"] + df["사전_2번"])
df["본_1번_득표율"] = df["본_1번"] / (df["본_1번"] + df["본_2번"])
df["득표율_차이"] = df["사전_1번_득표율"] - df["본_1번_득표율"]

# 데이터프레임 표시
st.subheader("선거 데이터")
st.dataframe(df)

# 유권자수 시각화
st.subheader("선거구별 유권자 수 (지수분포 기반, 내림차순)")
df_sorted = df.sort_values(by="유권자수", ascending=False).reset_index(drop=True)

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(df_sorted["유권자수"], marker='o')
ax1.set_title("선거구별 유권자 수", fontsize=14)
ax1.set_xlabel("선거구 순위")
ax1.set_ylabel("유권자 수")
ax1.grid(True)
st.pyplot(fig1)

# 득표율 차이 히스토그램
st.subheader("1번 후보 사전 vs 본투표 득표율 차이")

fig2, ax2 = plt.subplots()
ax2.hist(df["득표율_차이"], bins=20, edgecolor='black')
ax2.set_title("1번 후보 사전-본투표 득표율 차이")
ax2.set_xlabel("득표율 차이")
ax2.set_ylabel("선거구 수")
st.pyplot(fig2)

# 유권자수 내림차순으로 정렬
df_sorted = df.sort_values(by="유권자수", ascending=False).reset_index(drop=True)

st.subheader("선거인구 내림차순 정렬에 따른 1번 후보 득표율 차이")

fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df_sorted["득표율_차이"], marker='o', linestyle='-')
ax.set_title("선거인구 많은 순서대로 본 사전-본투표 득표율 차이")
ax.set_xlabel("선거구 순위 (선거인구 많은 순)")
ax.set_ylabel("득표율 차이")
ax.grid(True)
st.pyplot(fig)
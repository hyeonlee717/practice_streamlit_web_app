import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("사전투표 vs 본투표 시뮬레이션")

# 선거구 수
n = 250

# 시드 고정
np.random.seed(42)

# 사전/본투표 유권자 수
early_voters = np.random.randint(500, 3000, size=n)
main_voters = np.random.randint(2000, 8000, size=n)

# 1번 후보는 사전투표에서 우세 (득표율 60~80%)
early_rate_1 = np.random.uniform(0.6, 0.8, size=n)
early_vote_1 = (early_voters * early_rate_1).astype(int)
early_vote_2 = early_voters - early_vote_1

# 2번 후보는 본투표에서 우세 (득표율 60~80%)
main_rate_2 = np.random.uniform(0.6, 0.8, size=n)
main_vote_2 = (main_voters * main_rate_2).astype(int)
main_vote_1 = main_voters - main_vote_2

# 총합
total_vote_1 = early_vote_1 + main_vote_1
total_vote_2 = early_vote_2 + main_vote_2

# 데이터프레임 구성
df = pd.DataFrame({
    "선거구": [f"선거구{i+1}" for i in range(n)],
    "사전투표_1번": early_vote_1,
    "사전투표_2번": early_vote_2,
    "본투표_1번": main_vote_1,
    "본투표_2번": main_vote_2,
    "총득표_1번": total_vote_1,
    "총득표_2번": total_vote_2,
})

# 표 표시
st.dataframe(df)

# 득표율 차이 시각화
df["사전_1번_득표율"] = df["사전투표_1번"] / (df["사전투표_1번"] + df["사전투표_2번"])
df["본_1번_득표율"] = df["본투표_1번"] / (df["본투표_1번"] + df["본투표_2번"])
df["득표율_차이"] = df["사전_1번_득표율"] - df["본_1번_득표율"]

st.subheader("사전 vs 본투표 1번 득표율 차이 분포")

fig, ax = plt.subplots()
ax.hist(df["득표율_차이"], bins=20, edgecolor='black')
ax.set_title("1번 후보 사전-본투표 득표율 차이")
ax.set_xlabel("득표율 차이")
ax.set_ylabel("선거구 수")
st.pyplot(fig)
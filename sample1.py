import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

st.title("📊 정규분포 시각화 도구")

# 평균과 표준편차 설정
mean = st.slider("평균 (μ)", min_value=-10.0, max_value=10.0, value=0.0, step=0.1)
std_dev = st.slider("표준편차 (σ)", min_value=0.1, max_value=10.0, value=1.0, step=0.1)

# 데이터 생성
x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 1000)
y = norm.pdf(x, mean, std_dev)

# 그래프 출력
fig, ax = plt.subplots()
ax.plot(x, y, label=f"N(μ={mean}, σ={std_dev})")
ax.fill_between(x, y, alpha=0.3)
ax.set_title("정규분포 곡선")
ax.set_xlabel("x")
ax.set_ylabel("확률밀도 f(x)")
ax.legend()

st.pyplot(fig)

st.markdown("""
- 평균(μ)은 곡선의 중심 위치를 조절합니다.  
- 표준편차(σ)는 곡선의 **넓이와 퍼짐 정도**를 조절합니다.  
- 이 곡선은 **확률밀도함수 (PDF)** 입니다.
""")
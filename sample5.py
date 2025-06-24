import streamlit as st
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# 한글 폰트 설정 (MacOS용 예시: AppleGothic)
matplotlib.rc('font', family='AppleGothic')
matplotlib.rcParams['axes.unicode_minus'] = False

st.title("선거구 유권자 수에 따른 득표율 차이 시뮬레이션")

# 실제 유권자 수 리스트
voters = np.array([
    617951, 561654, 533584, 493010, 506849, 472730, 452664, 446923, 430719, 428942,
    448630, 443085, 424683, 433899, 435944, 433087, 397014, 421631, 411789, 398834,
    402095, 396043, 362472, 366811, 374002, 368029, 347519, 358624, 346438, 345855,
    344220, 337985, 341688, 366830, 335136, 323168, 332596, 342360, 339630, 321302,
    338629, 309712, 325211, 307067, 335343, 325663, 307342, 301242, 313951, 307846,
    300119, 301007, 309973, 303506, 279415, 289796, 277170, 294314, 272865, 287897,
    287897, 261733, 272942, 269110, 263759, 244138, 255448, 240133, 258595, 257971,
    234321, 244536, 243541, 248733, 247155, 238889, 231349, 234688, 235338, 245241,
    234995, 233819, 242536, 241014, 222936, 232652, 221550, 222856, 217320, 225516,
    208500, 212190, 208154, 206121, 197016, 205448, 196407, 189461, 188148, 176412,
    194244, 184908, 189163, 184068, 192259, 191335, 177671, 181085, 181085, 183614,
    178000, 176478, 181665, 183191, 178351, 172558, 162776, 167297, 170398, 156251,
    158412, 158716, 157266, 154518, 153669, 155343, 147846, 147381, 145228, 148454,
    133116, 146414, 146196, 131128, 136331, 136399, 126811, 125901, 125079, 127307,
    117773, 112618, 113975, 112680, 110181, 99973, 102203, 92286, 101401, 90401,
    94356, 86947, 95971, 92886, 93909, 91037, 87894, 90650, 92234, 86901, 85181,
    77728, 86128, 81951, 82897, 81862, 73203, 77893, 68790, 75688, 76927, 66857,
    72896, 71055, 70334, 63399, 56611, 59787, 55564, 59907, 54306, 55205, 56266,
    54218, 54627, 52316, 51663, 51990, 50638, 46202, 45723, 46657, 45634, 45733,
    43387, 40521, 43863, 40385, 44528, 43287, 44051, 41725, 41362, 38328, 38236,
    37839, 39554, 37770, 37540, 35832, 37329, 37329, 36504, 36753, 36974, 34072,
    35356, 33528, 33250, 31153, 35284, 33422, 32702, 30968, 30579, 28924, 30577,
    31928, 27478, 27768, 27900, 25634, 27383, 26412, 24184, 27165, 24642, 25010,
    24980, 23342, 24393, 21975, 22236, 22070, 23294, 21402, 20899, 20014, 18588,
    18554, 17713, 14161, 8412
])
voters.sort()
voters = voters[::-1]
n = len(voters)

# 유권자 수 기반 표준편차 조절
stds = np.interp(voters, (voters.min(), voters.max()), (0.08, 0.01))

# 사전투표 득표율
early_rates_1 = np.clip(np.random.normal(loc=0.6, scale=stds), 0, 1)
early_votes = (voters * 0.35).astype(int)
early_1 = (early_votes * early_rates_1).astype(int)
early_2 = early_votes - early_1

# 본투표 득표율
main_rates_1 = np.clip(np.random.normal(loc=0.4, scale=stds), 0, 1)
main_votes = (voters * 0.44).astype(int)
main_1 = (main_votes * main_rates_1).astype(int)
main_2 = main_votes - main_1

# 득표율 차이 계산
early_rate_1 = early_1 / early_votes
main_rate_1 = main_1 / main_votes
gap = np.clip(np.abs(early_rate_1 - main_rate_1), 0, 1)

# 데이터프레임 구성
df = pd.DataFrame({
    "선거구": [f"선거구{i+1}" for i in range(n)],
    "유권자수": voters,
    "사전_득표율": early_rate_1,
    "본_득표율": main_rate_1,
    "득표율_차이": gap
}).reset_index(drop=True)

# 표 출력
st.dataframe(df)

# 총 유권자 수 출력
st.write(f"🔢 총 유권자 수: {df['유권자수'].sum():,}명")

# 그래프 1: 득표율 차이 + 추세선
fig, ax = plt.subplots(figsize=(10, 5))
x = np.arange(len(df))
y = df["득표율_차이"]
ax.plot(x, y, marker='o', linestyle='-', label="득표율 차이")
coeffs = np.polyfit(x, y, 1)
trend = np.poly1d(coeffs)
ax.plot(x, trend(x), color='red', linestyle='--', label='선형 추세선')
ax.set_title("득표율 (사전 - 본투표)", fontsize=14)
ax.set_xlabel("선거구 순위", fontsize=12)
ax.set_ylabel("득표율 차이", fontsize=12)
ax.legend()
ax.grid(True)
st.pyplot(fig)

# 새로고침 버튼
if st.button("📊 시뮬레이션 다시 실행"):
    st.rerun()

# 그래프 2: 유권자 수 그래프
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.plot(df["유권자수"], marker='o', linestyle='-', color='green')
ax2.set_title("선거구별 유권자 수 (내림차순)", fontsize=14)
ax2.set_xlabel("선거구 순위", fontsize=12)
ax2.set_ylabel("유권자 수", fontsize=12)
ax2.grid(True)
st.pyplot(fig2)
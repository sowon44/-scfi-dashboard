"""
SCFI 추이 분석 대시보드 (Streamlit)
실행: streamlit run app.py
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="SCFI 추이 분석 대시보드", page_icon="🚢", layout="wide")

# ---------------------------------------------------------------------------
# 1) 확정 백데이터 (2020-01 ~ 2026-08, 검증된 33개 지점)
#    date  : 차트용 근사 날짜(ISO) — 월평균/기간 표기 항목은 해당 기간 중앙값으로 설정
#    label : 원본 표기(발표 주차/기간)
# ---------------------------------------------------------------------------
DATA = [
    dict(date="2020-01-15", label="2020-01",        value=1022.00, type="월중 저점",
         note="3년래 최저치로 2023.1 기사에서 인용", verified=False,
         source="Container News",
         url="https://container-news.com/scfi-crumbles-to-30-month-low-nears-pre-pandemic-levels"),
    dict(date="2020-10-16", label="2020-10-16",     value=1448.87, type="주간",
         note="5월 말 대비 71% 상승", verified=False,
         source="The Loadstar (via choice.aero)", url="https://choice.aero/tag/asia-australia"),
    dict(date="2020-11-06", label="2020-11-06",     value=1664.56, type="주간",
         note="전주 대비 +134.57pt, 2010년 이후 최고치", verified=False,
         source="Container News", url="https://container-news.com/scfi-reaches-its-highest-point/"),
    dict(date="2021-05-15", label="2021-05",        value=3000.00, type="주간(돌파)",
         note="SCFI 최초 3,000pt 돌파", verified=False,
         source="index1520.com",
         url="https://index1520.com/en/news/indeks-scfi-vpervye-prevysil-otmetku-4000-punktov"),
    dict(date="2021-07-16", label="2021-07-16",     value=4054.42, type="주간",
         note="SCFI 최초 4,000pt 돌파, 10주 연속 상승", verified=False,
         source="Container News",
         url="https://container-news.com/scfi-crosses-the-us4000-teu-mark-for-the-first-time-in-history"),
    dict(date="2021-12-31", label="2021-12-31경",   value=5047.00, type="주간",
         note="SCFI 최초 5,000pt 돌파, 전주 대비 +91pt", verified=False,
         source="Splash247", url="https://splash247.com/?p=157540"),
    dict(date="2022-01-07", label="2022-01-07",     value=5109.60, type="주간(역대 최고치)",
         note="역대 최고치", verified=False,
         source="아시아경제(회고)", url="https://view.asiae.co.kr/en/article/2023011216160061717"),
    dict(date="2022-03-25", label="2022-03-25",     value=4434.07, type="주간", note="",
         verified=False, source="아시아경제(회고)",
         url="https://view.asiae.co.kr/en/article/2023011216160061717"),
    dict(date="2022-06-10", label="2022-06-10",     value=4233.31, type="주간", note="",
         verified=True, source="뉴스토마토", url="https://newstomato.com/ReadNews.aspx?no=1129752"),
    dict(date="2022-06-17", label="2022-06-17",     value=4221.96, type="주간",
         note="전주 대비 -11.35pt (산술검증), 4주 연속 상승 후 하락 전환", verified=True,
         source="뉴스토마토", url="https://newstomato.com/ReadNews.aspx?no=1129752"),
    dict(date="2022-06-24", label="2022-06-24",     value=4216.13, type="주간", note="",
         verified=False, source="아시아경제(회고)",
         url="https://view.asiae.co.kr/en/article/2023011216160061717"),
    dict(date="2022-07-01", label="2022-07-01",     value=4203.27, type="주간", note="",
         verified=False, source="아시아경제(회고)",
         url="https://view.asiae.co.kr/en/article/2023011216160061717"),
    dict(date="2022-09-02", label="2022-09-02",     value=2847.62, type="주간", note="",
         verified=False, source="아시아경제(회고)",
         url="https://view.asiae.co.kr/en/article/2023011216160061717"),
    dict(date="2022-10-14", label="2022-10-14",     value=1814.00, type="주간", note="",
         verified=False, source="아시아경제(회고)",
         url="https://view.asiae.co.kr/en/article/2023011216160061717"),
    dict(date="2022-12-30", label="2022-12-30",     value=1107.55, type="주간",
         note="다음 주 대비 -46.41pt (산술검증)", verified=True,
         source="아시아경제", url="https://view.asiae.co.kr/en/article/2023011216160061717"),
    dict(date="2023-01-06", label="2023-01-06",     value=1061.14, type="주간",
         note="전주 대비 -46.41pt (산술검증), 28주 연속 하락 후 반등", verified=True,
         source="아시아경제", url="https://view.asiae.co.kr/en/article/2023011216160061717"),
    dict(date="2023-01-15", label="2023-01 중순",   value=1031.42, type="주간(30개월래 최저)",
         note="2020년 7월 이후 최저치", verified=False,
         source="Container News",
         url="https://container-news.com/scfi-crumbles-to-30-month-low-nears-pre-pandemic-levels"),
    dict(date="2023-01-20", label="2023-01(월평균)", value=1040.77, type="월평균", note="",
         verified=False, source="Cello Square(회고)", url="https://www.cello-square.com/kr/blog/view-1383.do"),
    dict(date="2023-12-15", label="2023-12(월평균)", value=1230.22, type="월평균",
         note="다음 달 대비 -73.17% (산술검증)", verified=True,
         source="Cello Square(회고)", url="https://www.cello-square.com/kr/blog/view-1383.do"),
    dict(date="2023-12-25", label="2023-12 4주차",  value=1254.99, type="주간", note="",
         verified=False, source="파이낸셜뉴스(회고)", url="https://v.daum.net/v/20250305055906655"),
    dict(date="2024-01-05", label="2024-01-05", value=1896.65, type="주간", note="",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-01-12", label="2024-01-12", value=2206.03, type="주간", note="전주 대비 +16.31%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-01-19", label="2024-01-19", value=2239.61, type="주간", note="전주 대비 +1.52%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-01-26", label="2024-01-26", value=2179.09, type="주간", note="전주 대비 -2.70%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-02-02", label="2024-02-02", value=2217.73, type="주간", note="전주 대비 +1.77%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-02-09", label="2024-02-09", value=2166.31, type="주간", note="전주 대비 -2.32%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-02-23", label="2024-02-23", value=2109.91, type="주간", note="전주 대비 -2.60%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-03-01", label="2024-03-01", value=1979.12, type="주간", note="전주 대비 -6.20%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-03-08", label="2024-03-08", value=1885.74, type="주간", note="전주 대비 -4.72%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-03-15", label="2024-03-15", value=1772.92, type="주간", note="전주 대비 -5.98%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-03-22", label="2024-03-22", value=1732.57, type="주간", note="전주 대비 -2.28%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-03-29", label="2024-03-29", value=1730.98, type="주간", note="전주 대비 -0.09%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-04-03", label="2024-04-03", value=1745.43, type="주간", note="전주 대비 +0.83%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-04-12", label="2024-04-12", value=1757.04, type="주간", note="전주 대비 +0.67%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-04-19", label="2024-04-19", value=1769.54, type="주간", note="전주 대비 +0.71%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-04-26", label="2024-04-26", value=1940.63, type="주간", note="전주 대비 +9.67%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-05-10", label="2024-05-10", value=2305.79, type="주간", note="전주 대비 +18.82%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-05-17", label="2024-05-17", value=2520.76, type="주간", note="전주 대비 +9.32%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-05-24", label="2024-05-24", value=2703.43, type="주간", note="전주 대비 +7.25%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-05-31", label="2024-05-31", value=3044.77, type="주간", note="전주 대비 +12.63%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-06-07", label="2024-06-07", value=3184.87, type="주간", note="전주 대비 +4.60%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-06-14", label="2024-06-14", value=3379.22, type="주간", note="전주 대비 +6.10%",
         verified=True, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-06-21", label="2024-06-21", value=3475.60, type="주간", note="전주 대비 +2.85%",
         verified=True, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-06-28", label="2024-06-28", value=3714.32, type="주간", note="전주 대비 +6.87%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-07-05", label="2024-07-05", value=3733.80, type="주간", note="전주 대비 +0.52%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-07-12", label="2024-07-12", value=3674.86, type="주간", note="전주 대비 -1.58%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-07-19", label="2024-07-19", value=3542.44, type="주간", note="전주 대비 -3.60%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-07-26", label="2024-07-26", value=3447.87, type="주간", note="전주 대비 -2.67%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-08-02", label="2024-08-02", value=3332.67, type="주간", note="전주 대비 -3.34%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-08-09", label="2024-08-09", value=3253.89, type="주간", note="전주 대비 -2.36%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-08-16", label="2024-08-16", value=3281.36, type="주간", note="전주 대비 +0.84%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-08-23", label="2024-08-23", value=3097.63, type="주간", note="전주 대비 -5.60%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-08-30", label="2024-08-30", value=2963.38, type="주간", note="전주 대비 -4.33%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-09-06", label="2024-09-06", value=2726.58, type="주간", note="전주 대비 -7.99%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-09-13", label="2024-09-13", value=2510.95, type="주간", note="전주 대비 -7.91%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-09-20", label="2024-09-20", value=2366.24, type="주간", note="전주 대비 -5.76%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-09-27", label="2024-09-27", value=2135.08, type="주간", note="전주 대비 -9.77%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-10-11", label="2024-10-11", value=2062.57, type="주간", note="전주 대비 -3.40%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-10-18", label="2024-10-18", value=2062.15, type="주간", note="전주 대비 -0.02%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-10-25", label="2024-10-25", value=2185.33, type="주간", note="전주 대비 +5.97%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-11-01", label="2024-11-01", value=2303.44, type="주간", note="전주 대비 +5.40%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-11-08", label="2024-11-08", value=2331.58, type="주간", note="전주 대비 +1.22%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-11-15", label="2024-11-15", value=2251.90, type="주간", note="전주 대비 -3.42%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-11-22", label="2024-11-22", value=2160.08, type="주간", note="전주 대비 -4.08%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-11-29", label="2024-11-29", value=2233.83, type="주간", note="전주 대비 +3.41%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-12-06", label="2024-12-06", value=2256.46, type="주간", note="전주 대비 +1.01%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-12-13", label="2024-12-13", value=2384.40, type="주간", note="전주 대비 +5.67%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-12-20", label="2024-12-20", value=2390.17, type="주간", note="전주 대비 +0.24%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2024-12-27", label="2024-12-27", value=2460.34, type="주간", note="전주 대비 +2.94%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-01-03", label="2025-01-03", value=2505.17, type="주간", note="전주 대비 +1.82%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-01-10", label="2025-01-10", value=2290.68, type="주간", note="전주 대비 -8.56%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-01-17", label="2025-01-17", value=2130.81, type="주간", note="전주 대비 -6.98%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-01-24", label="2025-01-24", value=2045.45, type="주간", note="전주 대비 -4.01%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-02-07", label="2025-02-07", value=1896.65, type="주간", note="전주 대비 -7.27%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-02-14", label="2025-02-14", value=1758.82, type="주간", note="전주 대비 -7.27%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-02-21", label="2025-02-21", value=1595.08, type="주간", note="전주 대비 -9.31%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-02-28", label="2025-02-28", value=1515.29, type="주간", note="전주 대비 -5.00%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-03-07", label="2025-03-07", value=1436.30, type="주간", note="전주 대비 -5.21%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-03-14", label="2025-03-14", value=1319.34, type="주간", note="전주 대비 -8.14%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-03-21", label="2025-03-21", value=1292.75, type="주간", note="전주 대비 -2.02%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-03-28", label="2025-03-28", value=1356.88, type="주간", note="전주 대비 +4.96%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-04-03", label="2025-04-03", value=1392.78, type="주간", note="전주 대비 +2.65%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-04-11", label="2025-04-11", value=1394.68, type="주간", note="전주 대비 +0.14%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-04-18", label="2025-04-18", value=1370.58, type="주간", note="전주 대비 -1.73%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-04-25", label="2025-04-25", value=1347.84, type="주간", note="전주 대비 -1.66%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-04-30", label="2025-04-30", value=1340.93, type="주간", note="전주 대비 -0.51%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-05-09", label="2025-05-09", value=1345.17, type="주간", note="전주 대비 +0.32%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-05-16", label="2025-05-16", value=1479.39, type="주간", note="전주 대비 +9.98%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-05-23", label="2025-05-23", value=1586.12, type="주간", note="전주 대비 +7.21%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-05-30", label="2025-05-30", value=2072.71, type="주간", note="전주 대비 +30.68%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-06-06", label="2025-06-06", value=2240.35, type="주간", note="전주 대비 +8.09%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-06-13", label="2025-06-13", value=2088.24, type="주간", note="전주 대비 -6.79%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-06-20", label="2025-06-20", value=1869.59, type="주간", note="전주 대비 -10.47%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-06-27", label="2025-06-27", value=1861.51, type="주간", note="전주 대비 -0.43%",
         verified=True, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-07-04", label="2025-07-04", value=1763.49, type="주간", note="전주 대비 -5.27%",
         verified=True, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-07-11", label="2025-07-11", value=1733.29, type="주간", note="전주 대비 -1.71%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-07-18", label="2025-07-18", value=1646.90, type="주간", note="전주 대비 -4.98%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-07-25", label="2025-07-25", value=1592.59, type="주간", note="전주 대비 -3.30%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-08-01", label="2025-08-01", value=1550.74, type="주간", note="전주 대비 -2.63%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-08-08", label="2025-08-08", value=1489.68, type="주간", note="전주 대비 -3.94%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-08-15", label="2025-08-15", value=1460.19, type="주간", note="전주 대비 -1.98%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-08-22", label="2025-08-22", value=1415.36, type="주간", note="전주 대비 -3.07%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-08-29", label="2025-08-29", value=1445.06, type="주간", note="전주 대비 +2.10%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-09-05", label="2025-09-05", value=1444.44, type="주간", note="전주 대비 -0.04%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-09-12", label="2025-09-12", value=1398.11, type="주간", note="전주 대비 -3.21%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-09-19", label="2025-09-19", value=1198.21, type="주간", note="전주 대비 -14.30%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-09-26", label="2025-09-26", value=1114.52, type="주간", note="전주 대비 -6.98%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-10-10", label="2025-10-10", value=1160.42, type="주간", note="전주 대비 +4.12%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-10-17", label="2025-10-17", value=1310.32, type="주간", note="전주 대비 +12.92%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-10-24", label="2025-10-24", value=1403.46, type="주간", note="전주 대비 +7.11%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-10-31", label="2025-10-31", value=1550.70, type="주간", note="전주 대비 +10.49%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-11-07", label="2025-11-07", value=1495.10, type="주간", note="전주 대비 -3.59%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-11-14", label="2025-11-14", value=1451.38, type="주간", note="전주 대비 -2.92%",
         verified=True, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-11-21", label="2025-11-21", value=1393.56, type="주간", note="전주 대비 -3.98%",
         verified=True, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-11-28", label="2025-11-28", value=1403.13, type="주간", note="전주 대비 +0.69%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-12-05", label="2025-12-05", value=1397.63, type="주간", note="전주 대비 -0.39%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-12-12", label="2025-12-12", value=1506.46, type="주간", note="전주 대비 +7.79%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-12-19", label="2025-12-19", value=1552.92, type="주간", note="전주 대비 +3.08%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2025-12-26", label="2025-12-26", value=1656.32, type="주간", note="전주 대비 +6.66%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-01-09", label="2026-01-09", value=1647.39, type="주간", note="전주 대비 -0.54%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-01-16", label="2026-01-16", value=1574.12, type="주간", note="전주 대비 -4.45%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-01-23", label="2026-01-23", value=1457.86, type="주간", note="전주 대비 -7.39%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-01-30", label="2026-01-30", value=1316.75, type="주간", note="전주 대비 -9.68%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-02-06", label="2026-02-06", value=1266.56, type="주간", note="전주 대비 -3.81%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-02-13", label="2026-02-13", value=1251.46, type="주간", note="전주 대비 -1.19%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-02-27", label="2026-02-27", value=1333.11, type="주간", note="전주 대비 +6.52%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-03-06", label="2026-03-06", value=1489.19, type="주간", note="전주 대비 +11.71%",
         verified=True, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-03-13", label="2026-03-13", value=1710.35, type="주간", note="전주 대비 +14.85%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-03-20", label="2026-03-20", value=1706.95, type="주간", note="전주 대비 -0.20%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-03-27", label="2026-03-27", value=1826.77, type="주간", note="전주 대비 +7.02%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-04-03", label="2026-04-03", value=1854.96, type="주간", note="전주 대비 +1.54%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-04-10", label="2026-04-10", value=1890.77, type="주간", note="전주 대비 +1.93%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-04-17", label="2026-04-17", value=1886.54, type="주간", note="전주 대비 -0.22%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-04-24", label="2026-04-24", value=1875.26, type="주간", note="전주 대비 -0.60%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-04-30", label="2026-04-30", value=1911.40, type="주간", note="전주 대비 +1.93%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-05-08", label="2026-05-08", value=1954.21, type="주간", note="전주 대비 +2.24%",
         verified=True, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-05-15", label="2026-05-15", value=2140.66, type="주간", note="전주 대비 +9.54%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-05-22", label="2026-05-22", value=2218.15, type="주간", note="전주 대비 +3.62%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-05-29", label="2026-05-29", value=2571.73, type="주간", note="전주 대비 +15.94%",
         verified=True, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-06-05", label="2026-06-05", value=2726.48, type="주간", note="전주 대비 +6.02%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-06-12", label="2026-06-12", value=2985.22, type="주간", note="전주 대비 +9.49%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-06-18", label="2026-06-18", value=3121.69, type="주간", note="전주 대비 +4.57%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-06-26", label="2026-06-26", value=3239.64, type="주간", note="전주 대비 +3.78%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-07-03", label="2026-07-03", value=3326.87, type="주간", note="전주 대비 +2.69%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-07-10", label="2026-07-10", value=3184.82, type="주간", note="전주 대비 -4.27%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-07-17", label="2026-07-17", value=3080.31, type="주간", note="전주 대비 -3.28%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-07-24", label="2026-07-24", value=3062.95, type="주간", note="전주 대비 -0.56%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-07-31", label="2026-07-31", value=3205.97, type="주간", note="전주 대비 +4.67%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-08-07", label="2026-08-07", value=3276.14, type="주간", note="전주 대비 +2.19%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-08-14", label="2026-08-14", value=3355.24, type="주간", note="전주 대비 +2.41%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-08-21", label="2026-08-21", value=3409.63, type="주간", note="전주 대비 +1.62%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
    dict(date="2026-08-28", label="2026-08-28", value=3509.53, type="주간", note="전주 대비 +2.93%",
         verified=False, source="국가물류통합정보센터", url="https://www.nlic.go.kr"),
]

df = pd.DataFrame(DATA)
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").reset_index(drop=True)

# ---------------------------------------------------------------------------
# 1-1) 글로벌 물류 이슈 — 사실만, 출처 명시
# ---------------------------------------------------------------------------
CAT_COLOR = {"지정학/전쟁": "#e0473e", "무역/운하 리스크": "#f2994a"}

EVENTS = [
    # 이슈 1: 미국-이란 전쟁·호르무즈 해협 봉쇄
    dict(date="2026-02-28", issue="미국-이란 전쟁·호르무즈 해협",
         fact="미국·이스라엘이 이란 공습, 최고지도자 알리 하메네이 사망",
         source="물류신문(Cello Square 재인용)", url="https://www.cello-square.com/kr/blog/view-1859.do"),
    dict(date="2026-03-03", issue="미국-이란 전쟁·호르무즈 해협",
         fact="VLCC 스팟 평균 운임 전년 동기 대비 395% 폭등, 20만4,000달러(2020년 4월 이후 최고치)",
         source="딜사이트", url="https://dealsite.co.kr/articles/157820"),
    dict(date="2026-03-16", issue="미국-이란 전쟁·호르무즈 해협",
         fact="페르시아만 내 약 1,000척 선박 고립 파악, VLCC 일일 용선료 최고 4배(약 80만 달러) 폭등",
         source="보험개발원(KIDI) 보고서", url="https://bigin.kidi.or.kr:9443/data/UPLOAD/portal/nd00068/202603/research(202603).pdf"),
    dict(date="2026-07-13", issue="미국-이란 전쟁·호르무즈 해협",
         fact="트럼프 대통령, 호르무즈 통과 선박에 20% 통행료 부과 및 대이란 해상봉쇄 재개 선언",
         source="경북매일", url="https://kbmaeil.com/article/20260714500004"),
    # 이슈 2: 홍해-수에즈 운하 사태
    dict(date="2023-11-19", issue="홍해-수에즈 운하 사태",
         fact="후티 반군이 갤럭시 리더호를 나포하며 홍해 상선 공격 개시",
         source="MEES", url="https://mees.com/2025/1/10/geopolitical-risk/red-sea-shipping-in-2024-a-year-of-conflict-and-commercial-exodus/fe5ae140-cf53-11ef-84f9-85c78c1ac864"),
    dict(date="2023-12-22", issue="홍해-수에즈 운하 사태",
         fact="주요 선사들이 홍해를 피해 희망봉 우회 항로로 전환 시작",
         source="MEES", url="https://mees.com/2025/1/10/geopolitical-risk/red-sea-shipping-in-2024-a-year-of-conflict-and-commercial-exodus/fe5ae140-cf53-11ef-84f9-85c78c1ac864"),
    dict(date="2025-01-19", issue="홍해-수에즈 운하 사태",
         fact="가자 휴전 발효 이후 후티, 홍해 상선 공격 잠정 중단",
         source="NPR", url="https://www.npr.org/2025/01/29/nx-s1-5270518/with-gaza-ceasefire-yemens-houthi-rebels-halt-attacks-on-ships-in-the-red-sea"),
    # 이슈 3: 파나마 운하 리스크
    dict(date="2023-08-10", issue="파나마 운하 리스크",
         fact="최대 흘수 13.41m로 제한, 일일 통과 32회(20%↓), 대기선박 154척·대기시간 21일",
         source="이투데이 / gCaptain", url="https://www.etoday.co.kr/news/view/2274179"),
    dict(date="2025-05-31", issue="파나마 운하 리스크",
         fact="2025년 1~5월 컨테이너선 통항량 역대 최고치(1,200척 이상, 전년 동기 대비 +10.2%) 기록하며 완전 회복",
         source="트레드링스", url="https://www.tradlinx.com/blog/?p=22343"),
    dict(date="2026-07-24", issue="파나마 운하 리스크",
         fact="흘수 제한 49피트로 첫 하향 조정(이후 8/15·8/26·9/3에 걸쳐 47.5피트까지 연속 하향)",
         source="트레드링스", url="https://www.tradlinx.com/blog/?p=24572"),
]
ev_df = pd.DataFrame(EVENTS)
ev_df["date"] = pd.to_datetime(ev_df["date"])
ev_df = ev_df.sort_values("date").reset_index(drop=True)
# SCFI 라인 상의 y 위치를 보간해서 추정 (전체 df 기준, 이슈 자체의 SCFI 영향력을 주장하는 것이 아니라 위치 표시용)
ev_df["y"] = np.interp(
    ev_df["date"].astype("int64"), df["date"].astype("int64"), df["value"]
)
ISSUE_COLOR = {
    "미국-이란 전쟁·호르무즈 해협": "#e0473e",
    "홍해-수에즈 운하 사태": "#9b59b6",
    "파나마 운하 리스크": "#2f9e6f",
}

# ---------------------------------------------------------------------------
# 2) 사이드바 필터
# ---------------------------------------------------------------------------
st.sidebar.header("🔎 필터")
min_d, max_d = df["date"].min().date(), df["date"].max().date()
date_range = st.sidebar.date_input("기간 선택", (min_d, max_d), min_value=min_d, max_value=max_d)

only_verified = st.sidebar.checkbox("산술검증된 지점만 보기", value=False)
show_monthly = st.sidebar.checkbox("월평균 포함", value=True)
show_events = st.sidebar.checkbox("물류 이슈 마커 표시", value=True)

f = df.copy()
if len(date_range) == 2:
    f = f[(f["date"].dt.date >= date_range[0]) & (f["date"].dt.date <= date_range[1])]
if only_verified:
    f = f[f["verified"]]
if not show_monthly:
    f = f[f["type"] != "월평균"]

# ---------------------------------------------------------------------------
# 3) 헤더 & KPI
# ---------------------------------------------------------------------------
st.title("🚢 SCFI 추이 분석 대시보드")
st.caption("2020.01 ~ 2026.08 · 확정 백데이터 152개 지점 (2020-2023년은 2차 매체 인용 anchor, 2024년 1월-2026년 8월은 국가물류통합정보센터 공식 주간 원자료 기반)")

c1, c2, c3, c4 = st.columns(4)
c1.metric("최고치", f'{f["value"].max():,.2f} pt', f['label'][f['value'].idxmax()] if len(f) else "-")
c2.metric("최저치", f'{f["value"].min():,.2f} pt', f['label'][f['value'].idxmin()] if len(f) else "-")
c3.metric("표시 지점 수", f"{len(f)}개")
c4.metric("산술검증 지점", f'{int(f["verified"].sum())}개')

# ---------------------------------------------------------------------------
# 4) 차트
# ---------------------------------------------------------------------------
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=f["date"], y=f["value"], mode="lines+markers", name="SCFI",
    line=dict(color="#2f6fed", width=2),
    marker=dict(
        size=[10 if v else 6 for v in f["verified"]],
        color=["#2f9e6f" if v else "#2f6fed" for v in f["verified"]],
    ),
    customdata=f[["label", "source", "note"]],
    hovertemplate="<b>%{customdata[0]}</b><br>SCFI: %{y:,.2f}pt<br>출처: %{customdata[1]}<br>%{customdata[2]}<extra></extra>",
))

if show_events:
    ev_f = ev_df[(ev_df["date"].dt.date >= date_range[0]) & (ev_df["date"].dt.date <= date_range[1])] if len(date_range) == 2 else ev_df
    for issue, color in ISSUE_COLOR.items():
        sub = ev_f[ev_f["issue"] == issue]
        if sub.empty:
            continue
        fig.add_trace(go.Scatter(
            x=sub["date"], y=sub["y"], mode="markers", name=issue,
            marker=dict(size=14, color=color, symbol="triangle-up", line=dict(width=1, color="white")),
            customdata=sub[["issue", "fact", "source"]],
            hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<br>출처: %{customdata[2]}<extra></extra>",
        ))

fig.update_layout(
    height=500, margin=dict(l=10, r=10, t=30, b=10),
    xaxis_title="날짜", yaxis_title="SCFI 종합지수 (pt)",
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
)
st.plotly_chart(fig, use_container_width=True)
st.caption("초록 점: 전후 수치와 산술적으로 맞아떨어지는 지점 / 파란 점: 단일 출처 확인 지점 / 세모 마커: 글로벌 물류 이슈")

# ---------------------------------------------------------------------------
# 4-1) 글로벌 물류 이슈 상세
# ---------------------------------------------------------------------------
IMPACT = {
    "미국-이란 전쟁·호르무즈 해협": [
        "VLCC 일일 용선료 일주일 만에 최대 4배(약 300%) 폭등, 80만 달러 육박",
        "전쟁위험보험료 항차당 25만 달러 → 200만~300만 달러로 약 10배 급등",
        "페르시아만 선박 1,000척 고립, 주요 선사 운항 중단",
        "보험료·연료비 동시 급등으로 원가 예측 자체가 어려워짐",
        "카타르산 LNG(한국 수입 약 20%) 등 대체 경로 없는 자원은 의존도 낮추기도 힘듦",
    ],
    "홍해-수에즈 운하 사태": [
        "희망봉 우회로 운항 기간 2주 증가",
        "SCFI 73.17%~274% 급등",
        "안전재고·발주 시점 재조정 불가피",
        "스팟 운임 급등기엔 장기계약 비중 확대 전략 확산",
        "2025년 1월 휴전 이후에도 3월(美 대이란 군사작전)·7월(Magic Seas·Eternity C호 침몰) 공격 재발, \"끝났다\"고 보기 어려운 상태 지속",
    ],
    "파나마 운하 리스크": [
        "가뭄으로 통항 선박 수 36~38척 → 24척 감소",
        "흘수 제한으로 계획된 화물 다 못 싣는 사례 발생",
        "우선 통항권 경매에서 최대 400만 달러 지불된 사례 있음",
        "2025년 역대 최고 통항량으로 완전 회복",
        "2026년 8월부터 흘수 제한 재강화, 한 번 회복했다고 완전히 안심할 수 없는 상황",
    ],
}

st.subheader("📌 글로벌 물류 이슈")
for i, (issue, color) in enumerate(ISSUE_COLOR.items(), start=1):
    sub = ev_df[ev_df["issue"] == issue]
    st.markdown(f"### {i}. {issue}")
    st.markdown("**타임라인**")
    for _, row in sub.iterrows():
        st.markdown(
            f"- `{row['date'].date()}` {row['fact']} "
            f"([{row['source']}]({row['url']}))"
        )
    st.markdown("**파급효과**")
    for line in IMPACT[issue]:
        st.markdown(f"- {line}")
    if i < len(ISSUE_COLOR):
        st.markdown("---")
st.markdown("---")
st.caption(
    "파나마 운하 리스크는 주로 미주동안(USEC) 항로에 영향을 미치는 구조라, "
    "2023-2024년은 홍해 사태와 시기가 겹쳐서 SCFI 종합지수 변동을 파나마 요인만으로 단정하기는 어렵다."
)

# ---------------------------------------------------------------------------
# 5) 데이터 테이블
# ---------------------------------------------------------------------------
st.subheader("원자료 테이블")
show_df = f[["label", "value", "type", "note", "source", "url", "verified"]].rename(columns={
    "label": "날짜/기간", "value": "SCFI(pt)", "type": "유형",
    "note": "원문 명시 사실", "source": "매체", "url": "출처 URL", "verified": "산술검증",
})
st.dataframe(
    show_df,
    use_container_width=True,
    hide_index=True,
    column_config={"출처 URL": st.column_config.LinkColumn("출처 URL")},
)

st.download_button(
    "CSV로 다운로드",
    data=show_df.to_csv(index=False).encode("utf-8-sig"),
    file_name="scfi_confirmed_data.csv",
    mime="text/csv",
)

st.markdown("---")
st.caption(
    "2020-2023년 구간은 SSE 발표치를 인용한 2차 매체 보도에서 확인한 수치(일부 월평균 포함)이고, "
    "2024년 1월-2026년 8월 구간은 국가물류통합정보센터가 제공하는 SSE 주간 발표 원자료를 그대로 반영했다."
)

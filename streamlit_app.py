# app.py

import streamlit as st
import pandas as pd
import uuid
from datetime import date
from utils import to_decimal, find_zodiac, find_nakshatra, generate_full_dasha
from NAKSHATRA_TABLE import NAKSHATRAS

PLANET_STYLE = {
    "Ketu":    {"symbol": "☋", "color": "494529"},
    "Venus":   {"symbol": "♀", "color": "BFBFBF"},
    "Sun":     {"symbol": "☉", "color": "FF99CC"},
    "Moon":    {"symbol": "☽", "color": "FFCCFF"},
    "Mars":    {"symbol": "♂", "color": "FF0000"},
    "Rahu":    {"symbol": "☊", "color": "F2F2F2"},
    "Jupiter": {"symbol": "♃", "color": "00B050"},
    "Saturn":  {"symbol": "♄", "color": "FFFF00"},
    "Mercury": {"symbol": "☿", "color": "00B0F0"},
}

st.set_page_config(page_title="Vimshottari Dasha Calculator", layout="wide")

st.title("🌌 Vimshottari Dasha Calculator")

# --- 사용자 입력 ---
zodiac = st.selectbox("Zodiac sign", [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
])

degree = st.number_input("Degree (0-29)", min_value=0, max_value=29, value=0)
minute = st.number_input("Minute (0-59)", min_value=0, max_value=59, value=0)

birth_year = st.number_input("Birth year", min_value=1800, max_value=2100, value=1992)
birth_month = st.number_input("Birth month", min_value=1, max_value=12, value=6)
birth_day = st.number_input("Birth day", min_value=1, max_value=31, value=1)

if st.button("Calculate Dasha Chart"):
    birth_date = date(birth_year, birth_month, birth_day)

    # --- decimal 변환 ---
    decimal = to_decimal(zodiac, degree, minute)
    zod = find_zodiac(decimal)
    nak, ruler = find_nakshatra(decimal)

    st.write(f"**Zodiac**: {zod}")
    st.write(f"**Nakshatra**: {nak} (Ruler: {ruler})")

    # --- 낙샤트라 범위로 offset 계산 ---
    for info in NAKSHATRAS:
        if info["name"] == nak:
            total_minutes = (info["end"] - info["start"]) * 60
            current_minutes = (decimal - info["start"]) * 60
            offset_minutes = int(current_minutes)
            break

    # --- 대샤 계산 ---
    rows = generate_full_dasha(birth_date, ruler, offset_minutes)

    # --- DataFrame 변환 ---
    df = pd.DataFrame(rows, columns=["Date", "Age", "Lv1", "Lv2", "Lv3"])

    # 행성 기호 치환
    for col in ["Lv1", "Lv2", "Lv3"]:
        df[col] = df[col].apply(lambda x: f"{PLANET_STYLE[x]['symbol']} {x}" if x in PLANET_STYLE else x)

    st.subheader("📊 Vimshottari Dasha Chart")
    st.dataframe(df, use_container_width=True)

    # --- 엑셀 다운로드 ---
    filename = f"dasha_output_{uuid.uuid4().hex[:6]}.xlsx"
    df.to_excel(filename, index=False)

    with open(filename, "rb") as f:
        st.download_button(
            label="⬇ Download Excel",
            data=f,
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


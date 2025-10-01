# utils.py

from ZODIAC_TABLE import ZODIAC_SIGNS
from NAKSHATRA_TABLE import NAKSHATRAS
from datetime import timedelta
from DASHA_TABLE import DASHA_TABLE
from DASHA_REMAINING import DASHA_REMAINING

def generate_full_dasha(birth_date, start_planet, offset_minutes):
    rows = []
    current_date = birth_date

    dasha_order = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
    start_index = dasha_order.index(start_planet)

    # --- 첫 번째 다샤: Lv1만 (하드코딩된 잔여기간 사용) ---
    first_days = DASHA_REMAINING[start_planet][offset_minutes]
    start_date = current_date
    current_date += timedelta(days=first_days)
    age = int((start_date - birth_date).days // 365)
    rows.append([start_date, age, start_planet, "-", "-"])

    # --- 두 번째 이후: Lv2, Lv3까지 ---
    for i in range(1, 9):
        planet = dasha_order[(start_index + i) % 9]

        for lv2_planet, lv2_info in DASHA_TABLE[planet]["sub"].items():
            for lv3_planet, lv3_days in lv2_info["sub"].items():
                start_date = current_date
                current_date += timedelta(days=lv3_days)
                age = int((start_date - birth_date).days // 365)

                rows.append([
                    start_date,
                    age,
                    planet,      # Lv1
                    lv2_planet,  # Lv2
                    lv3_planet   # Lv3
                ])

    return rows




def to_decimal(zodiac: str, degree: int, minute: int) -> float:
    """
    zodiac + degree + minute → decimal degree 변환
    예: Taurus 15°30' → 45 + 15.5 = 60.5°
    """
    if zodiac not in ZODIAC_SIGNS:
        raise ValueError(f"Unknown zodiac sign: {zodiac}")
    start = ZODIAC_SIGNS[zodiac]["start"]
    return start + degree + (minute / 60)


def find_zodiac(decimal: float) -> str:
    for sign, info in ZODIAC_SIGNS.items():
        if info["start"] <= decimal < info["end"]:
            return sign
    return "Unknown"


def find_nakshatra(decimal: float) -> tuple:
    """
    decimal degree → (nakshatra 이름, ruler) 반환
    """
    for info in NAKSHATRAS:
        if info["start"] <= decimal < info["end"]:
            return info["name"], info["ruler"]
    return "Unknown", "Unknown"



def decimal_to_dms(decimal: float) -> tuple:
    """
    decimal degree → zodiac 내 degree/minute 변환
    예: 60.5 → (Taurus, 0, 30)
    """
    # zodiac 찾기
    zodiac = find_zodiac(decimal)
    ZODIAC_SIGNS[zodiac]["start"]

    # zodiac 내 degree/minute
    offset = decimal - start
    deg = int(offset)
    minute = int((offset - deg) * 60)

    return zodiac, deg, minute

def adjust_periods(periods, total_days):
    int_periods = [(p, int(d)) for p, d in periods]
    current_sum = sum(d for _, d in int_periods)
    diff = total_days - current_sum
    if diff != 0:
        last_planet, last_days = int_periods[-1]
        int_periods[-1] = (last_planet, last_days + diff)
    return int_periods


def calculate_first_dasha(moon_fraction: float, start_planet: str) -> dict:
    """
    nested DASHA_TABLE 구조에 맞게 첫 대샤 계산
    """
    lv1_days = int(DASHA_TABLE[start_planet]["length"] * moon_fraction)

    # 2단계
    lv2_raw = []
    for planet, info in DASHA_TABLE[start_planet]["sub"].items():
        lv2_raw.append((planet, info["length"] * moon_fraction))

    lv2_adjusted = adjust_periods(lv2_raw, lv1_days)

    # 3단계 (Lv1이 10년 이상일 때만)
    lv3_results = {}
    if lv1_days >= 3650:
        for planet, lv2_days in lv2_adjusted:
            lv3_raw = []
            for subplanet, sublen in DASHA_TABLE[start_planet]["sub"][planet]["sub"].items():
                lv3_raw.append((subplanet, sublen * moon_fraction))
            lv3_adjusted = adjust_periods(lv3_raw, lv2_days)
            lv3_results[planet] = lv3_adjusted

    return {
        "Lv1": (start_planet, lv1_days),
        "Lv2": lv2_adjusted,
        "Lv3": lv3_results,
    }

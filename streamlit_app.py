"""10주차 과제: 김연호의 자기소개·시간표·가보고 싶은 장소.

실행: python -m streamlit run streamlit_app.py
개인정보와 수업 시각·강의실은 사용자가 제공하고 확인한 내용을 사용합니다.
"""

from __future__ import annotations

from html import escape

import pandas as pd
import streamlit as st


# 1. 사용자 정보 — 소개문은 사용자가 직접 제공한 문장입니다.
PROFILE = {
    "name": "김연호",
    "department": "소비자학과",
    "team": "토트넘",
    "player": "손흥민",
    "introduction": (
        "안녕하세요, 소비자학과 김연호입니다.\n\n"
        "저는 축구를 정말 사랑합니다. 응원하는 팀은 토트넘이고, "
        "손흥민 선수를 진짜 좋아합니다.\n\n"
        "나중에 토트넘 핫스퍼 스타디움에서 경기를 꼭 보고 싶습니다."
    ),
}

# 수강과목은 6개, 실제 수업은 월·화·목·금 총 8회입니다.
# 강의실도 공개해 달라는 사용자 확인을 받아 포함했습니다. 학번·연락처는 넣지 않습니다.
COURSES = {
    "innovation": {"name": "창조와혁신", "short": "창조와혁신", "room": "58-323", "color": "#B56C59", "background": "#F7E6DF"},
    "accounting": {"name": "회계원리", "short": "회계원리", "room": "58-120", "color": "#758C49", "background": "#EAF0DB"},
    "writing": {"name": "대학 글쓰기 2: 사회과학글쓰기", "short": "대학 글쓰기 2", "room": "14-104", "color": "#47887F", "background": "#DFF0EC"},
    "computing": {"name": "컴퓨팅 탐색: 실생활에서 활용하기", "short": "컴퓨팅 탐색", "room": "26-104", "color": "#5A78AD", "background": "#E2EAF8"},
    "bigdata": {"name": "소비자빅데이터분석", "short": "소비자빅데이터분석", "room": "222-B202", "color": "#A58B40", "background": "#F8EECB"},
    "quantitative": {"name": "소비자정량분석론", "short": "소비자정량분석론", "room": "222-B202", "color": "#AF7747", "background": "#F8E7D7"},
}
MEETINGS = [
    {"course": "innovation", "day": "월", "start": "10:00", "end": "12:50"},
    {"course": "bigdata", "day": "월", "start": "15:30", "end": "19:20"},
    {"course": "accounting", "day": "화", "start": "11:00", "end": "12:15"},
    {"course": "writing", "day": "화", "start": "14:00", "end": "15:15"},
    {"course": "accounting", "day": "목", "start": "11:00", "end": "12:15"},
    {"course": "writing", "day": "목", "start": "14:00", "end": "15:15"},
    {"course": "computing", "day": "금", "start": "10:00", "end": "12:50"},
    {"course": "quantitative", "day": "금", "start": "14:00", "end": "17:50"},
]
DAYS = ("월", "화", "수", "목", "금")
PLACE = {
    "name": "토트넘 핫스퍼 스타디움",
    "english_name": "Tottenham Hotspur Stadium",
    "city": "런던",
    "country": "영국",
    "address": "782 High Road, London, N17 0BX",
    "lat": 51.6044,
    "lon": -0.0664,
    "reason": "응원하는 팀 토트넘의 경기를 경기장에서 직접 보고 싶습니다.",
    "official_url": "https://www.tottenhamhotspurstadium.com/",
    "coordinate_source": "https://en.wikipedia.org/wiki/Tottenham_Hotspur_Stadium",
}
PAGES = ("자기소개", "시간표", "가보고 싶은 장소")


# 2. 레이아웃 — 과제 내용은 Streamlit 요소로, 시간표 블록은 강의의 HTML 테이블 응용으로 구성합니다.
STYLE = """
<style>
.stApp { background: #F8F9FC; }
.stApp, .stApp button, .stApp input {
    font-family: 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
}
.block-container { max-width: 1260px; padding-top: 2.2rem; padding-bottom: 2rem; }
h1 { color: #132257; letter-spacing: -0.06em; font-weight: 800 !important; }
h2, h3 { color: #132257; letter-spacing: -0.035em; }
section[data-testid="stSidebar"] { background: #FFFFFF; border-right: 1px solid #E1E5EE; }
section[data-testid="stSidebar"] .block-container { padding-top: 2rem; }
.eyebrow { color: #68738B; font-size: 11px; letter-spacing: .18em; font-weight: 700; margin: 0 0 12px; }
.side-brand { color: #132257; font-weight: 900; font-size: 29px; letter-spacing: -.04em; margin: 4px 0 3px; }
.side-name { color: #7B8497; font-size: 12px; margin-bottom: 30px; }
.side-note { color: #7B8497; font-size: 11px; line-height: 1.8; margin-top: 28px; }
.profile-copy { color: #344159; font-size: 18px; line-height: 1.95; margin: 20px 0 28px; word-break: keep-all; }
.profile-copy p { margin: 0 0 18px; word-break: keep-all; overflow-wrap: normal; }
.profile-tag { display: inline-block; color: #334971; background: #E8EDF8;
    border-radius: 5px; font-size: 12px; padding: 5px 9px; margin: 0 5px 8px 0; }
.fan-pass { color: white; background: #132257; border-radius: 18px; padding: 27px 27px 24px;
    min-height: 330px; box-shadow: 0 16px 40px #13225712; }
.fan-pass .small { color: #B8C4E6; font-size: 10px; letter-spacing: .19em; }
.fan-pass .club { font-size: 36px; line-height: 1.13; letter-spacing: -.035em; font-weight: 900; margin: 25px 0 12px; }
.fan-pass .rule { border-top: 1px solid #FFFFFF33; margin: 22px 0; }
.fan-pass .pair { display: flex; justify-content: space-between; gap: 12px; margin-top: 15px; font-size: 13px; }
.fan-pass .pair span { color: #BDC9E9; }
.dream-strip { border-left: 4px solid #132257; padding: 15px 22px; background: #EDF1F9;
    color: #344159; border-radius: 0 10px 10px 0; margin: 24px 0 16px; line-height: 1.8; }
[data-testid="stMetric"] { background: white; padding: 12px 18px; border: 1px solid #E1E5EE; border-radius: 10px; }
[data-testid="stMetricValue"] { font-size: 26px; color: #132257; }
.calendar-scroll { overflow-x: auto; border: 1px solid #DCE1ED; border-radius: 12px; background: white; margin: 15px 0 5px; }
.calendar { min-width: 730px; padding-right: 12px; }
.calendar-head, .calendar-body { display: grid; grid-template-columns: 54px repeat(5, minmax(0, 1fr)); }
.calendar-head { height: 42px; background: #F0F3FA; border-bottom: 1px solid #DEE4EF; }
.calendar-day { text-align: center; padding-top: 11px; color: #394B70; font-size: 13px; font-weight: 700; }
.calendar-day.free { color: #668060; }
.calendar-body { height: 528px; position: relative; }
.time-axis { height: 100%; position: relative; color: #8A94A8; font-size: 10px; }
.time-tick { position: absolute; right: 8px; transform: translateY(-50%); font-variant-numeric: tabular-nums; }
.day-column { position: relative; border-left: 1px solid #E8EBF2;
    background: repeating-linear-gradient(to bottom, transparent 0px, transparent 23px, #EDF0F5 23px, #EDF0F5 24px); }
.day-column.free { background-color: #FAFCF9; }
.class-block { position: absolute; left: 5px; right: 5px; box-sizing: border-box;
    padding: 7px 7px 5px; border-radius: 6px; border-left: 3px solid;
    color: #243149; overflow: hidden; }
.class-name { font-weight: 700; font-size: 12px; line-height: 1.4; overflow-wrap: anywhere; }
.class-time { font-size: 10px; line-height: 1.4; margin-top: 3px; font-variant-numeric: tabular-nums; }
.class-room { font-size: 10px; line-height: 1.4; color: #536176; }
.free-label { position: absolute; top: 44%; width: 100%; text-align: center; color: #8F9C8B; font-size: 13px; }
.place-card { background: #FFFFFF; padding: 23px; border: 1px solid #DEE4EF; border-radius: 12px; min-height: 210px; }
.place-card .place-en { color: #75819B; font-size: 12px; line-height: 1.7; }
.place-card .place-ko { color: #132257; font-size: 24px; font-weight: 800; line-height: 1.45; margin: 13px 0; word-break: keep-all; }
.place-card p { font-size: 14px; line-height: 1.85; color: #475570; }
.footer-note { color: #8A94A8; font-size: 11px; margin-top: 24px; border-top: 1px solid #E2E7F0; padding-top: 12px; }
@media (max-width: 700px) {
    .block-container { padding-top: 1.4rem; }
    .profile-copy { font-size: 16px; }
    .fan-pass { min-height: 280px; margin-top: 10px; }
    h1 { font-size: 31px !important; }
}
</style>
"""


def time_minutes(value: str) -> int:
    hour, minute = map(int, value.split(":"))
    if not 0 <= hour <= 23 or not 0 <= minute < 60:
        raise ValueError(f"올바르지 않은 시간: {value}")
    return hour * 60 + minute


def validate_schedule() -> None:
    for meeting in MEETINGS:
        assert meeting["course"] in COURSES
        assert meeting["day"] in DAYS
        assert 9 * 60 <= time_minutes(meeting["start"]) < time_minutes(meeting["end"]) <= 20 * 60
    for day in DAYS:
        daily = sorted((m for m in MEETINGS if m["day"] == day), key=lambda m: m["start"])
        for first, second in zip(daily, daily[1:]):
            assert time_minutes(first["end"]) <= time_minutes(second["start"]), "겹치는 수업 시간"


def make_schedule_frame(day: str = "전체") -> pd.DataFrame:
    rows = []
    for meeting in MEETINGS:
        if day != "전체" and meeting["day"] != day:
            continue
        course = COURSES[meeting["course"]]
        rows.append({"요일": meeting["day"], "시간": f'{meeting["start"]}–{meeting["end"]}',
                     "과목명": course["name"], "강의실": course["room"]})
    return pd.DataFrame(rows, columns=["요일", "시간", "과목명", "강의실"])


def make_calendar_html(show_rooms: bool = True) -> str:
    """분 단위 좌표를 사용해 12:15·12:50·19:20을 반올림하지 않습니다."""
    start_minute, span = 9 * 60, 11 * 60
    headers = '<div></div>' + ''.join(
        f'<div class="calendar-day {"free" if day == "수" else ""}">{day}요일</div>' for day in DAYS
    )
    ticks = ''.join(
        f'<span class="time-tick" style="top:{(hour * 60 - start_minute) / span * 100:.4f}%">{hour:02d}:00</span>'
        for hour in range(10, 20)
    )
    columns = [f'<div class="time-axis">{ticks}</div>']
    for day in DAYS:
        blocks = []
        for meeting in MEETINGS:
            if meeting["day"] != day:
                continue
            course = COURSES[meeting["course"]]
            top = (time_minutes(meeting["start"]) - start_minute) / span * 100
            height = (time_minutes(meeting["end"]) - time_minutes(meeting["start"])) / span * 100
            clock = f'{meeting["start"]}–{meeting["end"]}'
            room = f'<div class="class-room">{escape(course["room"])}</div>' if show_rooms else ''
            description = escape(f'{course["name"]} / {clock} / {course["room"]}', quote=True)
            blocks.append(
                f'<div class="class-block" title="{description}" '
                f'style="top:{top:.4f}%;height:{height:.4f}%;background:{course["background"]};border-color:{course["color"]}">'
                f'<div class="class-name">{escape(course["short"])}</div>'
                f'<div class="class-time">{clock}</div>{room}</div>'
            )
        if not blocks:
            blocks.append('<div class="free-label">공강</div>')
        columns.append(f'<div class="day-column {"free" if day == "수" else ""}">{"".join(blocks)}</div>')
    return (
        '<div class="calendar-scroll" role="region" aria-label="2026년 2학기 주간 시간표"><div class="calendar">'
        f'<div class="calendar-head">{headers}</div><div class="calendar-body">{"".join(columns)}</div></div></div>'
    )


def go_to(page: str) -> None:
    st.session_state["page"] = page


def page_header(section: str, title: str, subtitle: str) -> None:
    st.markdown(f'<div class="eyebrow">WEEK 10 &nbsp; / &nbsp; {escape(section)}</div>', unsafe_allow_html=True)
    st.title(title)
    st.caption(subtitle)


# 3. 자기소개 — 텍스트, Markdown, 컬럼과 버튼
def show_profile() -> None:
    page_header("ABOUT ME", "안녕하세요, 김연호입니다.", "소비자학과 · 축구를 사랑하는 토트넘 팬")
    st.write("")
    left, right = st.columns([1.5, 1], gap="large")
    with left:
        paragraphs = ''.join(f'<p>{escape(p)}</p>' for p in PROFILE["introduction"].split("\n\n"))
        st.markdown(f'<div class="profile-copy">{paragraphs}</div>', unsafe_allow_html=True)
        st.markdown('<span class="profile-tag">소비자학과</span><span class="profile-tag">축구</span>'
                    '<span class="profile-tag">토트넘</span><span class="profile-tag">손흥민</span>', unsafe_allow_html=True)
        st.markdown('<div class="dream-strip"><strong>꼭 이루고 싶은 한 가지</strong><br>'
                    '토트넘 핫스퍼 스타디움에서 경기를 직접 관람하기.</div>', unsafe_allow_html=True)
    with right:
        st.markdown(
            '<div class="fan-pass"><div class="small">MY FOOTBALL PASS</div>'
            '<div class="club">TOTTENHAM<br>HOTSPUR</div><div>토트넘을 응원합니다.</div>'
            '<div class="rule"></div><div class="pair"><span>FAVOURITE PLAYER</span><strong>손흥민</strong></div>'
            '<div class="pair"><span>DREAM DESTINATION</span><strong>런던</strong></div>'
            '<div class="pair"><span>SUPPORTER</span><strong>김연호</strong></div></div>', unsafe_allow_html=True
        )
    st.write("")
    col1, col2, _ = st.columns([1, 1, 1.2])
    with col1:
        st.button("나의 시간표 보기 →", on_click=go_to, args=("시간표",), width="stretch")
    with col2:
        st.button("가보고 싶은 곳 보기 →", on_click=go_to, args=("가보고 싶은 장소",), width="stretch", type="primary")


# 4. 시간표 — 실제 시각을 반영한 주간 격자와 데이터프레임
def show_timetable() -> None:
    page_header("MY WEEK", "나의 일주일", "2026년 2학기 · 과목명, 수업 시간, 강의실")
    c1, c2, c3 = st.columns(3)
    c1.metric("수강 과목", f"{len(COURSES)}개")
    c2.metric("수업이 있는 요일", f"{len({m['day'] for m in MEETINGS})}일")
    c3.metric("공강인 날", "수요일")
    st.markdown(make_calendar_html(), unsafe_allow_html=True)
    st.caption("09:00–20:00 기준 · 블록 높이는 실제 수업 시간에 비례합니다. 긴 과목명은 아래 목록에서 확인하세요.")
    with st.expander("과목별 상세 시간과 강의실 보기"):
        selected_day = st.selectbox("요일별 수업", ["전체", *DAYS], key="timetable_day")
        frame = make_schedule_frame(selected_day)
        if frame.empty:
            st.info("수요일에는 등록된 수업이 없습니다. 공강입니다.")
        else:
            tab1, tab2 = st.tabs(["수업 목록", "정적 표"])
            with tab1:
                st.dataframe(frame, hide_index=True, width="stretch")
            with tab2:
                st.table(frame, hide_index=True)


# 5. 가보고 싶은 장소 — 강의의 위도·경도 지도 표시 기능
def show_destination() -> None:
    page_header("MY DREAM DESTINATION", "언젠가, 이 경기장에서", "가보고 싶은 장소 · 토트넘 핫스퍼 스타디움")
    left, right = st.columns([1.65, 1], gap="large")
    with left:
        zoom = st.selectbox("지도 범위", ["경기장 주변", "런던에서의 위치"], key="map_range")
        location = pd.DataFrame([{"lat": PLACE["lat"], "lon": PLACE["lon"]}])
        st.map(location, latitude="lat", longitude="lon", color="#132257", size=85,
               zoom=14 if zoom == "경기장 주변" else 9, height=430, width="stretch")
        st.caption("표시점은 경기장 부근의 대표 위치입니다. 입구·좌석 안내용 좌표는 아닙니다.")
    with right:
        st.markdown(
            f'<div class="place-card"><div class="eyebrow">LONDON, UNITED KINGDOM</div>'
            f'<div class="place-ko">{escape(PLACE["name"])}</div>'
            f'<div class="place-en">{escape(PLACE["english_name"])}</div>'
            f'<p>{escape(PLACE["reason"])}</p><div class="place-en">{escape(PLACE["address"])}</div></div>',
            unsafe_allow_html=True,
        )
        st.markdown("#### 가보고 싶은 이유")
        st.write("축구를 정말 사랑하고 토트넘을 응원하기 때문에, 이곳에서 경기를 직접 관람하고 싶습니다.")
        st.markdown(f'[경기장 공식 홈페이지 ↗]({PLACE["official_url"]})')
        with st.expander("위치 정보와 출처"):
            st.checkbox("위도·경도 표시", key="show_coordinates")
            if st.session_state.get("show_coordinates", False):
                st.table(pd.DataFrame([{"위도": PLACE["lat"], "경도": PLACE["lon"]}]), hide_index=True)
            st.markdown(f'주소: [경기장 공식 홈페이지]({PLACE["official_url"]})')
            st.markdown(f'대표 좌표: [경기장 위치 자료]({PLACE["coordinate_source"]})')


# 6. 메뉴와 화면 함수 연결 — 강의의 함수 매핑 예제 응용
def main() -> None:
    st.set_page_config(page_title="김연호 | 축구와 캠퍼스", page_icon="⚽", layout="wide")
    validate_schedule()
    st.markdown(STYLE, unsafe_allow_html=True)
    with st.sidebar:
        st.markdown('<div class="side-brand">KYH /</div><div class="side-name">FOOTBALL & CAMPUS</div>', unsafe_allow_html=True)
        st.radio("페이지 선택", PAGES, key="page", label_visibility="collapsed")
        st.divider()
        st.markdown("**김연호**  \n소비자학과")
        st.caption("축구와 함께하는 캠퍼스 라이프")
        st.markdown('<div class="side-note">2026 · 2학기<br>컴퓨팅 탐색 10주차 과제<br>'
                    '개인 소개 페이지이며 구단 공식 사이트가 아닙니다.</div>', unsafe_allow_html=True)
    page_functions = {"자기소개": show_profile, "시간표": show_timetable, "가보고 싶은 장소": show_destination}
    page_functions[st.session_state["page"]]()
    st.markdown('<div class="footer-note">김연호 · 소비자학과 &nbsp; / &nbsp; Streamlit으로 만든 나의 소개 페이지</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()

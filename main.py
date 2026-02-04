import streamlit as st
import pandas as pd
import requests
import json
import os
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone

# --- CONFIG & PROFESSIONAL STYLING ---
st.set_page_config(page_title="Business Weather Pro", layout="wide")

st.markdown("""
    <style>
    a.header-anchor { display: none !important; }
    .viewerBadge_container__1QS1n { display: none; }
    .block-container { padding-top: 1rem !important; }
    .data-label { font-weight: bold; color: #555; text-transform: uppercase; font-size: 0.85rem; margin-bottom: 2px; }
    .data-value { font-size: 1.1rem; color: #111; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- SETTINGS & PERSISTENCE ---
SETTINGS_FILE = "settings.json"


def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f: return json.load(f)
    return {"favorites": [], "default_city": "New York", "units": "metric"}


def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f: json.dump(settings, f)


if 'settings' not in st.session_state: st.session_state.settings = load_settings()
if 'active_city' not in st.session_state: st.session_state.active_city = st.session_state.settings.get("default_city")

# --- API & DATA SOURCES ---
API_KEY = st.secrets["WEATHER_API_KEY"]
CSV_URL = "https://raw.githubusercontent.com/erezgrn3112-stack/weather_automation/main/weather_data.csv"


def fetch_weather(city, units):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={API_KEY}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None


def fetch_forecast(city, units):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&units={units}&appid={API_KEY}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None


@st.cache_data(show_spinner=False)
def load_historical(): return pd.read_csv(CSV_URL)


# --- SIDEBAR & NAVIGATION ---
with st.sidebar:
    st.title("📌 Saved Destinations")
    if st.session_state.settings["favorites"]:
        for fav in st.session_state.settings["favorites"]:
            if st.button(f"📍 {fav}", key=f"nav_{fav}", use_container_width=True):
                st.session_state.active_city = fav;
                st.rerun()
    st.divider()
    if st.button("Clear All Favorites"):
        st.session_state.settings["favorites"] = [];
        save_settings(st.session_state.settings);
        st.rerun()

st.title("Business Travel Control Center")
df_raw = load_historical()

if not df_raw.empty:
    st.subheader("Choose Your Next Destination")
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
    with c1:
        cont = st.selectbox("Continent", df_raw['continent'].unique())
    with c2:
        country = st.selectbox("Country", df_raw[df_raw['continent'] == cont]['country'].unique())
    with c3:
        city_option = st.selectbox("City", df_raw[df_raw['country'] == country]['city'].unique())
    with c4:
        st.markdown('<div style="padding-top: 28px;"></div>', unsafe_allow_html=True)
        if st.button("Show Weather", use_container_width=True): st.session_state.active_city = city_option

# --- MAIN DISPLAY ---
if st.session_state.active_city:
    active = st.session_state.active_city
    data = fetch_weather(active, st.session_state.settings["units"])

    if data:
        st.divider()
        is_f = st.session_state.settings["units"] == "imperial"
        unit_sym = "°F" if is_f else "°C"
        current_temp = round(data['main']['temp'])

        # זמן מקומי מדויק
        tz_offset = timedelta(seconds=data['timezone'])
        dt_now = datetime.now(timezone.utc) + tz_offset
        dt_now = dt_now.replace(tzinfo=None)  # לצורך השוואת Pandas

        col_main, col_map = st.columns([1.5, 1])
        with col_main:
            icon_url = f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
            c_icon, c_text = st.columns([1, 5])
            with c_icon:
                st.image(icon_url, width=100)
            with c_text:
                st.markdown(f"## {active}: {dt_now.strftime('%H:%M')} | {current_temp}{unit_sym}")
                st.markdown(
                    f'<div class="data-label">Date:</div><div class="data-value">{dt_now.strftime("%A, %B %d, %Y")}</div>',
                    unsafe_allow_html=True)
                st.markdown(
                    f'<div class="data-label">Conditions:</div><div class="data-value">{data["weather"][0]["description"].capitalize()}</div>',
                    unsafe_allow_html=True)

            c_unit, c_fav, c_def = st.columns(3)
            with c_unit:
                if st.button(f"Switch to {'°C' if is_f else '°F'}", use_container_width=True):
                    st.session_state.settings["units"] = "metric" if is_f else "imperial";
                    save_settings(st.session_state.settings);
                    st.rerun()
            with c_fav:
                if active in st.session_state.settings["favorites"]:
                    st.write("✅ In Your List")
                    if st.button("🗑️ Remove", use_container_width=True):
                        st.session_state.settings["favorites"].remove(active);
                        save_settings(st.session_state.settings);
                        st.rerun()
                else:
                    if st.button("⭐ Save to List", use_container_width=True):
                        st.session_state.settings["favorites"].append(active);
                        save_settings(st.session_state.settings);
                        st.rerun()
            with c_def:
                if st.button("🏠 Set Default", use_container_width=True):
                    st.session_state.settings["default_city"] = active;
                    save_settings(st.session_state.settings);
                    st.success("Home Set")

            st.markdown("---")
            st.subheader("🎒 Packing Essentials")
            temp_c = data['main']['temp'] if not is_f else (data['main']['temp'] - 32) * 5 / 9
            items = ["Laptop & Charger", "Business Passport", "Local Currency"]
            if temp_c < 15:
                items += ["Heavy Coat", "Warm Scarf"]
            elif temp_c > 25:
                items += ["Sunscreen", "Light Business Wear"]
            else:
                items += ["Light Blazer", "Comfortable Walking Shoes"]
            for item in items: st.markdown(f"- {item}")

        with col_map:
            st.subheader("Destination Map")
            map_df = pd.DataFrame({'lat': [data['coord']['lat']], 'lon': [data['coord']['lon']]})
            st.map(map_df, zoom=10)

        # --- GRAPH SECTION: SYMMETRICAL DYNAMIC WINDOWS ---
        st.divider()
        hist = df_raw[df_raw['city'] == active].copy()

        # 1. HISTORICAL TRENDS (PAST)
        st.subheader("📊 Weather Trend Analysis (Past)")
        if len(hist) > 1:
            hist['local_time'] = pd.to_datetime(hist['local_time']).dt.tz_localize(None)
            if is_f: hist['temp'] = (hist['temp'] * 9 / 5) + 32
            hist['temp'] = hist['temp'].round()

            g1_c1, g1_c2 = st.columns(2)

            with g1_c1:
                last_7_days = hist[hist['local_time'] > (dt_now - timedelta(days=7))].copy()
                if not last_7_days.empty:
                    weekly_avg = last_7_days.set_index('local_time').resample('D').mean(
                        numeric_only=True).round().reset_index()
                    weekly_avg['day_index'] = range(len(weekly_avg))
                    lm_weekly = sns.lmplot(data=weekly_avg, x='day_index', y='temp', height=4, aspect=1.3,
                                           scatter_kws={'s': 50}, line_kws={'color': 'red'})
                    lm_weekly.set(title="7-Day Historical Average")
                    lm_weekly.set_axis_labels("Date", f"Temp ({unit_sym})")
                    plt.xlim(weekly_avg['day_index'].min() - 0.5, weekly_avg['day_index'].max() + 0.5)
                    plt.xticks(weekly_avg['day_index'], weekly_avg['local_time'].dt.strftime('%b %d'))
                    st.pyplot(lm_weekly.fig)

            with g1_c2:
                # 24-Hour Past Pulse (Dynamic Window)
                past_24h = hist[hist['local_time'] > (dt_now - timedelta(hours=24))].copy()
                if not past_24h.empty:
                    min_t = past_24h['local_time'].min()
                    max_t = past_24h['local_time'].max()
                    past_24h['rel_hour'] = (past_24h['local_time'] - min_t).dt.total_seconds() / 3600
                    lm_h_past = sns.lmplot(data=past_24h, x='rel_hour', y='temp', height=4, aspect=1.3,
                                           scatter_kws={'s': 40, 'alpha': 0.7}, line_kws={'color': 'orange'})
                    lm_h_past.set(title="Last 24-Hour Pulse")
                    lm_h_past.set_axis_labels("Time", f"Temp ({unit_sym})")

                    # לוגיקה לשעות עגולות (00, 06, 12, 18)
                    p_ticks = []
                    for day in [min_t.date(), (min_t + timedelta(days=1)).date()]:
                        for h in [0, 6, 12, 18]:
                            p_ticks.append(datetime.combine(day, datetime.min.time().replace(hour=h)))
                    p_final = sorted([t for t in p_ticks if min_t <= t <= max_t])

                    plt.xticks([(t - min_t).total_seconds() / 3600 for t in p_final],
                               [t.strftime('%H:00') for t in p_final])
                    plt.xlim(-0.5, past_24h['rel_hour'].max() + 0.5)
                    st.pyplot(lm_h_past.fig)

        # 2. FORECAST TRENDS (FUTURE)
        st.divider()
        st.subheader("🔮 Future Forecast Analysis")
        f_data = fetch_forecast(active, st.session_state.settings["units"])

        if f_data:
            # המרת תחזית לזמן מקומי (UTC -> Local)
            f_tz_offset = timedelta(seconds=f_data['city']['timezone'])
            f_list = []
            for entry in f_data['list']:
                f_dt = (pd.to_datetime(entry['dt_txt']) + f_tz_offset).replace(tzinfo=None)
                f_list.append({'dt': f_dt, 'temp': round(entry['main']['temp'])})
            df_f = pd.DataFrame(f_list)

            g2_c1, g2_c2 = st.columns(2)

            with g2_c1:
                f_weekly_avg = df_f.set_index('dt').resample('D').mean(numeric_only=True).round().reset_index()
                f_weekly_avg['day_index'] = range(len(f_weekly_avg))
                lm_f_weekly = sns.lmplot(data=f_weekly_avg, x='day_index', y='temp', height=4, aspect=1.3,
                                         scatter_kws={'s': 50}, line_kws={'color': 'green'})
                lm_f_weekly.set(title="Upcoming 5-Day Average")
                lm_f_weekly.set_axis_labels("Date", f"Temp ({unit_sym})")
                plt.xlim(f_weekly_avg['day_index'].min() - 0.5, f_weekly_avg['day_index'].max() + 0.5)
                plt.xticks(f_weekly_avg['day_index'], f_weekly_avg['dt'].dt.strftime('%b %d'))
                st.pyplot(lm_f_weekly.fig)

            with g2_c2:
                # 24-Hour Forecast Pulse (Dynamic Alignment)
                f_24h = df_f.head(8).copy()
                f_min_t = f_24h['dt'].min()
                f_max_t = f_24h['dt'].max()
                f_24h['rel_hour'] = (f_24h['dt'] - f_min_t).dt.total_seconds() / 3600
                lm_f_24 = sns.lmplot(data=f_24h, x='rel_hour', y='temp', height=4, aspect=1.3, scatter_kws={'s': 40},
                                     line_kws={'color': 'blue'})
                lm_f_24.set(title="Upcoming 24-Hour Forecast")
                lm_f_24.set_axis_labels("Time", f"Temp ({unit_sym})")

                # לוגיקה לשעות עגולות בתחזית (00, 06, 12, 18)
                f_ticks = []
                for day in [f_min_t.date(), (f_min_t + timedelta(days=1)).date()]:
                    for h in [0, 6, 12, 18]:
                        f_ticks.append(datetime.combine(day, datetime.min.time().replace(hour=h)))
                f_final = sorted([t for t in f_ticks if f_min_t <= t <= f_max_t])

                plt.xticks([(t - f_min_t).total_seconds() / 3600 for t in f_final],
                           [t.strftime('%H:00') for t in f_final])
                plt.xlim(-0.5, f_24h['rel_hour'].max() + 0.5)
                st.pyplot(lm_f_24.fig)
        else:
            st.warning("Forecast data is currently unavailable.")
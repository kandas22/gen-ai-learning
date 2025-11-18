import os
from contextlib import contextmanager

import requests
import streamlit as st

try:
    from streamlit_extras.stylable_container import stylable_container  # type: ignore
except ImportError:
    @contextmanager
    def stylable_container(key: str, css_styles: str):
        with st.container():
            yield


st.set_page_config(
    page_title="Day 5 • Unit Converter",
    page_icon="🔄",
    layout="wide",
)

CUSTOM_STYLE = """
    <style>
        body {
            background: radial-gradient(circle at top, #1f3b70, #05060a);
            color: #f5f6fb;
        }
        section[data-testid="stSidebar"] {
            background: #0f172a;
        }
        .stMetric {
            background: rgba(15, 23, 42, 0.55);
            padding: 0.8rem;
            border-radius: 12px;
        }
        .stRadio > label {
            font-weight: 600;
        }
        .embedded-header {
            display: flex;
            gap: 1rem;
            align-items: center;
            margin-bottom: 0.8rem;
        }
        .embedded-icon {
            font-size: 1.75rem;
        }
        .embedded-title {
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
            line-height: 1.2;
        }
        .embedded-subtitle {
            font-size: 0.95rem;
            color: rgba(255, 255, 255, 0.75);
        }
    </style>
"""
st.markdown(CUSTOM_STYLE, unsafe_allow_html=True)

REACTIVE_CARD_STYLE = """
{
    background: rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 1.75rem;
    box-shadow: 0 25px 60px rgba(15, 15, 35, 0.35);
    border: 1px solid rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(16px);
}
"""


@st.cache_data(ttl=3600)
def fetch_live_rate(base: str = "USD", target: str = "INR") -> tuple[float | None, str]:
    api_key = os.getenv("EXCHANGERATE_HOST_API_KEY")

    primary_url = "https://api.exchangerate.host/latest"
    fallback_url = f"https://open.er-api.com/v6/latest/{base}"

    try:
        params = {"base": base, "symbols": target}
        if api_key:
            params["apikey"] = api_key
        response = requests.get(primary_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "rates" in data and target in data["rates"]:
            return float(data["rates"][target]), "exchangerate.host"
        raise ValueError("Unexpected response payload.")
    except Exception:
        try:
            response = requests.get(fallback_url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("result") == "success":
                rate = data["rates"][target]
                return float(rate), "open.er-api.com"
        except Exception:
            return None, ""
    return None, ""


CITY_COORDS = {
    "Delhi": (28.6139, 77.209),
    "Mumbai": (19.076, 72.8777),
    "Bengaluru": (12.9716, 77.5946),
    "Hyderabad": (17.385, 78.4867),
    "Chennai": (13.0827, 80.2707),
    "New York": (40.7128, -74.006),
    "Madurai": (9.9252, 78.1198),
}


@st.cache_data(ttl=900)
def fetch_live_temperature(city: str) -> float | None:
    lat, lon = CITY_COORDS[city]
    url = "https://api.open-meteo.com/v1/forecast"
    try:
        response = requests.get(
            url,
            params={"latitude": lat, "longitude": lon, "current_weather": True},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        return float(data["current_weather"]["temperature"])
    except Exception:
        return None


def segmented_control(label: str, options: list[str], key: str):
    return st.radio(label, options=options, horizontal=True, key=key)


def converter_card(
    icon: str,
    title: str,
    subtitle: str,
    primary_label: str,
    primary_unit: str,
    secondary_label: str,
    secondary_unit: str,
    forward_converter,
    backward_converter,
    default_value: float,
    precision: int = 2,
    accent: str = "#f5f6fb",
):
    with stylable_container(
        key=f"{title}-card",
        css_styles=REACTIVE_CARD_STYLE,
    ):
        render_card_header(icon, title, subtitle, accent)

        direction = segmented_control(
            "Direction",
            [f"{primary_unit} → {secondary_unit}", f"{secondary_unit} → {primary_unit}"],
            key=f"{title}-direction",
        )

        col_input, col_output = st.columns(2, gap="large")

        if direction == f"{primary_unit} → {secondary_unit}":
            input_value = col_input.number_input(
                primary_label,
                min_value=0.0,
                value=float(default_value),
                key=f"{title}-input-primary",
            )
            converted = forward_converter(input_value)
            col_output.metric(
                label=secondary_label,
                value=f"{converted:.{precision}f} {secondary_unit}",
                delta=None,
            )
        else:
            input_value = col_input.number_input(
                secondary_label,
                min_value=0.0,
                value=float(default_value),
                key=f"{title}-input-secondary",
            )
            converted = backward_converter(input_value)
            col_output.metric(
                label=primary_label,
                value=f"{converted:.{precision}f} {primary_unit}",
                delta=None,
            )


st.title("Day 5 • Build a Unit Converter 🔄")
st.caption("React-inspired Streamlit surface that responds in real time while you type!")


# Conversion helpers ----------------------------------------------------------
USD_TO_INR_FALLBACK = 83.0
CM_TO_INCH = 0.393701
KG_TO_LB = 2.20462

CARD_ACCENTS = {
    "Currency": "#facc15",
    "Temperature": "#f97316",
    "Length": "#38bdf8",
    "Weight": "#a855f7",
}


def celsius_to_fahrenheit(value: float) -> float:
    return (value * 9 / 5) + 32


def fahrenheit_to_celsius(value: float) -> float:
    return (value - 32) * 5 / 9


def cm_to_inch(value: float) -> float:
    return value * CM_TO_INCH


def inch_to_cm(value: float) -> float:
    return value / CM_TO_INCH


def kg_to_lb(value: float) -> float:
    return value * KG_TO_LB


def lb_to_kg(value: float) -> float:
    return value / KG_TO_LB


def render_card_header(icon: str, title: str, subtitle: str, accent: str):
    st.markdown(
        f"""
        <div class="embedded-header">
            <div class="embedded-icon" style="color:{accent};">{icon}</div>
            <div>
                <div class="embedded-title" style="color:{accent};">{title}</div>
                <div class="embedded-subtitle">{subtitle}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Specialized cards -----------------------------------------------------------
def currency_card():
    with stylable_container("currency-card", REACTIVE_CARD_STYLE):
        render_card_header(
            icon="💰",
            title="Currency",
            subtitle="INR ↔ USD powered by exchangerate.host (fallback: open.er-api / static).",
            accent=CARD_ACCENTS["Currency"],
        )

        use_live_rate = st.toggle(
            "Use live FX rate", value=False, key="currency-live-toggle"
        )
        live_rate, rate_source = fetch_live_rate() if use_live_rate else (None, "")
        effective_rate = live_rate or USD_TO_INR_FALLBACK

        if use_live_rate and live_rate is None:
            st.warning(
                "Live FX fetch failed. Using fallback rate "
                f"{USD_TO_INR_FALLBACK:.2f} INR per USD."
            )

        rate_label = (
            f"{rate_source} (cached 1h)" if live_rate else "Fallback (manual)"
        )
        st.markdown(
            f"**Current rate:** 1 USD = `{effective_rate:.4f}` INR — {rate_label}",
        )

        direction = segmented_control(
            "Direction",
            ["INR → USD", "USD → INR"],
            key="currency-direction",
        )

        col_input, col_output = st.columns(2, gap="large")

        if direction == "INR → USD":
            amount_inr = col_input.number_input(
                "Amount in INR",
                min_value=0.0,
                value=100.0,
                key="currency-inr",
            )
            converted = amount_inr / effective_rate
            col_output.metric(
                "Amount in USD",
                f"{converted:.2f} USD",
            )
        else:
            amount_usd = col_input.number_input(
                "Amount in USD",
                min_value=0.0,
                value=100.0,
                key="currency-usd",
            )
            converted = amount_usd * effective_rate
            col_output.metric(
                "Amount in INR",
                f"{converted:.2f} INR",
            )

        st.caption(
            "Rates cached for 1 hour. Update frequency depends on exchangerate.host."
        )


def temperature_card():
    with stylable_container("temperature-card", REACTIVE_CARD_STYLE):
        render_card_header(
            icon="🌡️",
            title="Temperature",
            subtitle="Convert °C ↔ °F with optional live readings from Open-Meteo.",
            accent=CARD_ACCENTS["Temperature"],
        )

        city = st.selectbox("City for live weather", list(CITY_COORDS), key="city")
        use_live_temp = st.toggle(
            "Use live city temperature", value=False, key="temperature-live-toggle"
        )
        live_temp = fetch_live_temperature(city) if use_live_temp else None

        if use_live_temp and live_temp is None:
            st.warning(
                "Unable to fetch live temperature right now. "
                "Defaulting to manual entry."
            )

        base_value = live_temp if live_temp is not None else 25.0
        if live_temp is not None:
            st.markdown(f"**Live temperature:** `{live_temp:.1f}°C`")

        direction = segmented_control(
            "Direction",
            ["°C → °F", "°F → °C"],
            key="temperature-direction",
        )

        col_input, col_output = st.columns(2, gap="large")

        if direction == "°C → °F":
            temp_c = col_input.number_input(
                "Temperature in °C",
                value=float(base_value),
                key="temp-c",
            )
            converted = celsius_to_fahrenheit(temp_c)
            col_output.metric("Temperature in °F", f"{converted:.1f} °F")
        else:
            temp_f = col_input.number_input(
                "Temperature in °F",
                value=float(celsius_to_fahrenheit(base_value)),
                key="temp-f",
            )
            converted = fahrenheit_to_celsius(temp_f)
            col_output.metric("Temperature in °C", f"{converted:.1f} °C")

        st.caption("Weather data cached for 15 minutes via api.open-meteo.com.")


# Layout ----------------------------------------------------------------------
col_left, col_right = st.columns(2, gap="medium")

with col_left:
    currency_card()

with col_right:
    temperature_card()

with col_left:
    converter_card(
        icon="📏",
        title="Length",
        subtitle="Precise cm ↔ inch conversions for design specs.",
        primary_label="Length in cm",
        primary_unit="cm",
        secondary_label="Length in inches",
        secondary_unit="in",
        forward_converter=cm_to_inch,
        backward_converter=inch_to_cm,
        default_value=10.0,
        precision=3,
        accent=CARD_ACCENTS["Length"],
    )

with col_right:
    converter_card(
        icon="🏋️",
        title="Weight",
        subtitle="Switch between kilograms and pounds effortlessly.",
        primary_label="Weight in kg",
        primary_unit="kg",
        secondary_label="Weight in pounds",
        secondary_unit="lb",
        forward_converter=kg_to_lb,
        backward_converter=lb_to_kg,
        default_value=1.0,
        precision=3,
        accent=CARD_ACCENTS["Weight"],
    )


st.info(
    "⚡ These conversions update live as you type. Currency rates auto-refresh hourly "
    "via exchangerate.host (fallback to open.er-api/static). Set "
    "`EXCHANGERATE_HOST_API_KEY` for higher limits."
)


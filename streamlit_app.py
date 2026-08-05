import streamlit as st

from CoolProp.CoolProp import PropsSI

 

# -----------------------------

# Page config must come first

# -----------------------------

st.set_page_config(page_title="Hydrogen Tubetrailer Transfer Calculator", layout="centered")

 

# -----------------------------

# Language setup

# -----------------------------

if "lang" not in st.session_state:

    st.session_state.lang = "en"

 

def toggle_language():

    st.session_state.lang = "nl" if st.session_state.lang == "en" else "en"

    st.rerun()

 

translations = {

    "en": {

        "page_title": "Hydrogen Tubetrailer Transfer Calculator",

        "title": "Hydrogen Tubetrailer Transfer Calculator",

        "description": """

Calculate hydrogen mass in a constant-volume tubetrailer before and after a transfer process.

 

The app uses thermodynamic models in CoolProp to compute hydrogen density from pressure and temperature.

""",

        "language_button": "Switch to Dutch",

        "inputs": "Inputs",

        "volume": "Tubetrailer volume [m³]",

        "initial_state": "Initial state",

        "final_state": "Final state",

        "initial_temperature": "Initial temperature [°C]",

        "initial_pressure": "Initial pressure [bar]",

        "final_temperature": "Final temperature [°C]",

        "final_pressure": "Final pressure [bar]",

        "results": "Results",

        "calculate": "Calculate",

        "success": "Calculation completed successfully.",

        "initial_density": "Initial density",

        "initial_mass": "Initial mass",

        "final_density": "Final density",

        "final_mass": "Final mass",

        "transferred_mass": "Transferred H₂ mass",

        "calculation_details": "Calculation details",

        "volume_label": "Volume",

        "initial_state_label": "Initial state",

        "final_state_label": "Final state",

        "error": "Error during calculation",

        "error_info": "Please check that the pressure and temperature inputs are within valid CoolProp ranges for hydrogen.",

        "logo_caption": "This application is owned and managed by MV Energietechniek."

    },

    "nl": {

        "page_title": "Waterstof Tubetrailer Calculator",

        "title": "Waterstof Tubetrailer Calculator",

        "description": """

Bereken de waterstofmassa in een tubetrailer met constant volume voor en na het vullen of legen van een H2 tubetrailer.

 

De app gebruikt thermodynamische modellen in CoolProp om de waterstofdichtheid te berekenen op basis van druk en temperatuur.

""",

        "language_button": "Schakel naar Engels",

        "inputs": "Invoer",

        "volume": "Tubetrailer volume [m³]",

        "initial_state": "Begintoestand",

        "final_state": "Eindtoestand",

        "initial_temperature": "Begintemperatuur [°C]",

        "initial_pressure": "Begindruk [bar]",

        "final_temperature": "Eindtemperatuur [°C]",

        "final_pressure": "Einddruk [bar]",

        "results": "Resultaten",

        "calculate": "Berekenen",

        "success": "Berekening succesvol uitgevoerd.",

        "initial_density": "Begindichtheid",

        "initial_mass": "Beginmassa",

        "final_density": "Einddichtheid",

        "final_mass": "Eindmassa",

        "transferred_mass": "Overgedragen H₂-massa",

        "calculation_details": "Berekeningsdetails",

        "volume_label": "Volume",

        "initial_state_label": "Begintoestand",

        "final_state_label": "Eindtoestand",

        "error": "Fout tijdens berekening",

        "error_info": "Controleer of de ingevoerde druk- en temperatuurwaarden binnen het geldige CoolProp-bereik voor waterstof vallen.",

        "logo_caption": "Deze applicatie is eigendom van en wordt beheerd door MV Energietechniek."

    }

}

 

t = translations[st.session_state.lang]

 

# -----------------------------

# Language toggle button

# -----------------------------

st.button(t["language_button"], on_click=toggle_language)

 

# Refresh translation after possible rerun

t = translations[st.session_state.lang]

 

# -----------------------------

# UI

# -----------------------------

st.image(

    "MVE_Logo.png",

    caption=t["logo_caption"],

    use_container_width=True

)

 

st.title(t["title"])

st.write(t["description"])

 

st.header(t["inputs"])

 

volume = st.number_input(

    t["volume"],

    min_value=0.001,

    value=40.0,

    step=0.1

)

 

col1, col2 = st.columns(2)

 

with col1:

    st.subheader(t["initial_state"])

    T_initial_C = st.number_input(

        t["initial_temperature"],

        value=15.0,

        step=0.1,

        key="T_initial"

    )

    P_initial_bar = st.number_input(

        t["initial_pressure"],

        min_value=0.0,

        value=300.0,

        step=1.0,

        key="P_initial"

    )

 

with col2:

    st.subheader(t["final_state"])

    T_final_C = st.number_input(

        t["final_temperature"],

        value=15.0,

        step=0.1,

        key="T_final"

    )

    P_final_bar = st.number_input(

        t["final_pressure"],

        min_value=0.0,

        value=50.0,

        step=1.0,

        key="P_final"

    )

 

# Unit conversions

T_initial_K = T_initial_C + 273.15

T_final_K = T_final_C + 273.15

P_initial_Pa = P_initial_bar * 1e5

P_final_Pa = P_final_bar * 1e5

 

st.header(t["results"])

 

if st.button(t["calculate"]):

    try:

        rho_initial = PropsSI("D", "T", T_initial_K, "P", P_initial_Pa, "Hydrogen")

        rho_final = PropsSI("D", "T", T_final_K, "P", P_final_Pa, "Hydrogen")

 

        m_initial = rho_initial * volume

        m_final = rho_final * volume

        m_transferred = m_initial - m_final

 

        st.success(t["success"])

 

        col3, col4, col5 = st.columns(3)

 

        with col3:

            st.metric(t["initial_density"], f"{rho_initial:.4f} kg/m³")

            st.metric(t["initial_mass"], f"{m_initial:.4f} kg")

 

        with col4:

            st.metric(t["final_density"], f"{rho_final:.4f} kg/m³")

            st.metric(t["final_mass"], f"{m_final:.4f} kg")

 

        with col5:

            st.metric(t["transferred_mass"], f"{m_transferred:.4f} kg")

 

        st.subheader(t["calculation_details"])

        st.write(f"**{t['volume_label']}:** {volume:.4f} m³")

        st.write(f"**{t['initial_state_label']}:** {T_initial_C:.2f} °C, {P_initial_bar:.2f} bar")

        st.write(f"**{t['final_state_label']}:** {T_final_C:.2f} °C, {P_final_bar:.2f} bar")

 

    except Exception as e:

        st.error(f"{t['error']}: {e}")

        st.info(t["error_info"])

 

st.markdown("---")

st.caption("© 2026 MV Energietechniek. All rights reserved.")
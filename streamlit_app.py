import streamlit as st

from CoolProp.CoolProp import PropsSI

 
st.set_page_config(page_title="Hydrogen Tubetrailer Transfer Calculator", layout="centered")

st.title("Hydrogen Tubetrailer Transfer Calculator")

st.write(

    """

    Calculate hydrogen mass in a constant-volume tubetrailer before and after a transfer process.

    The app uses CoolProp to compute hydrogen density from pressure and temperature.

    """

)

 

st.header("Inputs")

 

volume = st.number_input(

    "Tubetrailer volume [m³]",

    min_value=0.001,

    value=40.0,

    step=0.1

)

 

col1, col2 = st.columns(2)

 

with col1:

    st.subheader("Initial state")

    T_initial_C = st.number_input(

        "Initial temperature [°C]",

        value=15.0,

        step=0.1,

        key="T_initial"

    )

    P_initial_bar = st.number_input(

        "Initial pressure [bar]",

        min_value=0.0,

        value=300.0,

        step=1.0,

        key="P_initial"

    )

 

with col2:

    st.subheader("Final state")

    T_final_C = st.number_input(

        "Final temperature [°C]",

        value=15.0,

        step=0.1,

        key="T_final"

    )

    P_final_bar = st.number_input(

        "Final pressure [bar]",

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

 

st.header("Results")

 

if st.button("Calculate"):

    try:

        # Density from CoolProp

        rho_initial = PropsSI("D", "T", T_initial_K, "P", P_initial_Pa, "Hydrogen")

        rho_final = PropsSI("D", "T", T_final_K, "P", P_final_Pa, "Hydrogen")

 

        # Mass calculations

        m_initial = rho_initial * volume

        m_final = rho_final * volume

        m_transferred = m_initial - m_final

 

        st.success("Calculation completed successfully.")

 

        col3, col4, col5 = st.columns(3)

 

        with col3:

            st.metric("Initial density", f"{rho_initial:.4f} kg/m³")

            st.metric("Initial mass", f"{m_initial:.4f} kg")

 

        with col4:

            st.metric("Final density", f"{rho_final:.4f} kg/m³")

            st.metric("Final mass", f"{m_final:.4f} kg")

 

        with col5:

            st.metric("Transferred H₂ mass", f"{m_transferred:.4f} kg")

 

        st.subheader("Calculation details")

        st.write(f"**Volume:** {volume:.4f} m³")

        st.write(f"**Initial state:** {T_initial_C:.2f} °C, {P_initial_bar:.2f} bar")

        st.write(f"**Final state:** {T_final_C:.2f} °C, {P_final_bar:.2f} bar")

 

    except Exception as e:

        st.error(f"Error during calculation: {e}")

        st.info("Please check that the pressure and temperature inputs are within valid CoolProp ranges for hydrogen.")
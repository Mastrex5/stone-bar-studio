import streamlit as st
from models.material_calculator import calculate_bom
from utils.data_handler import save_project

def show_page():
    st.title("Material Prep & Planning Studio")
    st.markdown("Calculate the Bill of Materials for your custom stone bar.")

    # Inputs
    shape = st.selectbox("Bar Shape", ["Rectangular", "L-Shape"])
    col1, col2, col3 = st.columns(3)
    with col1:
        length = st.number_input("Main Length (ft)", min_value=0.0, step=0.1)
    with col2:
        width = st.number_input("Main Width (ft)", min_value=0.0, step=0.1)
    with col3:
        height = st.number_input("Height (ft)", min_value=0.0, step=0.1)

    waste_factor = st.slider("Waste Factor (%)", 0, 50, 10)

    if shape == "L-Shape":
        st.subheader("L-Shape Leg Dimensions")
        col4, col5 = st.columns(2)
        with col4:
            leg_length = st.number_input("Leg Length (ft)", min_value=0.0, step=0.1)
        with col5:
            leg_width = st.number_input("Leg Width (ft)", min_value=0.0, step=0.1)

    if st.button("Calculate BOM"):
        try:
            if shape == "Rectangular":
                bom = calculate_bom(length, width, height, shape.lower(), waste_factor)
            else:
                bom = calculate_bom(length, width, height, shape.lower(), waste_factor, leg_length=leg_length, leg_width=leg_width)
            
            st.success("BOM Calculated!")
            st.json(bom)
            
            # Save project
            save_project(bom)
            st.info("Project saved to data/projects.json")
        except Exception as e:
            st.error(f"Error: {e}")
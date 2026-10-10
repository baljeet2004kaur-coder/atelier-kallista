import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="ATELIER KALLISTA",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Refined Editorial Theme with Crisp Contrast
st.markdown("""
<style>
    .stApp {
        background-color: #FAF9F6;
        color: #1A1715;
    }
    h1, h2, h3 {
        color: #1A1715 !important;
        font-family: 'Georgia', serif;
        letter-spacing: 0.04em;
    }
    section[data-testid="stSidebar"] {
        background-color: #F3EFEA !important;
        border-right: 1px solid #E5DFD5;
    }
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background-color: #FFFFFF !important;
        color: #1A1715 !important;
        border-radius: 6px !important;
    }
    .stButton>button {
        background-color: #1A1715 !important;
        color: #FAF9F6 !important;
        border-radius: 6px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
    }
    .stButton>button:hover {
        background-color: #B38F58 !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR: MEASUREMENTS & DIRECTIVES -----------------
with st.sidebar:
    st.markdown("### 🏛️ ATELIER KALLISTA")
    st.caption("Architectural Measurements & Design Directives")
    st.write("---")

    st.markdown("#### 1. Surface Geometry")
    wall_w = st.number_input("Wall Width (ft)", min_value=1.0, value=14.0, step=0.5)
    wall_h = st.number_input("Wall Height (ft)", min_value=1.0, value=10.0, step=0.5)
    
    deduct_openings = st.checkbox("Deduct Openings (Doors/Windows)", value=True)
    deduction_area = 0.0
    if deduct_openings:
        col_o1, col_o2 = st.columns(2)
        with col_o1:
            op_w = st.number_input("Opening W (ft)", min_value=0.0, value=3.0, step=0.5)
        with col_o2:
            op_h = st.number_input("Opening H (ft)", min_value=0.0, value=7.0, step=0.5)
        deduction_area = op_w * op_h

    net_wall_area = max(0.0, (wall_w * wall_h) - deduction_area)
    mat_rate = st.number_input("Cladding Rate (₹/sq.ft)", value=240.0, step=10.0)
    labor_rate = st.number_input("Installation Labor (₹/sq.ft)", value=65.0, step=5.0)

    st.markdown("#### 2. Cabinetry & Joinery")
    cab_w = st.number_input("Cabinet Width (ft)", min_value=1.0, value=8.5, step=0.5)
    cab_h = st.number_input("Cabinet Height (ft)", min_value=1.0, value=7.0, step=0.5)
    cab_d = st.number_input("Cabinet Depth (ft)", min_value=0.5, value=1.5, step=0.25)
    
    # Standard 8x4 sheet calculation (32 sq ft per sheet with 12% cutting waste)
    carcass_sqft = (2 * cab_w * cab_d) + (2 * cab_h * cab_d) + (cab_w * cab_h)
    sheets_est = max(1.0, round((carcass_sqft * 1.12) / 32.0, 1))

    board_rate = st.number_input("8×4 Board Price (₹)", value=2900.0, step=100.0)
    hardware_cost = st.number_input("Hardware Allowance (₹)", value=5500.0, step=500.0)
    joinery_labor = st.number_input("Joinery Labor (₹/sq.ft)", value=180.0, step=10.0)

    st.markdown("#### 3. AI Design Directives")
    room_type = st.selectbox("Interior Space", [
        "Living Room & TV Feature Wall", "Master Bedroom Suite", 
        "Contemporary Modular Kitchen", "Minimalist Pooja Room", "Foyer & Staircase"
    ])
    style_theme = st.selectbox("Aesthetic Style", [
        "Modern Punjabi Contemporary", "Warm Japandi Minimalist", 
        "Modern Indian Luxury", "Refined Organic Modern"
    ])
    materials = st.multiselect(
        "Materials & Textures",
        ["Natural Teak Wood", "Italian Bottochino Marble", "Charcoal Fluted Panels", "Brushed Brass Trims", "Fluted Reeded Glass"],
        default=["Natural Teak Wood", "Charcoal Fluted Panels", "Brushed Brass Trims"]
    )
    lighting_opt = st.selectbox("Lighting Profile", [
        "Concealed 3000K warm LED cove strips", "4000K neutral daylight profile tracks", "Moody directional accent sconces"
    ])
    design_notes = st.text_area("Specific Notes", value="Clean low-profile floating console, hidden wiring, fluted backdrop panel.")

    # Estimation Totals
    wall_total = net_wall_area * (mat_rate + labor_rate)
    cab_total = (sheets_est * board_rate) + (cab_w * cab_h * joinery_labor) + hardware_cost
    subtotal = wall_total + cab_total
    contingency = subtotal * 0.05
    gst = (subtotal + contingency) * 0.18
    grand_total = subtotal + contingency + gst

    st.write("---")
    st.markdown("### 📊 Live Cost Engine")
    st.metric("Net Cladding Area", f"{net_wall_area:.1f} sq.ft")
    st.metric("8×4 Sheets Needed", f"{sheets_est} sheets")
    st.metric("Estimated Grand Total", f"₹{grand_total:,.2f}")

# ----------------- MAIN STUDIO WORKSPACE -----------------
st.title("ATELIER KALLISTA")
st.caption("HAUTE INTERIOR ARCHITECTURE & ESTIMATION STUDIO")

# Synthesized Architectural Prompt
mat_str = ", ".join(materials) if materials else "Natural Teak, Polished Stone"
compiled_prompt = (
    f"Architectural interior photograph of an exquisite {style_theme} {room_type}. "
    f"Material palette: {mat_str}. "
    f"Lighting: {lighting_opt}. "
    f"{design_notes.strip()} "
    f"Shot on Hasselblad H6D-100c, 24mm tilt-shift lens, photorealistic 8k resolution, authentic material textures."
)

st.markdown("### 1. Synthesized AI Concept Prompt")
st.code(compiled_prompt, language="text")

st.markdown("### 2. Room Visualizer & Site Photo Uploader")
uploaded_file = st.file_uploader("Upload an existing site image to apply design changes", type=["jpg", "jpeg", "png"])

col_img1, col_img2 = st.columns(2)
with col_img1:
    st.markdown("**Site Reference**")
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption="Uploaded Site Photo", use_container_width=True)
    else:
        st.info("Upload an image to inspect your site baseline.")

with col_img2:
    st.markdown("**Concept Render Preview**")
    st.image(
        "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=1200&q=80",
        caption=f"Atelier Kallista — Render Concept for {room_type}",
        use_container_width=True
    )
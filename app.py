import streamlit as st
from PIL import Image
import urllib.parse
import time
import random

# 1. Compact Page Setup & Editorial Layout
st.set_page_config(
    page_title="ATELIER KALLISTA",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Robust, high-contrast style injection with compact sizing
st.markdown("""
<style>
    html, body, [class*="css"], .stMarkdown, p, span, label, h1, h2, h3, h4, h5, h6 {
        color: #111111 !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .stApp { background-color: #FAF8F5 !important; }
    section[data-testid="stSidebar"] {
        background-color: #F3ECE2 !important;
        border-right: 1px solid #DFD5C7;
    }
    input, select, textarea, div[data-baseweb="select"], div[data-baseweb="input"] {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border: 1px solid #C8BEB0 !important;
        border-radius: 6px !important;
    }
    .prompt-box {
        background-color: #FFFFFF;
        border: 1px solid #D5C9B8;
        border-radius: 6px;
        padding: 10px;
        font-family: monospace;
        font-size: 0.82rem;
        color: #111111;
    }
    .stButton>button {
        background-color: #8C6D46 !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
        font-weight: 700 !important;
        padding: 8px 16px !important;
        border: none !important;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR: MEASUREMENTS & SPECIFICATIONS -----------------
with st.sidebar:
    st.markdown("## 🏛️ ATELIER KALLISTA")
    st.caption("Contemporary Architecture & Cost Engine")
    st.markdown("---")

    with st.expander("📐 1. Geometry", expanded=True):
        wall_w = st.number_input("Wall Width (ft)", min_value=1.0, value=14.0, step=0.5)
        wall_h = st.number_input("Wall Height (ft)", min_value=1.0, value=10.0, step=0.5)
        deduct_openings = st.checkbox("Deduct Openings", value=True)
        deduction_sqft = 0.0
        if deduct_openings:
            c1, c2 = st.columns(2)
            with c1: op_w = st.number_input("Opening W (ft)", min_value=0.0, value=3.0, step=0.5)
            with c2: op_h = st.number_input("Opening H (ft)", min_value=0.0, value=7.0, step=0.5)
            deduction_sqft = op_w * op_h
        net_wall_sqft = max(0.0, (wall_w * wall_h) - deduction_sqft)

    with st.expander("🪵 2. Board Rates & Joinery", expanded=True):
        mat_rate = st.number_input("Material Cladding (₹/sq.ft)", value=320.0, step=10.0)
        labor_rate = st.number_input("Labor (₹/sq.ft)", value=75.0, step=5.0)
        cab_w = st.number_input("Cabinet W (ft)", min_value=1.0, value=9.0, step=0.5)
        cab_h = st.number_input("Cabinet H (ft)", min_value=1.0, value=7.5, step=0.5)
        cab_d = st.number_input("Cabinet D (ft)", min_value=0.5, value=1.5, step=0.25)
        
        carcass_sqft = (2 * cab_w * cab_d) + (2 * cab_h * cab_d) + (cab_w * cab_h)
        sheets_count = max(1.0, round((carcass_sqft * 1.12) / 32.0, 1))
        sheet_rate = st.number_input("8×4 Sheet (₹)", value=3200.0, step=100.0)
        hardware_cost = st.number_input("Hardware (₹)", value=6500.0, step=500.0)
        cab_labor = st.number_input("Labor (₹/sq.ft)", value=190.0, step=10.0)

    with st.expander("🎨 3. Design Directives", expanded=True):
        room_space = st.selectbox("Target Space", [
            "Luxury Walk-in Dressing Wardrobe", "Double-Height Staircase & Foyer Gallery",
            "Grand Living Room & TV Wall", "Master Bedroom & Headboard Suite",
            "Contemporary Modular Kitchen", "Pooja Room with Backlit CNC Jali"
        ])
        design_style = st.selectbox("Aesthetic", [
            "Ultra-Modern Luxury Staging", "Modern Punjabi Royal Luxury",
            "Contemporary Indian Fusion", "Warm Japandi Minimalist"
        ])
        wood_selection = st.multiselect(
            "Wood Substrates",
            ["Natural Teak Wood", "Action TESA HDHMR", "Century BWP Plywood", "American Dark Walnut Veneer", "White Oak Grain"],
            default=["Action TESA HDHMR", "American Dark Walnut Veneer"]
        )
        accents = st.multiselect(
            "Luxury Accents",
            ["Curved Edge Panel casework", "Fluted Slat Panels", "Gold PVD Brass Trim Inlays", "CNC Backlit Jali", "Glass Doors", "High-End Satin PU Finish"],
            default=["Curved Edge Panel casework", "Gold PVD Brass Trim Inlays", "High-End Satin PU Finish"]
        )
        color_palette = st.selectbox("Palettes", [
            "Lumiere Matte Off-White, Cashmere Ivory & Gold Brass",
            "Burnt Ochre, Warm Teak & Brushed Gold",
            "Royal Emerald, Warm Oak & Champagne Brass"
        ])
        lighting = st.selectbox("Ceiling & Lighting", [
            "Curved Display Backlighting, Soft 3000K LEDs & Shadow Cove Highlights",
            "Modern Magnetic Linear Tracks with Ambient Pendant & Floor Washers"
        ])
        special_notes = st.text_area("Custom Staging Info", value="Curved glass/display shelving, illuminated open tiers, vertical fluted paneling, matte lacquer finishes, zero visual clutter.")

    # Estimation Calculations
    wall_sub = net_wall_sqft * (mat_rate + labor_rate)
    cab_sub = (sheets_count * sheet_rate) + (cab_w * cab_h * cab_labor) + hardware_cost
    subtotal = wall_sub + cab_sub
    contingency = subtotal * 0.05
    gst = (subtotal + contingency) * 0.18
    grand_total = subtotal + contingency + gst

    st.markdown("---")
    st.markdown("### 📊 Project Cost Summary")
    st.metric("Area Size", f"{net_wall_sqft:.1f} sq.ft")
    st.metric("8×4 Sheets Needed", f"{sheets_count} sheets")
    st.metric("Grand Total (inc. GST)", f"₹{grand_total:,.2f}")

# ----------------- MAIN STUDIO WORKSPACE -----------------
st.title("ATELIER KALLISTA")
st.caption("HAUTE INTERIOR ARCHITECTURE & ESTIMATION STUDIO")
st.markdown("---")

# Dynamic architectural prompt compiler rejecting traditional/dated layouts
woods_str = ", ".join(wood_selection) if wood_selection else "Warm Oak"
accents_str = ", ".join(accents) if accents else "Brass and Lacquer"
compiled_prompt = (
    f"Luxurious architectural photography of an exquisite {design_style} {room_space}. "
    f"Reject dated, flat brown wood design. Implement a ultra-modern, elite staging aesthetic. "
    f"Material specification: {woods_str}, {accents_str}. "
    f"Color Palette: {color_palette}. "
    f"Lighting: {lighting}. "
    f"Fitted Features: {special_notes.strip()} "
    f"Captured on Hasselblad H6D-100c, 24mm tilt-shift lens, soft volumetric daylight, authentic high-contrast reflections, 8k resolution, contemporary layout."
)

col_prompt, col_uploader = st.columns([1.5, 1], gap="medium")
with col_prompt:
    st.markdown("**1. Synthesized Prompt**")
    st.markdown(f'<div class="prompt-box">{compiled_prompt}</div>', unsafe_allow_html=True)
with col_uploader:
    st.markdown("**2. Reference Photo**")
    uploaded_file = st.file_uploader("Upload existing site photo (.jpg, .png)", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

st.markdown("---")
st.markdown("### 3. Studio Visualizer & Live Generative Studio")

col_left, col_right = st.columns([1, 1], gap="medium")

with col_left:
    if uploaded_file is not None:
        user_img = Image.open(uploaded_file)
        st.image(user_img, caption="Original Room Photo Reference", use_container_width=True)
    else:
        st.info("Drag and drop your space reference photo on the top right to compare site geometry.")

with col_right:
    # Live generative update
    render_button = st.button("✨ GENERATE NEW ARCHITECTURAL RENDER")
    
    if "render_seed" not in st.session_state:
        st.session_state.render_seed = random.randint(1000, 999999)
        
    if render_button:
        st.session_state.render_seed = random.randint(1000, 999999)
        with st.spinner("Synthesizing contemporary textures..."):
            time.sleep(1.0)
            st.success(f"New modern concept render loaded!")

    # Live generation endpoint using modern style inject tags
    contemporary_sceneries = "high-end architectural, modern, elite luxury, curved and rounded casing, textured off-white and warm ivory PU satin lacquer, vertical fluted details, long vertical brass/champagne gold hardware, curved open shelves, illuminated 3000K warm LED strips"
    clean_prompt = f"beautiful luxury interior indoor {design_style} {room_space}, {contemporary_sceneries}, {color_palette}, {accents_str}, {woods_str}, no old-fashioned, realistic 8k photograph, cinematic lighting"
    encoded_prompt = urllib.parse.quote(clean_prompt)
    
    dynamic_ai_image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=800&seed={st.session_state.render_seed}&nologo=true"
    
    st.image(
        dynamic_ai_image_url,
        caption=f"Atelier Kallista Concept Render (Seed: {st.session_state.render_seed})",
        use_container_width=True
    )

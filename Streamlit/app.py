import streamlit as st
import requests
from PIL import Image
import io

st.set_page_config(
    page_title="ðŸŒ¿ PlantGuard AI",
    page_icon="ðŸŒ¿",
    layout="wide"
)

FLASK_URL = "http://127.0.0.1:5000/predict"

if "lang" not in st.session_state:
    st.session_state.lang = "en"

ui = {
    "en": {
        "title": "ðŸŒ¿ PlantGuard AI",
        "subtitle": "Upload or capture a leaf photo â€” AI will diagnose instantly",
        "nav": ["ðŸ” Detect Disease", "ðŸ—ï¸ Model Architecture", "ðŸ“Š About"],
        "upload_tab": "ðŸ“ Upload Image",
        "camera_tab": "ðŸ“· Take Photo",
        "upload_hint": "âœ… Image loaded â€” click Detect below",
        "camera_hint": "âœ… Photo captured â€” click Detect below",
        "your_image": "ðŸ–¼ï¸ Your Image",
        "analysis": "ðŸ” Analysis",
        "detect_btn": "ðŸŒ¿ Detect Disease",
        "analyzing": "Analyzing leaf...",
        "detected": "DETECTED",
        "confidence": "Confidence",
        "description": "ðŸ“‹ About this Disease",
        "treatment": "ðŸ’Š Treatment",
        "prevention": "ðŸ›¡ï¸ Prevention",
        "warning_label": "âš ï¸ Warning",
        "top3": "ðŸ“Š Top 3 Predictions",
        "click_to_detect": "Click Detect Disease to analyze",
        "severity": "Severity",
        "healthy_msg": "ðŸŽ‰ Great news! Your plant is healthy!",
        "lang_label": "ðŸŒ Language",
        "drop_hint": "Drop your leaf image here",
        "flask_online": "âœ… Flask API is Online",
        "flask_offline": "âŒ Flask API is Offline â€” run: python app.py",
    },
    "hi": {
        "title": "ðŸŒ¿ PlantGuard AI",
        "subtitle": "Patte ki photo upload karein ya kheenchen â€” AI turant pehchan karega",
        "nav": ["ðŸ” Bimari Pehchano", "ðŸ—ï¸ Model Architecture", "ðŸ“Š Baare Mein"],
        "upload_tab": "ðŸ“ Photo Upload Karein",
        "camera_tab": "ðŸ“· Photo Kheenchen",
        "upload_hint": "âœ… Photo load ho gayi â€” Neeche detect dabayein",
        "camera_hint": "âœ… Photo li gayi â€” Neeche detect dabayein",
        "your_image": "ðŸ–¼ï¸ Aapki Photo",
        "analysis": "ðŸ” Jaanch",
        "detect_btn": "ðŸŒ¿ Bimari Pehchano",
        "analyzing": "Patte ki jaanch ho rahi hai...",
        "detected": "PEHCHAANA GAYA",
        "confidence": "Vishwasniyata",
        "description": "ðŸ“‹ Is Bimari Ke Baare Mein",
        "treatment": "ðŸ’Š Ilaj",
        "prevention": "ðŸ›¡ï¸ Bachaav",
        "warning_label": "âš ï¸ Chetaavni",
        "top3": "ðŸ“Š Top 3 Anumaan",
        "click_to_detect": "Bimari Pehchanne ke liye Detect dabayein",
        "severity": "Gambhirata",
        "healthy_msg": "ðŸŽ‰ Badhaai! Aapka podha bilkul swasth hai!",
        "lang_label": "ðŸŒ Bhaasha",
        "drop_hint": "Yahan patte ki photo daalein",
        "flask_online": "âœ… Flask API chal rahi hai",
        "flask_offline": "âŒ Flask API band hai â€” chalayein: python app.py",
    }
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Tiro+Devanagari+Hindi&display=swap');

.stApp {
    background: #0a1628;
    background-image: radial-gradient(ellipse at 20% 50%, rgba(16,86,46,0.3) 0%, transparent 60%),
                      radial-gradient(ellipse at 80% 20%, rgba(5,46,22,0.4) 0%, transparent 50%);
    font-family: 'Nunito', sans-serif;
}

[data-testid="stSidebar"] {
    background: rgba(5, 20, 12, 0.97) !important;
    border-right: 1px solid rgba(74,222,128,0.15);
}

.main-title {
    font-family: 'Nunito', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #4ade80 0%, #86efac 50%, #bbf7d0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    letter-spacing: -0.5px;
}

.sub-title {
    text-align: center;
    color: #6ee7a0;
    font-size: 1rem;
    opacity: 0.85;
    margin-bottom: 1.5rem;
    font-weight: 400;
}

.result-card {
    background: linear-gradient(135deg, rgba(20,40,28,0.9), rgba(10,25,18,0.95));
    border: 1px solid rgba(74,222,128,0.2);
    border-radius: 20px;
    padding: 1.5rem;
    margin: 0.8rem 0;
}

.sev-none    { background:#064e3b; color:#6ee7b7; padding:0.3rem 0.9rem; border-radius:999px; font-size:0.8rem; font-weight:700; display:inline-block; }
.sev-moderate{ background:#78350f; color:#fde68a; padding:0.3rem 0.9rem; border-radius:999px; font-size:0.8rem; font-weight:700; display:inline-block; }
.sev-severe  { background:#7f1d1d; color:#fecaca; padding:0.3rem 0.9rem; border-radius:999px; font-size:0.8rem; font-weight:700; display:inline-block; }

.healthy-badge {
    background: linear-gradient(135deg, #065f46, #047857);
    color: #d1fae5;
    padding: 0.6rem 1.4rem;
    border-radius: 999px;
    font-size: 1.05rem;
    font-weight: 700;
    display: inline-block;
    margin: 0.4rem 0;
    letter-spacing: 0.3px;
}
.disease-badge {
    background: linear-gradient(135deg, #7f1d1d, #991b1b);
    color: #fee2e2;
    padding: 0.6rem 1.4rem;
    border-radius: 999px;
    font-size: 1.05rem;
    font-weight: 700;
    display: inline-block;
    margin: 0.4rem 0;
}

.info-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(74,222,128,0.15);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
}
.info-box-label {
    color: #4ade80;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.info-box-text {
    color: #cbd5e1;
    font-size: 0.9rem;
    line-height: 1.65;
}

.treatment-box {
    background: rgba(251,191,36,0.07);
    border: 1px solid rgba(251,191,36,0.25);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
}
.prevention-box {
    background: rgba(59,130,246,0.07);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
}
.warning-box {
    background: rgba(239,68,68,0.08);
    border: 1px solid rgba(239,68,68,0.3);
    border-left: 4px solid #ef4444;
    border-radius: 0 14px 14px 0;
    padding: 0.8rem 1.2rem;
    margin: 0.6rem 0;
}

.arch-layer {
    background: rgba(74,222,128,0.05);
    border: 1px solid rgba(74,222,128,0.2);
    border-left: 3px solid #4ade80;
    border-radius: 0 12px 12px 0;
    padding: 0.8rem 1.2rem;
    margin: 0.4rem 0;
}
.arch-layer h4 { color: #4ade80; margin: 0 0 0.2rem 0; font-size: 0.95rem; }
.arch-layer p  { margin: 0; font-size: 0.82rem; color: #94a3b8; }

.metric-box {
    background: rgba(74,222,128,0.06);
    border: 1px solid rgba(74,222,128,0.18);
    border-radius: 14px;
    padding: 1.2rem 1rem;
    text-align: center;
}
.metric-value { font-size: 2rem; font-weight: 800; color: #4ade80; }
.metric-label { font-size: 0.78rem; color: #86efac; opacity: 0.7; margin-top: 0.2rem; }

.stButton > button {
    background: linear-gradient(135deg, #16a34a, #15803d) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.65rem 2rem !important;
    letter-spacing: 0.3px !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #15803d, #166534) !important;
    box-shadow: 0 4px 24px rgba(74,222,128,0.25) !important;
}

.stTabs [data-baseweb="tab"] { color: #86efac !important; font-weight: 600 !important; }
.stTabs [aria-selected="true"] { color: #4ade80 !important; border-bottom-color: #4ade80 !important; }

.stProgress > div > div { background: linear-gradient(90deg, #4ade80, #22c55e) !important; }

p, li, label { color: #cbd5e1 !important; }
h1, h2, h3, h4 { color: #bbf7d0 !important; }
hr { border-color: rgba(74,222,128,0.12) !important; }

.upload-hint { text-align:center; color:#6ee7a0; font-size:0.88rem; margin-top:0.5rem; }

.empty-state { text-align:center; padding:3rem 1rem; color:#4ade80; opacity:0.4; }
</style>
""", unsafe_allow_html=True)

L = ui[st.session_state.lang]

with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; padding:1.2rem 0 0.5rem;'>
        <div style='font-size:2.8rem;'>ðŸŒ¿</div>
        <div style='font-size:1.25rem; color:#4ade80; font-weight:800; letter-spacing:-0.3px;'>PlantGuard AI</div>
        <div style='font-size:0.72rem; color:#6ee7a0; opacity:0.6; margin-top:2px;'>Powered by TensorFlow</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(f"<div style='color:#86efac; font-size:0.82rem; font-weight:700; margin-bottom:6px;'>{L['lang_label']}</div>", unsafe_allow_html=True)
    col_en, col_hi = st.columns(2)
    with col_en:
        if st.button("ðŸ‡¬ðŸ‡§ English", use_container_width=True,
                     type="primary" if st.session_state.lang == "en" else "secondary"):
            st.session_state.lang = "en"
            st.rerun()
    with col_hi:
        if st.button("ðŸ‡®ðŸ‡³ à¤¹à¤¿à¤‚à¤¦à¥€", use_container_width=True,
                     type="primary" if st.session_state.lang == "hi" else "secondary"):
            st.session_state.lang = "hi"
            st.rerun()

    st.divider()

    L = ui[st.session_state.lang]
    page = st.radio("Nav", L["nav"], label_visibility="collapsed")

    st.divider()
    st.markdown("""
    <div style='font-size:0.72rem; color:#6ee7a0; opacity:0.5; text-align:center; line-height:1.8;'>
        Tomato Â· Potato Â· Pepper<br>15 classes Â· ~96% accuracy
    </div>
    """, unsafe_allow_html=True)

L = ui[st.session_state.lang]

if L["nav"][0] in page:

    st.markdown(f'<div class="main-title">{L["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-title">{L["subtitle"]}</div>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs([L["upload_tab"], L["camera_tab"]])
    image_data = None

    with tab1:
        uploaded = st.file_uploader(L["drop_hint"], type=["jpg","jpeg","png"], label_visibility="collapsed")
        if uploaded:
            image_data = uploaded.read()
            st.markdown(f'<div class="upload-hint">{L["upload_hint"]}</div>', unsafe_allow_html=True)

    with tab2:
        camera_photo = st.camera_input(" ")
        if camera_photo:
            image_data = camera_photo.read()
            st.markdown(f'<div class="upload-hint">{L["camera_hint"]}</div>', unsafe_allow_html=True)

    st.divider()

    if image_data:
        col_img, col_result = st.columns([1, 1], gap="large")

        with col_img:
            st.markdown(f"#### {L['your_image']}")
            st.image(Image.open(io.BytesIO(image_data)), use_container_width=True)

        with col_result:
            st.markdown(f"#### {L['analysis']}")
            if st.button(L["detect_btn"], use_container_width=True):
                with st.spinner(L["analyzing"]):
                    try:
                        response = requests.post(
                            FLASK_URL,
                            files={"file": ("image.jpg", image_data, "image/jpeg")},
                            timeout=30
                        )

                        if response.status_code == 200:
                            result     = response.json()
                            pred_class = result["predicted_class"]
                            confidence = result["confidence"]
                            severity   = result["severity"]
                            lang_info  = result.get(st.session_state.lang, result.get("en", {}))
                            top3       = result["top3"]

                            is_healthy   = "healthy" in pred_class.lower()
                            badge_class  = "healthy-badge" if is_healthy else "disease-badge"
                            icon         = "âœ…" if is_healthy else "âš ï¸"
                            display_name = pred_class.replace("_", " ").replace("  ", " ")

                            sev_class = {"None": "sev-none", "Moderate": "sev-moderate", "Severe": "sev-severe"}.get(severity, "sev-moderate")
                            sev_label = {"None": "âœ… Healthy", "Moderate": "âš¡ Moderate", "Severe": "ðŸ”´ Severe"}.get(severity, severity)

                            st.markdown(f"""
                            <div class="result-card">
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
                                    <span style="font-size:0.78rem; color:#6ee7a0; letter-spacing:1px; font-weight:700;">{L['detected']}</span>
                                    <span class="{sev_class}">{sev_label}</span>
                                </div>
                                <div class="{badge_class}">{icon} {display_name}</div>
                                <div style="margin-top:1rem; color:#94a3b8; font-size:0.85rem; font-weight:600;">{L['confidence']}</div>
                            </div>
                            """, unsafe_allow_html=True)

                            st.progress(confidence / 100)
                            st.markdown(f"<div style='text-align:right; color:#4ade80; font-weight:700; margin-top:-0.3rem;'>{confidence:.1f}%</div>", unsafe_allow_html=True)

                            if is_healthy:
                                st.markdown(f"<div style='text-align:center; color:#4ade80; font-size:1.1rem; font-weight:700; padding:0.5rem;'>{L['healthy_msg']}</div>", unsafe_allow_html=True)

                            if lang_info.get("description"):
                                st.markdown(f"""
                                <div class="info-box">
                                    <div class="info-box-label">{L['description']}</div>
                                    <div class="info-box-text">{lang_info['description']}</div>
                                </div>
                                """, unsafe_allow_html=True)

                            if lang_info.get("treatment"):
                                st.markdown(f"""
                                <div class="treatment-box">
                                    <div class="info-box-label" style="color:#fbbf24;">{L['treatment']}</div>
                                    <div class="info-box-text">{lang_info['treatment']}</div>
                                </div>
                                """, unsafe_allow_html=True)

                            if lang_info.get("prevention"):
                                st.markdown(f"""
                                <div class="prevention-box">
                                    <div class="info-box-label" style="color:#60a5fa;">{L['prevention']}</div>
                                    <div class="info-box-text">{lang_info['prevention']}</div>
                                </div>
                                """, unsafe_allow_html=True)

                            if lang_info.get("warning"):
                                st.markdown(f"""
                                <div class="warning-box">
                                    <div class="info-box-label" style="color:#f87171;">{L['warning_label']}</div>
                                    <div class="info-box-text" style="color:#fca5a5;">{lang_info['warning']}</div>
                                </div>
                                """, unsafe_allow_html=True)

                            st.markdown(f"<div style='color:#86efac; font-weight:700; font-size:0.9rem; margin-top:1rem;'>{L['top3']}</div>", unsafe_allow_html=True)
                            for i, item in enumerate(top3):
                                name = item["class"].replace("_", " ")
                                conf = item["confidence"]
                                st.markdown(f"<div style='color:#94a3b8; font-size:0.82rem; margin-top:0.5rem;'>{i+1}. {name}</div>", unsafe_allow_html=True)
                                st.progress(conf / 100)
                                st.markdown(f"<div style='text-align:right; color:#4ade80; font-size:0.8rem; margin-top:-0.4rem;'>{conf:.1f}%</div>", unsafe_allow_html=True)

                        else:
                            st.error(f"API Error: {response.json().get('error')}")

                    except requests.exceptions.ConnectionError:
                        st.error("âŒ Cannot connect to Flask API. Make sure Flask is running on port 5000!")
                    except Exception as e:
                        st.error(f"Error: {e}")

            else:
                st.markdown(f"""
                <div class="empty-state">
                    <div style='font-size:2.5rem; margin-bottom:0.5rem;'>ðŸ”¬</div>
                    <div style='font-size:0.9rem;'>{L['click_to_detect']}</div>
                </div>
                """, unsafe_allow_html=True)

elif L["nav"][1] in page:

    st.markdown('<div class="main-title">ðŸ—ï¸ Model Architecture</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">How the CNN works under the hood</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl in zip([c1,c2,c3,c4],
                              ["4", "458K", "128Â²", "15"],
                              ["Conv Blocks", "Parameters", "Input Size", "Classes"]):
        col.markdown(f'<div class="metric-box"><div class="metric-value">{val}</div><div class="metric-label">{lbl}</div></div>', unsafe_allow_html=True)

    st.divider()
    col_arch, col_info = st.columns([1, 1], gap="large")

    with col_arch:
        st.markdown("#### ðŸ”¢ Layer Stack")
        layers = [
            ("ðŸ“¥ Input", "Shape: (128, 128, 3) â€” RGB image"),
            ("âš–ï¸ Rescaling", "Normalizes pixels 0â€“255 â†’ 0â€“1 (built into model)"),
            ("ðŸ”µ Conv2D â€” 32 filters", "3Ã—3 kernel Â· ReLU Â· Same padding"),
            ("â¬‡ï¸ MaxPooling2D", "2Ã—2 â†’ 64Ã—64"),
            ("ðŸ”µ Conv2D â€” 64 filters", "3Ã—3 kernel Â· ReLU Â· Same padding"),
            ("â¬‡ï¸ MaxPooling2D", "2Ã—2 â†’ 32Ã—32"),
            ("ðŸ”µ Conv2D â€” 128 filters", "3Ã—3 kernel Â· ReLU Â· Same padding"),
            ("â¬‡ï¸ MaxPooling2D", "2Ã—2 â†’ 16Ã—16"),
            ("ðŸ”µ Conv2D â€” 256 filters", "3Ã—3 kernel Â· ReLU Â· Same padding"),
            ("â¬‡ï¸ MaxPooling2D", "2Ã—2 â†’ 8Ã—8"),
            ("ðŸŒ GlobalAveragePooling2D", "8Ã—8Ã—256 â†’ 256 vector"),
            ("ðŸŸ¡ Dense â€” 256", "Fully connected Â· ReLU"),
            ("ðŸ’§ Dropout â€” 0.3", "Prevents overfitting"),
            ("ðŸ“¤ Dense â€” 15 + Softmax", "15 class probabilities"),
        ]
        for name, desc in layers:
            st.markdown(f'<div class="arch-layer"><h4>{name}</h4><p>{desc}</p></div>', unsafe_allow_html=True)

    with col_info:
        st.markdown("#### ðŸŽ“ Training Details")
        details = {
            "Optimizer": "RMSprop (lr = 0.0005)",
            "Loss Function": "Sparse Categorical Crossentropy",
            "Epochs": "50 (EarlyStopping patience=5)",
            "Batch Size": "32",
            "Split": "70% Train / 15% Val / 15% Test",
            "Dataset": "PlantVillage (20,063 images)",
            "Image Size": "128 Ã— 128 pixels",
            "Normalization": "Built-in Rescaling (Ã·255)",
            "Regularization": "Dropout 0.3",
        }
        for k, v in details.items():
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; padding:0.55rem 0;
                        border-bottom:1px solid rgba(74,222,128,0.08);'>
                <span style='color:#6ee7a0; font-size:0.87rem;'>{k}</span>
                <span style='color:#4ade80; font-weight:700; font-size:0.87rem;'>{v}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### ðŸ“ˆ Results")
        for label, val, color in [
            ("Train Accuracy", "96.3%", "#4ade80"),
            ("Validation Accuracy", "97.3%", "#4ade80"),
            ("Test Accuracy", "96.2%", "#4ade80"),
            ("Test Loss", "0.131", "#fbbf24"),
        ]:
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; padding:0.55rem 0;
                        border-bottom:1px solid rgba(74,222,128,0.08);'>
                <span style='color:#6ee7a0; font-size:0.87rem;'>{label}</span>
                <span style='color:{color}; font-weight:800; font-size:1rem;'>{val}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### ðŸŒ¿ Supported Classes")
        for c in ["Pepper â€” Bacterial Spot","Pepper â€” Healthy","Potato â€” Early Blight",
                   "Potato â€” Late Blight","Potato â€” Healthy","Tomato â€” Bacterial Spot",
                   "Tomato â€” Early Blight","Tomato â€” Late Blight","Tomato â€” Leaf Mold",
                   "Tomato â€” Septoria Leaf Spot","Tomato â€” Spider Mites",
                   "Tomato â€” Target Spot","Tomato â€” Yellow Leaf Curl Virus",
                   "Tomato â€” Mosaic Virus","Tomato â€” Healthy"]:
            icon = "âœ…" if "Healthy" in c else "ðŸ”´"
            st.markdown(f"<div style='color:#94a3b8; font-size:0.83rem; padding:0.18rem 0;'>{icon} {c}</div>", unsafe_allow_html=True)

elif L["nav"][2] in page:

    st.markdown('<div class="main-title">ðŸ“Š About PlantGuard AI</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("#### ðŸŒ± About")
        st.markdown("""
        <div class="info-box">
            <div class="info-box-text">
                PlantGuard AI is a deep learning-powered plant disease detection system
                trained on the <strong style='color:#4ade80;'>PlantVillage dataset</strong>
                (20,000+ leaf images). It uses a custom
                <strong style='color:#4ade80;'>Convolutional Neural Network (CNN)</strong>
                to detect 15 disease categories across Tomato, Potato, and Bell Pepper
                with ~96% accuracy â€” helping farmers act faster and reduce crop loss.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### ðŸš€ How to Use")
        for num, en_step, hi_step in [
            ("1", "Go to Detect Disease page", "Bimari Pehchano page par jayein"),
            ("2", "Upload leaf photo or use camera", "Patte ki photo upload karein ya camera se lein"),
            ("3", "Click Detect Disease", "Detect button dabayein"),
            ("4", "Get diagnosis + treatment advice", "Diagnosis aur ilaj ki salaah milegi"),
        ]:
            step = hi_step if st.session_state.lang == "hi" else en_step
            st.markdown(f"""
            <div style='display:flex; align-items:center; gap:0.8rem; padding:0.5rem 0;
                        border-bottom:1px solid rgba(74,222,128,0.08);'>
                <div style='background:#4ade80; color:#0a1628; border-radius:50%;
                            width:26px; height:26px; display:flex; align-items:center;
                            justify-content:center; font-weight:800; font-size:0.85rem; flex-shrink:0;'>{num}</div>
                <div style='color:#cbd5e1; font-size:0.9rem;'>{step}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### âš¡ Tech Stack")
        for icon, name, desc in [
            ("ðŸ§ ", "TensorFlow / Keras", "Deep learning model"),
            ("ðŸŒ¶ï¸", "Flask", "Backend REST API"),
            ("ðŸŽ¨", "Streamlit", "Frontend UI"),
            ("ðŸ‘ï¸", "OpenCV", "Image preprocessing"),
            ("ðŸ”¥", "Grad-CAM", "Visual explainability"),
            ("ðŸ“¦", "PlantVillage", "Training dataset (20K images)"),
        ]:
            st.markdown(f"""
            <div style='display:flex; align-items:center; gap:0.8rem; padding:0.65rem;
                        background:rgba(74,222,128,0.04); border:1px solid rgba(74,222,128,0.12);
                        border-radius:12px; margin:0.25rem 0;'>
                <div style='font-size:1.4rem;'>{icon}</div>
                <div>
                    <div style='color:#4ade80; font-weight:700; font-size:0.9rem;'>{name}</div>
                    <div style='color:#6ee7a0; font-size:0.78rem; opacity:0.7;'>{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### ðŸ”— API Status")
        try:
            r = requests.get("http://127.0.0.1:5000/", timeout=3)
            if r.status_code == 200:
                st.markdown(f"""
                <div style='background:rgba(74,222,128,0.08); border:1px solid rgba(74,222,128,0.4);
                            border-radius:12px; padding:0.8rem 1rem; color:#4ade80; font-weight:700;'>
                    {L['flask_online']} â€” http://127.0.0.1:5000
                </div>
                """, unsafe_allow_html=True)
        except:
            st.markdown(f"""
            <div style='background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.4);
                        border-radius:12px; padding:0.8rem 1rem; color:#ef4444; font-weight:700;'>
                {L['flask_offline']}
            </div>
            """, unsafe_allow_html=True)

st.divider()
st.markdown("""
<div style='text-align:center; color:#4ade80; opacity:0.3; font-size:0.73rem; letter-spacing:0.5px;'>
    PlantGuard AI Â· TensorFlow + Flask + Streamlit Â· ~96% Accuracy
</div>
""", unsafe_allow_html=True)


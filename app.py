from pathlib import Path
import streamlit as st
import random

st.set_page_config(
    page_title="Birthday Fab 28th",
    page_icon="🎂",
    layout="centered"
)

# Custom CSS: Comic Sans Font, Gradien Lembut, Arcade Vibe (Tanpa Hint)
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top left, #E0F2FE 0%, #F8FAFC 50%, #FEF9C3 100%);
        font-family: 'Comic Sans MS', 'Comic Sans', cursive, sans-serif;
        color: #1E293B;
    }

    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 540px !important;
    }

    .audio-pill {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(6px);
        border: 1.5px solid #BAE6FD;
        border-radius: 50px;
        padding: 6px 14px;
        margin: 0 auto 14px auto;
        max-width: 320px;
        box-shadow: 0 4px 12px rgba(2, 132, 199, 0.08);
        text-align: center;
    }
    .audio-pill-label {
        font-size: 11.5px;
        font-weight: 700;
        color: #0369A1;
        margin-bottom: 3px;
        font-family: 'Comic Sans MS', 'Comic Sans', cursive, sans-serif;
    }
    audio {
        width: 100%;
        height: 28px;
    }

    .hero-card {
        text-align: center;
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(8px);
        border: 2px solid #BAE6FD;
        border-radius: 24px;
        padding: 18px 16px;
        box-shadow: 0 8px 24px rgba(14, 116, 144, 0.08);
        margin-bottom: 16px;
    }

    .main-title {
        font-family: 'Comic Sans MS', 'Comic Sans', cursive, sans-serif;
        color: #0F172A;
        font-size: 28px;
        font-weight: 700;
        margin: 0;
        line-height: 1.15;
    }

    .subtitle {
        display: inline-block;
        background-color: #FEF08A;
        color: #854D0E;
        border: 1.5px solid #FACC15;
        padding: 5px 16px;
        border-radius: 50px;
        font-size: 14px;
        font-weight: 800;
        margin-top: 8px;
        transform: rotate(-1deg);
        box-shadow: 0 3px 8px rgba(234, 179, 8, 0.18);
        font-family: 'Comic Sans MS', 'Comic Sans', cursive, sans-serif;
    }

    @keyframes wiggle {
        0%, 100% { transform: rotate(-2deg) translateY(0px); }
        50% { transform: rotate(2deg) translateY(-4px); }
    }

    .koala-wrap {
        background: #FFFFFF;
        padding: 8px;
        border-radius: 22px;
        border: 2px solid #E2E8F0;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.07);
        animation: wiggle 3.5s ease-in-out infinite;
        max-width: 160px;
        margin: 0 auto;
    }
    .koala-wrap img {
        border-radius: 16px;
    }

    .game-box {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(6px);
        border: 2px solid #BAE6FD;
        border-radius: 22px;
        padding: 18px;
        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.07);
        margin-bottom: 14px;
        text-align: center;
    }

    .score-banner {
        display: flex;
        justify-content: space-between;
        background: #F0F9FF;
        padding: 8px 14px;
        border-radius: 14px;
        margin-bottom: 12px;
        font-weight: 700;
        font-size: 13px;
        color: #0369A1;
        border: 1px solid #BAE6FD;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #0284C7 0%, #0369A1 100%);
        color: #FFFFFF !important;
        border: none;
        border-radius: 50px;
        font-family: 'Comic Sans MS', 'Comic Sans', cursive, sans-serif;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 0.3px;
        min-height: 44px;
        box-shadow: 0 6px 16px rgba(2, 132, 199, 0.28);
        transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #0369A1 0%, #075985 100%);
        transform: scale(1.02) translateY(-2px);
        box-shadow: 0 8px 20px rgba(2, 132, 199, 0.35);
    }

    div[data-testid="stDialog"] div[role="dialog"] {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border-radius: 26px !important;
        border: 3px solid #7DD3FC !important;
        font-family: 'Comic Sans MS', 'Comic Sans', cursive, sans-serif !important;
    }
    div[data-testid="stDialog"] div[role="dialog"] * {
        color: #1E293B;
        font-family: 'Comic Sans MS', 'Comic Sans', cursive, sans-serif !important;
    }

    .footer-sign {
        text-align: center;
        color: #64748B;
        font-size: 12px;
        font-weight: 700;
        margin-top: 22px;
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "game_state" not in st.session_state:
    st.session_state.game_state = "arcade_1"
if "arcade_score" not in st.session_state:
    st.session_state.arcade_score = 0
if "clicked_items" not in st.session_state:
    st.session_state.clicked_items = []
if "quick_taps" not in st.session_state:
    st.session_state.quick_taps = 0
if "taps" not in st.session_state:
    st.session_state.taps = 0

TOTAL_CANDLES = 5
TARGET_GOOD_ITEMS = 5
NAMA_PENERIMA = "Sr. Fabiola, SPM"
assets_dir = Path(__file__).parent / "assets"

# --- MINI AUDIO PLAYER ---
music_path = assets_dir / "birthday_music.mp3"
if music_path.exists():
    st.markdown('<div class="audio-pill"><div class="audio-pill-label">🎵 Putar musik dulu biar makin seru!</div>', unsafe_allow_html=True)
    st.audio(str(music_path), format="audio/mp3")
    st.markdown('</div>', unsafe_allow_html=True)

# --- HEADER ---
st.markdown("""
<div class="hero-card">
    <p class="main-title">2026 umur berapa kaks?? 🎉</p>
    <div><span class="subtitle">Ciye 28 tahun ciye uhuyy💗</span></div>
</div>
""", unsafe_allow_html=True)

image_path = assets_dir / "koala.jpg"
if not image_path.exists():
    image_path = assets_dir / "koala.png"


# ==========================================
# STAGE ARCADE 1: TANGKAP BERKAH (TANPA HINT)
# ==========================================
if st.session_state.game_state == "arcade_1":
    st.markdown("""
    <div class="game-box">
        <h3 style="font-family:'Comic Sans MS', 'Comic Sans', cursive; color:#0369A1; margin:0 0 4px 0;">🎮 Level 1: Panen Berkah Ultah!</h3>
        <p style="font-size:13px; color:#334155; margin:0;">
            Pilih dan kumpulin <b>5 item yang tepat</b> dari tombol-tombol di bawah ini. Hati-hati salah pilih ya! 😉
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="score-banner">
        <span>⭐ Skor Total: {st.session_state.arcade_score} Poin</span>
        <span>🎁 Terkumpul: {len(st.session_state.clicked_items)} / {TARGET_GOOD_ITEMS}</span>
    </div>
    """, unsafe_allow_html=True)

    # Daftar item campuran (Good & Zonk tersembunyi)
    all_arcade_items = [
        {"id": 1, "emoji": "🌸", "label": "Sehat jiwa raga", "points": 20, "good": True},
        {"id": 2, "emoji": "☕", "label": "Kopi uenak Pagi Hari", "points": 15, "good": True},
        {"id": 3, "emoji": "💖", "label": "Hati Penuh Syukur", "points": 30, "good": True},
        {"id": 4, "emoji": "🐨", "label": "Rebahan seharian", "points": 25, "good": True},
        {"id": 5, "emoji": "🍰", "label": "Kue Coklat Gratis", "points": 20, "good": True},
        {"id": 6, "emoji": "✨", "label": "Good Vibes Only", "points": 25, "good": True},
        {"id": 7, "emoji": "🍕", "label": "Traktiran Pizza", "points": 20, "good": True},
        {"id": 8, "emoji": "🛍️", "label": "Diskon Belanjaan", "points": 15, "good": True},
        {"id": 9, "emoji": "💤", "label": "Tidur Jam 9 Malam", "points": -10, "good": False},
        {"id": 10, "emoji": "💻", "label": "Revisi Mendadak", "points": -15, "good": False},
        {"id": 11, "emoji": "🌧️", "label": "Hujan pas Mau Pulang", "points": -10, "good": False},
        {"id": 12, "emoji": "🔋", "label": "Batre HP Lowbat", "points": -15, "good": False}
    ]

    cols = st.columns(2)
    for idx, item in enumerate(all_arcade_items):
        with cols[idx % 2]:
            is_clicked = item["id"] in st.session_state.clicked_items
            if is_clicked:
                st.button(f"✅ {item['label']}", key=f"item_{item['id']}", disabled=True, use_container_width=True)
            else:
                btn_label = f"{item['emoji']} {item['label']}"
                if st.button(btn_label, key=f"item_{item['id']}", use_container_width=True):
                    if item["good"]:
                        st.session_state.arcade_score += item["points"]
                        st.session_state.clicked_items.append(item["id"])
                        st.success(f"Asyik! Pilihan tepat (+{item['points']} poin) 🎉")
                    else:
                        st.session_state.arcade_score += item["points"]
                        st.warning(f"Ups, kurang pas! ({item['points']} poin) 🙈")
                    st.rerun()

    st.write("")
    if len(st.session_state.clicked_items) >= TARGET_GOOD_ITEMS:
        if st.button("🚀 TARGET TERCAPAI! LANJUT KE LEVEL 2 ➡️", use_container_width=True):
            st.session_state.game_state = "arcade_2"
            st.rerun()


# ==========================================
# STAGE ARCADE 2: PILIH KOTAK HOKI (TANPA HINT)
# ==========================================
elif st.session_state.game_state == "arcade_2":
    st.markdown("""
    <div class="game-box">
        <h3 style="font-family:'Comic Sans MS', 'Comic Sans', cursive; color:#0369A1; margin:0 0 4px 0;">🎯 Level 2: Pilih Kotak Misteri!</h3>
        <p style="font-size:13px; color:#334155; margin:0;">
            Ada kotak misterius berhadiah poin rahasia. Percaya instingmu dan pilih salah satu:
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="score-banner">
        <span>⭐ Skor Total: {st.session_state.arcade_score} Poin</span>
        <span>🕹️ Status: Level 2 / 3</span>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        if st.button("🎁 Kotak A", use_container_width=True):
            st.session_state.arcade_score += 25
            st.success("Hoki banget! Bonus +25 Poin! ✨")
            st.session_state.game_state = "arcade_3"
            st.rerun()
            
    with col_b:
        if st.button("🎁 Kotak B", use_container_width=True):
            st.session_state.arcade_score += 50
            st.balloons()
            st.success("JACKPOT! Bonus +50 Poin! 🎉")
            st.session_state.game_state = "arcade_3"
            st.rerun()
            
    with col_c:
        if st.button("🎁 Kotak C", use_container_width=True):
            st.session_state.arcade_score += 10
            st.info("Lumayan, dapet Bonus +10 Poin! 👍")
            st.session_state.game_state = "arcade_3"
            st.rerun()


# ==========================================
# STAGE ARCADE 3: QUICK TAP SEMANGAT
# ==========================================
elif st.session_state.game_state == "arcade_3":
    st.markdown("""
    <div class="game-box">
        <h3 style="font-family:'Comic Sans MS', 'Comic Sans', cursive; color:#0369A1; margin:0 0 4px 0;">⚡ Level 3: Tap Semangat Cepat!</h3>
        <p style="font-size:13px; color:#334155; margin:0;">
            Tap tombol di bawah ini minimal <b>3 kali</b> buat ngumpulin energi penuh sebelum kuenya terbuka!
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="score-banner">
        <span>⭐ Skor Total: {st.session_state.arcade_score} Poin</span>
        <span>⚡ Tap Semangat: {st.session_state.quick_taps} / 3</span>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    if st.button("🔥 TAP SEMANGAT! 🚀", use_container_width=True):
        st.session_state.quick_taps += 1
        st.session_state.arcade_score += 15
        st.rerun()

    st.write("")
    if st.session_state.quick_taps >= 3:
        if st.button("🎂 SELESAI SEMUA LEVEL! BUKA KUE UTAMA 🎉", use_container_width=True):
            st.session_state.game_state = "candles"
            st.rerun()


# ==========================================
# STAGE 2: TIUP LILIN UTAMA
# ==========================================
elif st.session_state.game_state == "candles":
    remaining = max(TOTAL_CANDLES - st.session_state.taps, 0)

    if remaining > 0:
        col_left, col_right = st.columns([0.85, 1.15], gap="medium")

        with col_left:
            st.markdown('<div class="koala-wrap">', unsafe_allow_html=True)
            if image_path.exists():
                st.image(str(image_path), use_container_width=True)
            else:
                st.markdown('<div style="font-size:80px;text-align:center;padding:12px 0;">🐨</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_right:
            candles = " ".join(["🕯️" if i < remaining else "💨" for i in range(TOTAL_CANDLES)])
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.95); backdrop-filter:blur(6px); border:2px solid #E2E8F0; border-bottom:5px solid #FACC15; border-radius:22px; padding:16px 12px; text-align:center; box-shadow:0 8px 20px rgba(15,23,42,0.07);">
                <p style="font-size:13px; font-weight:700; color:#64748B; margin:0;">Happy Birthday,</p>
                <div style="font-family:'Comic Sans MS', 'Comic Sans', cursive; color:#0369A1; font-size:17px; font-weight:700; margin:2px 0 6px 0;">{NAMA_PENERIMA}! 💕</div>
                <div style="font-size:26px; letter-spacing:4px; margin:4px 0; display:inline-block;">{candles}</div>
                <div style="font-size:38px; line-height:1.1;">🎂</div>
                <div style="background:#F1F5F9; color:#334155; display:inline-block; padding:4px 12px; border-radius:50px; font-size:12px; font-weight:700; margin-top:6px;">
                    Lilin menyala: <b style="color:#D97706; font-size:13.5px;">{remaining}</b> / {TOTAL_CANDLES}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.progress(st.session_state.taps / TOTAL_CANDLES)

        st.markdown(
            "<p style='text-align:center;color:#334155;font-size:13.5px;font-weight:700;margin:6px 0 10px 0;'>"
            "Buat permohonan dalam hati, lalu tap tombol untuk meniup lilin! ✨</p>",
            unsafe_allow_html=True
        )

        if st.button("💨 TAP! Tiup lilin", use_container_width=True):
            st.session_state.taps = min(st.session_state.taps + 1, TOTAL_CANDLES)
            st.rerun()

    else:
        st.balloons()
        st.snow()

        st.markdown('<div style="text-align:center; margin: 10px 0 16px 0;"><div class="koala-wrap" style="max-width:210px;">', unsafe_allow_html=True)
        if image_path.exists():
            st.image(str(image_path), use_container_width=True)
        else:
            st.markdown('<div style="font-size:90px;text-align:center;padding:16px 0;">🐨</div>', unsafe_allow_html=True)
        st.markdown('</div></div>', unsafe_allow_html=True)

        st.markdown(
            f"<p style='text-align:center;color:#0369A1;font-size:15px;font-weight:800;margin-bottom:12px;'>"
            f"Yeay! Semua lilin padam! Total Skor Arcade: {st.session_state.arcade_score} ⭐ 🥳</p>",
            unsafe_allow_html=True
        )

        if st.button("🔄 Mainkan Ulang Game Dari Awal", use_container_width=True):
            st.session_state.taps = 0
            st.session_state.arcade_score = 0
            st.session_state.clicked_items = []
            st.session_state.quick_taps = 0
            st.session_state.game_state = "arcade_1"
            st.rerun()

        # Pop-up Wish Card
        @st.dialog("🌟 Yeay! Pesan Spesial Ultah 🌟")
        def show_wish_modal():
            st.markdown("""
            <div style="background-color:#FFFFFF; color:#1E293B; font-size:15px; line-height:1.65; text-align:center; padding:4px 6px;">
                <p style="color:#1E293B; margin-bottom:6px; font-weight:700; font-size:17px;">Selamat ulang tahun 🥳</p>
                <p style="color:#0369A1; margin-bottom:12px; font-weight:800;">ke 28 tahun ya</p>
                <p style="color:#334155; margin-bottom:12px;">Semoga di usia yang baru ini, kamu selalu diberi kesehatan, kebahagiaan, dan hati yang penuh rasa syukur.</p>
                <p style="color:#334155; margin-bottom:14px;">Semoga setiap langkahmu dipenuhi hal-hal baik, semoga setia dalam menjalani panggilan Tuhan, dan semakin menikmati cara Tuhan membentukmu.</p>
                <div style="background-color:#FEF9C3; border-left:4px solid #EAB308; padding:12px 14px; border-radius:12px; margin:14px 0; text-align:left; font-weight:700; color:#713F12; box-shadow: 0 4px 12px rgba(234, 179, 8, 0.15);">
                    Tetap jadi pribadi yang baik, kuat, dan shinning shimmering splendid. Jangan lupa bahagia dan mengandalkan Tuhan Yesus, ya! 💗
                </div>
                <h3 style="font-family:'Comic Sans MS', 'Comic Sans', cursive; color:#0284C7; margin-top:14px; font-size:20px;">With love, lots of hugs! 💐</h3>
            </div>
            """, unsafe_allow_html=True)

            st.write("")
            if st.button("🔄 Mainkan Ulang Dari Awal", key="modal_reset", use_container_width=True):
                st.session_state.taps = 0
                st.session_state.arcade_score = 0
                st.session_state.clicked_items = []
                st.session_state.quick_taps = 0
                st.session_state.game_state = "arcade_1"
                st.rerun()

        show_wish_modal()

# --- FOOTER ---
st.markdown('<div class="footer-sign">giaaaaaaaaa</div>', unsafe_allow_html=True)
import base64
from datetime import datetime, timedelta
import os
import random
import pandas as pd
import pydeck as pdk
import requests
import streamlit as st

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Merpati Putih - Remaja Terencana",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 2. URL GOOGLE APPS SCRIPT (API ENDPOINTS)
# ==========================================
API_URL_MATERI = "https://script.google.com/macros/s/AKfycbwLfXYY-9-PwdVB1xQKtD1c2npawNgTeOuGHmDzPr7LGC1inbTxuxwnt8m7Z0LcJHsxyA/exec"
API_URL_GALERI = "https://script.google.com/macros/s/AKfycbz-rX4p9SpDIE1TVv1zuItWKKgKxd0AJSWpib8XGCjE4oHb_n1RAH-4azED-MCCjpaHXg/exec"
API_URL_CERITA = "https://script.google.com/macros/s/AKfycbxCPeC-7fE7Fu2O1J5dJ7-juwi3iQrl0L0ug3nonVuTIf_sC0yJYjZ6mS4HaQDH4y-g/exec"
API_URL_KRITIK = "https://script.google.com/macros/s/AKfycbxMSnhdLOf1RbVDMRzxuiW1ITEvGQWcMcF5dTxiTmk7HWC4M8u21CYQ_jtrOdoQOI6B/exec"

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def fetch_api_data(url):
    if not url or "script.google.com" not in url:
        return []
    try:
        res = requests.get(url, timeout=6)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and "data" in data:
                return data["data"]
        return []
    except Exception:
        return []

def save_api_data(url, data_list):
    if not url or "script.google.com" not in url:
        return False
    try:
        res = requests.post(url, json={"data": data_list}, timeout=8)
        return res.status_code == 200
    except Exception:
        return False

# ==========================================
# 4. INITIAL MATERI EDUKASI
# ==========================================
MATERI_DEFAULT = [
    {
        "Judul": "🩸 Anemia: 'Baterai Drop' Penyebab Otak Lemot & Muka Pucat!",
        "Isi": "**Pernah ngerasa gampang ngantuk di kelas, muka pucat, dan mager parah? Bisa jadi kamu kena Anemia!** 🪫\n\nAnemia terjadi saat kadar **Hemoglobin (Hb)** drop akibat kekurangan zat besi. Hb ini ibarat 'ojek online' di dalam darah yang bertugas mengantar oksigen ke otak dan seluruh tubuh.\n\n**Gaya 5L yang Bikin Hidup Nggak Asyik:**\n1. **L**esu\n2. **L**emah\n3. **L**elah\n4. **L**etih\n5. **L**alai (Gampang lupa & susah fokus)\n\n**Kenapa Remaja Putri Paling Rawan?**\nKarena remaja putri mengalami menstruasi setiap bulan dan sering kali melakukan diet ketat yang salah.\n\n**Solusi Sat-Set Biar Baterai Tubuh Full Lagi:**\n• 💊 **Minum TTD (Tablet Tambah Darah):** Rutin **1 tablet seminggu sekali** (dan **1 tablet sehari saat menstruasi**).\n• 🍊 **Combo Vitamin C:** Minum TTD bareng es jeruk/jus buah biar penyerapan zat besinya maksimal!\n• 🚫 **Hindari Banting Zat Besi:** Jangan minum TTD barengan sama **Kopi, Teh, atau Susu**, karena bisa bikin zat besinya gagal diserap tubuh.",
        "Foto": "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?q=80&w=800&auto=format&fit=crop"
    },
    {
        "Judul": "🛑 Stunting: Bukan Cuma Pendek, Tapi Otak Juga 'Loading' Lama!",
        "Isi": "**Banyak yang salah kaprah: 'Pendek itu kan faktor keturunan (genetik)?' Eits, tunggu dulu!** ✋\n\nOrang pendek belum tentu stunting, tapi orang stunting **pasti pendek** dan pertumbuhan otak serta daya tahan tubuhnya terhambat akibat **kurang gizi kronis dalam 1.000 Hari Pertama Kehidupan (HPHT)**.\n\n**Dampak Horor Stunting:**\n• 🧠 **IQ Rendah:** Otak jadi lambat merespon dan sulit bersaing di dunia kerja.\n• 🤒 **Gampang Sakit:** Imunitas tubuh lemah.\n• 💸 **Biaya Berobat Mahal:** Berisiko kena penyakit tidak menular (diabetes, jantung) saat dewasa.\n\n**Gimana Cara Remaja Cegah Stunting dari Sekarang?**\n• 🥚 **Gempur Protein Hewani:** Rutin makan Telur, Ikan, Ayam, atau Daging. Telur 1-2 butir sehari itu *superfood* murah cegah stunting!\n• 💍 **Stop Pernikahan Dini:** Usia ibu yang belum siap (di bawah 21 tahun) bikin risiko bayi lahir stunting melonjak tajam!\n• 🩺 **Skrining Catin (Calon Pengantin):** Cek Hb dan Lingkar Lengan Atas (LILA) minimal 3 bulan sebelum nikah.",
        "Foto": "https://images.unsplash.com/photo-1498837167922-ddd27525d352?q=80&w=800&auto=format&fit=crop"
    },
    {
        "Judul": "🚀 Bonus Demografi: Indonesia Emas atau 'Bencana Demografi'?",
        "Isi": "**Kamu sadar nggak, kalau kamu dan teman-temanmu adalah penentu nasib Indonesia beberapa tahun ke depan?** 🇮🇩🔥\n\n**Apa Itu Bonus Demografi?**\nBonus Demografi adalah momen langka sekali seumur hidup di mana jumlah **penduduk usia produktif (15-64 tahun)** jauh lebih banyak dibandingkan penduduk non-produktif.\n\n**Peluang 'Indonesia Emas 2045':**\nKalau remajanya cerdas, sehat, kreatif, dan punya *skill* tinggi, Indonesia bisa berubah jadi negara maju dunia!\n\n**Ancaman 'Bencana Demografi':**\nTapi kalau remajanya malah terjebak **Triad KRR** (Seks Bebas, Nikah Dini, NAPZA), kena **Anemia**, dan melahirkan anak-anak **Stunting**, bonus demografi justru jadi beban berat buat negara!\n\n**Peran Kamu Sebagai GenRe:**\n1. 📚 Bekali diri dengan *Life Skills* & literasi digital.\n2. 🛡️ Berani bilang **TIDAK** pada Pernikahan Dini & Narkoba.\n3. 🎯 Rencanakan pendidikan, karir, dan pernikahan secara matang.",
        "Foto": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=800&auto=format&fit=crop"
    }
]

# ==========================================
# 5. SESSION STATE INITIALIZATION
# ==========================================
if "daftar_materi" not in st.session_state:
    api_materi = fetch_api_data(API_URL_MATERI)
    st.session_state["daftar_materi"] = api_materi if len(api_materi) > 0 else MATERI_DEFAULT
else:
    for m_def in MATERI_DEFAULT:
        if not any(x.get("Judul") == m_def["Judul"] for x in st.session_state["daftar_materi"]):
            st.session_state["daftar_materi"].append(m_def)

if "daftar_galeri" not in st.session_state:
    st.session_state["daftar_galeri"] = fetch_api_data(API_URL_GALERI)

if "tagline" not in st.session_state:
    st.session_state["tagline"] = "Sebuah Gerakan dari Remaja untuk Melangitkan Harapan dan Membumikan Kebermanfaatan."

if "jurnal_ttd" not in st.session_state:
    st.session_state["jurnal_ttd"] = {"Minggu 1": False, "Minggu 2": False, "Minggu 3": False, "Minggu 4": False}

# ==========================================
# 6. WALLPAPER BACKGROUND HELPER
# ==========================================
def get_base64_bg(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/webp;base64,{encoded}"
    return ""

bg_image = get_base64_bg("25117787.webp")

# ==========================================
# 7. CUSTOM CSS (STYLING)
# ==========================================
st.markdown(f"""
    <style>
    html {{ scroll-behavior: smooth; }}
    .stApp {{
        background: linear-gradient(rgba(15, 23, 42, 0.88), rgba(15, 23, 42, 0.95)), url("{bg_image}"); 
        background-size: cover !important; background-position: center !important; background-attachment: fixed !important;
        color: #F8FAFC !important;
    }}
    .hero-title {{ font-size: 3.2rem; font-weight: 800; color: #FFFFFF; line-height: 1.2; margin-bottom: 15px; text-shadow: 0 4px 12px rgba(0,0,0,0.5); }}
    .hero-subtitle {{ font-size: 1.25rem; color: #38BDF8; font-weight: 600; margin-bottom: 20px; }}
    .section-title {{ font-size: 2rem; font-weight: 700; text-align: center; color: #FFFFFF; margin-top: 35px; margin-bottom: 25px; }}
    .stApp p, .stApp span, .stApp label, .stApp div {{ color: #E2E8F0 !important; }}
    [data-testid="stMetricValue"] {{ color: #38BDF8 !important; font-size: 2.3rem !important; font-weight: 800 !important; }}
    div.stMetric {{ background: rgba(30, 41, 59, 0.65) !important; padding: 20px 15px !important; border-radius: 16px !important; border: 1px solid rgba(255, 255, 255, 0.12) !important; text-align: center !important; }}
    div[data-testid="stRadio"] > label {{ display: none; }}
    div[data-testid="stRadio"] > div {{ background-color: rgba(30, 41, 59, 0.7); padding: 8px; border-radius: 14px; gap: 8px; border: 1px solid rgba(255, 255, 255, 0.12); flex-wrap: wrap; }}
    div[data-testid="stRadio"] label[data-baseweb="radio"] {{ background-color: transparent; padding: 8px 18px !important; border-radius: 10px; transition: all 0.25s ease; }}
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {{ background-color: #38BDF8 !important; }}
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) span {{ color: #0F172A !important; font-weight: 700 !important; }}
    .stExpander, div[data-testid="stForm"] {{ background-color: rgba(30, 41, 59, 0.55) !important; border: 1px solid rgba(255, 255, 255, 0.12) !important; border-radius: 14px !important; padding: 20px !important;}}
    .hotline-card {{ background: rgba(220, 38, 38, 0.15); border-left: 5px solid #DC2626; padding: 15px; border-radius: 8px; margin-bottom: 15px; }}
    .hotline-title {{ font-size: 1.2rem; font-weight: bold; color: #FCA5A5; }}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 8. HEADER & NAVIGATION
# ==========================================
col_logo, col_nav = st.columns([1, 4], vertical_alignment="center")
with col_logo:
    if os.path.exists("Logo bumper (1).png"):
        st.image("Logo bumper (1).png", width=140)
    else:
        st.markdown("<h3 style='color:#FFFFFF; margin:0; font-weight:800;'>🕊️ MERPATI PUTIH</h3>", unsafe_allow_html=True)

with col_nav:
    # Mengembalikan menu Kenali Lebih Dekat dan menyesuaikan nama Ruang Cerita
    menu = st.radio("Menu Navigation", [
        "Beranda", 
        "Kenali Lebih Dekat",
        "Edukasi & Tools Terpadu", 
        "Kuis GenRe", 
        "Konsultasi & Ruang Cerita", 
        "Kritik & Saran", 
        "Admin"
    ], horizontal=True)

st.markdown("<hr style='margin-top:5px; margin-bottom:25px; border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

# ---------------------------------------------------------
# MENU 1: BERANDA
# ---------------------------------------------------------
if menu == "Beranda":
    h_col1, h_col2 = st.columns([1.2, 1], gap="large")
    with h_col1:
        st.markdown('<div class="hero-title">Merpati Putih: Menuju Era Remaja Terencana.</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-subtitle">{st.session_state["tagline"]}</div>', unsafe_allow_html=True)
        st.write("Jadilah pemuda yang aktif, harmonis, unggul, terencana, inspiratif, & hebat. Masa depan yang cemerlang dimulai dari langkah nyata hari ini.")
        
        quotes = [
            "Perencanaan hari ini adalah kunci kebahagiaan esok hari.",
            "Remaja Hebat itu menjauhi Narkoba, Seks Bebas, dan Pernikahan Dini!",
            "Tunda nikah muda, kejar prestasi setinggi-tingginya!"
        ]
        if st.button("🎲 Motivasi GenRe Hari Ini"):
            st.info(f'💡 *"{random.choice(quotes)}"*')

    with h_col2:
        if os.path.exists("genre_juara1.jpg"):
            st.image("genre_juara1.jpg", use_container_width=True)

    st.markdown('<div class="section-title">📊 Merpati Putih Dalam Angka</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Tahun Dedikasi", "1+")
    m2.metric("Remaja Terdampak", "200+")
    m3.metric("Titik Wilayah", "12")
    m4.metric("Aspirasi Masuk", str(len(fetch_api_data(API_URL_CERITA))))

    # PETA SPASIAL
    st.markdown('<div class="section-title">🗺️ Peta Zonasi "Blue Zone" (Cilacap Selatan)</div>', unsafe_allow_html=True)
    zona_cilacap_selatan = [[108.990, -7.745], [109.025, -7.745], [109.020, -7.710], [108.995, -7.710], [108.990, -7.745]]
    df_zona = pd.DataFrame({"zona": ["Kec. Cilacap Selatan"], "deskripsi": ["Wilayah percontohan bebas Stunting"], "koordinat": [[zona_cilacap_selatan]]})
    
    layer_polygon = pdk.Layer("PolygonLayer", df_zona, get_polygon="koordinat", get_fill_color="[56, 189, 248, 80]", get_line_color="[2, 132, 199, 255]", get_line_width=80, pickable=True)
    view_state = pdk.ViewState(latitude=-7.7279, longitude=109.0063, zoom=12.2, pitch=25)
    st.pydeck_chart(pdk.Deck(map_style="dark", initial_view_state=view_state, layers=[layer_polygon]))

    # GALERI
    st.markdown('<div class="section-title">🖼️ Galeri Kegiatan</div>', unsafe_allow_html=True)
    galeri_api = st.session_state.get("daftar_galeri", [])
    if galeri_api:
        g_cols = st.columns(3)
        for i, url_img in enumerate(galeri_api):
            try:
                g_cols[i % 3].image(url_img, use_container_width=True)
            except: pass
    else:
        st.info("Belum ada foto galeri.")

# ---------------------------------------------------------
# MENU 2: KENALI LEBIH DEKAT
# ---------------------------------------------------------
elif menu == "Kenali Lebih Dekat":
    st.markdown('<div class="section-title">✨ Kenali Merpati Putih Lebih Dekat</div>', unsafe_allow_html=True)
    
    col_profil1, col_profil2 = st.columns([1, 1])
    with col_profil1:
        st.subheader("🌟 Visi Kami")
        st.write("Mewujudkan generasi muda Cilacap yang terencana, bebas stunting, dan memiliki kesadaran tinggi akan pentingnya kesehatan reproduksi serta masa depan yang cerah.")
        
        st.subheader("🎯 Misi Kami")
        st.write("""
        1. Memberikan edukasi gizi dan pencegahan stunting secara interaktif.
        2. Menyediakan wadah konsultasi yang aman bagi remaja.
        3. Membangun kesadaran tentang bahaya Triad KRR.
        4. Mendorong remaja putri rutin mengonsumsi Tablet Tambah Darah (TTD).
        """)
    
    with col_profil2:
        st.subheader("🤝 Siapa Kami?")
        st.write("Merpati Putih lahir dari keresahan dan kepedulian remaja terhadap tingginya angka stunting dan pernikahan dini. Kami adalah agen perubahan (Agent of Change) dari jalur GenRe yang siap merangkul, mengedukasi, dan menjadi teman curhat yang aman bagi sesama remaja.")
        st.info("💡 **Prinsip Kami:** Dari Remaja, Oleh Remaja, Untuk Remaja.")

# ---------------------------------------------------------
# MENU 3: EDUKASI & TOOLS TERPADU
# ---------------------------------------------------------
elif menu == "Edukasi & Tools Terpadu":
    st.markdown('<div class="section-title">🚀 Super Tools GenRe Terpadu</div>', unsafe_allow_html=True)
    
    t1, t2, t3, t4, t5, t6, t7, t8 = st.tabs([
        "📖 Materi", "⚖️ IMT", "🍽️ Piringku", "💍 Catin", 
        "🗓️ Siklus & Habit", "💰 Dana", "🚨 Hotline", "🏥 Faskes"
    ])

    # 1. TAB MATERI (MEMPERBAIKI ERROR GAMBAR DI SINI)
    with t1:
        search_kw = st.text_input("🔍 Cari Materi...")
        materi_all = st.session_state.get("daftar_materi", [])
        materi_filtered = [m for m in materi_all if search_kw.lower() in m.get("Judul","").lower() or search_kw.lower() in m.get("Isi","").lower()] if search_kw else materi_all
        
        for m in materi_filtered:
            with st.expander(f"📌 {m.get('Judul')}"):
                st.markdown(m.get("Isi"))
                
                # FIX: Try-Except untuk mencegah crash jika link gambar kosong/rusak
                foto_url = m.get("Foto", "")
                if foto_url and isinstance(foto_url, str) and foto_url.strip() != "":
                    try:
                        st.image(foto_url, width=500)
                    except Exception:
                        pass # Abaikan jika gambar gagal dimuat, web tidak akan crash

    # 2. TAB IMT
    with t2:
        c_berat, c_tinggi = st.columns(2)
        berat = c_berat.number_input("Berat Badan (Kg)", 20.0, 150.0, 50.0)
        tinggi = c_tinggi.number_input("Tinggi Badan (Cm)", 100.0, 220.0, 160.0)
        if st.button("Hitung IMT", type="primary"):
            imt = berat / ((tinggi/100)**2)
            st.info(f"Nilai IMT Kamu: **{imt:.1f}**")

    # 3. TAB PIRINGKU
    with t3:
        st.write("Panduan porsi gizi seimbang cegah stunting.")
        f_pokok = st.selectbox("1. Karbohidrat", ["Nasi", "Kentang", "Tidak Ada"])
        f_lauk_h = st.selectbox("2. Protein Hewani", ["Telur", "Ikan", "Ayam", "Tidak Ada"])
        f_sayur = st.selectbox("3. Sayur", ["Bayam", "Wortel", "Tidak Ada"])
        if st.button("Cek Gizi", type="primary"):
            if f_lauk_h == "Tidak Ada": st.error("🚨 Protein Hewani Wajib Ada untuk mencegah stunting!")
            else: st.success("Piringmu bergizi!")

    # 4. TAB CATIN
    with t4:
        st.write("Skrining Kesiapan Menikah BKKBN")
        u_wanita = st.number_input("Usia Catin (Thn)", 15, 50, 22)
        hb_wanita = st.number_input("Hb (g/dL)", 7.0, 18.0, 12.5)
        if st.button("Cek Skrining", type="primary"):
            if u_wanita >= 21 and hb_wanita >= 12.0:
                st.success("Sangat Siap Menikah dan Hamil!")
            else:
                st.warning("Perbaiki usia/gizi sebelum menikah.")

    # 5. TAB SIKLUS & HABIT TTD
    with t5:
        st.subheader("🌸 Kalender Haid & Habit Tracker TTD")
        hpht = st.date_input("Hari Pertama Haid Terakhir", value=datetime.now())
        if st.button("Hitung Siklus", type="primary"):
            st.info(f"Est. Haid Berikutnya: {(hpht + timedelta(days=28)).strftime('%d %B %Y')}")
        
        st.markdown("---")
        st.subheader("✅ Jurnal Habit Minum Tablet Tambah Darah (TTD)")
        st.write("Catat konsumsi TTD-mu bulan ini biar nggak lupa (1 Tablet / Minggu).")
        
        c1, c2, c3, c4 = st.columns(4)
        st.session_state["jurnal_ttd"]["Minggu 1"] = c1.checkbox("Minggu 1", value=st.session_state["jurnal_ttd"]["Minggu 1"])
        st.session_state["jurnal_ttd"]["Minggu 2"] = c2.checkbox("Minggu 2", value=st.session_state["jurnal_ttd"]["Minggu 2"])
        st.session_state["jurnal_ttd"]["Minggu 3"] = c3.checkbox("Minggu 3", value=st.session_state["jurnal_ttd"]["Minggu 3"])
        st.session_state["jurnal_ttd"]["Minggu 4"] = c4.checkbox("Minggu 4", value=st.session_state["jurnal_ttd"]["Minggu 4"])
        
        progress = sum(st.session_state["jurnal_ttd"].values()) / 4
        st.progress(progress)
        if progress == 1.0: st.success("Keren! Kamu sudah full minum TTD bulan ini.")

    # 6. TAB DANA
    with t6:
        st.subheader("💰 Perencana Finansial Remaja")
        tujuan = st.selectbox("Tujuan", ["Kuliah", "Modal Usaha", "Menikah"])
        target = st.number_input("Target Dana (Rp)", value=10000000, step=1000000)
        bulan = st.number_input("Target Tercapai (Bulan)", value=24)
        if st.button("Hitung Tabungan", type="primary"):
            st.info(f"Kamu harus menabung Rp {int(target/bulan):,} / Bulan untuk target {tujuan}.")

    # 7. TAB HOTLINE
    with t7:
        st.subheader("🚨 Pusat Bantuan Darurat")
        st.markdown('''
        <div class="hotline-card"><div class="hotline-title">📞 SAPA 129</div>Kekerasan Perempuan & Anak<br><a href="tel:129" style="color:#FFF;">Telepon 129</a></div>
        <div class="hotline-card"><div class="hotline-title">🛑 BNN Call Center</div>Penyalahgunaan NAPZA<br><a href="tel:184" style="color:#FFF;">Telepon 184</a></div>
        ''', unsafe_allow_html=True)

    # 8. TAB FASKES
    with t8:
        st.subheader("🏥 Direktori Faskes Cilacap Selatan")
        st.write("Tempat cek kesehatan, ambil TTD, dan konsultasi Gizi terdekat.")
        
        df_faskes = pd.DataFrame({
            "Nama": ["Puskesmas Cilacap Sel I", "Puskesmas Cilacap Sel II", "Klinik Pratama XYZ"],
            "Lat": [-7.7310, -7.7200, -7.7250],
            "Lon": [109.0110, 109.0020, 109.0150]
        })
        
        st.dataframe(df_faskes[["Nama"]])
        
        layer_faskes = pdk.Layer(
            "ScatterplotLayer",
            df_faskes,
            get_position="[Lon, Lat]",
            get_color="[220, 38, 38, 200]",
            get_radius=200,
            pickable=True
        )
        view_faskes = pdk.ViewState(latitude=-7.7250, longitude=109.0080, zoom=13)
        st.pydeck_chart(pdk.Deck(map_style="light", initial_view_state=view_faskes, layers=[layer_faskes], tooltip={"html": "<b>{Nama}</b>"}))

# ---------------------------------------------------------
# MENU 4, 5, 6, 7 (KUIS, CERITA, KRITIK, ADMIN)
# ---------------------------------------------------------
elif menu == "Kuis GenRe":
    st.markdown('<div class="section-title">🧩 Kuis Kesiapan Remaja (Sample)</div>', unsafe_allow_html=True)
    st.write("1. Apa kepanjangan GenRe?")
    ans = st.radio("Jawaban:", ["Generasi Remaja", "Generasi Berencana"], index=None)
    if st.button("Cek"):
        if ans == "Generasi Berencana": st.success("Benar!")
        else: st.error("Salah!")

elif menu == "Konsultasi & Ruang Cerita":
    st.markdown('<div class="section-title">💬 Ruang Cerita Anonim</div>', unsafe_allow_html=True)
    daftar_cerita = fetch_api_data(API_URL_CERITA)
    with st.form("cerita_form"):
        user_input = st.text_area("Tulis curhatan anonim...")
        if st.form_submit_button("Kirim"):
            daftar_cerita.append({"Waktu": datetime.now().strftime("%d/%m/%Y"), "Cerita": user_input, "Respon Admin": ""})
            save_api_data(API_URL_CERITA, daftar_cerita)
            st.success("Terkirim!")
            st.rerun()
            
    for item in reversed(daftar_cerita):
        st.markdown(f"**Anonim:** {item.get('Cerita')}")
        if item.get('Respon Admin'): st.info(f"**Admin:** {item.get('Respon Admin')}")
        st.write("---")

elif menu == "Kritik & Saran":
    st.markdown('<div class="section-title">📥 Masukan Web</div>', unsafe_allow_html=True)
    with st.form("kritik_form"):
        k = st.text_area("Saran kamu?")
        if st.form_submit_button("Kirim"): st.success("Saran terkirim. Terima kasih!")

elif menu == "Admin":
    admin_pass = st.text_input("Passcode", type="password")
    if admin_pass == "chandikia":
        st.success("Akses Terbuka")
        st.write("Di sini Admin bisa balas cerita anonim, tambah materi, dan lihat data statistik web.")

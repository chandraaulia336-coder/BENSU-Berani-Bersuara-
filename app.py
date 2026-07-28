import streamlit as st
from datetime import datetime
import base64
import os
import requests
import pandas as pd

# 1. KONFIGURASI HALAMAN
st.set_page_config(
    page_title="Merpati Putih - Remaja Terencana",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. URL GOOGLE APPS SCRIPT (API ENDPOINTS)
API_URL_MATERI = "https://script.google.com/macros/s/AKfycbwLfXYY-9-PwdVB1xQKtD1c2npawNgTeOuGHmDzPr7LGC1inbTxuxwnt8m7Z0LcJHsxyA/exec"
API_URL_GALERI = "https://script.google.com/macros/s/AKfycbz-rX4p9SpDIE1TVv1zuItWKKgKxd0AJSWpib8XGCjE4oHb_n1RAH-4azED-MCCjpaHXg/exec"
API_URL_CERITA = "https://script.google.com/macros/s/AKfycbxCPeC-7fE7Fu2O1J5dJ7-juwi3iQrl0L0ug3nonVuTIf_sC0yJYjZ6mS4HaQDH4y-g/exec"
API_URL_KRITIK = "https://script.google.com/macros/s/AKfycbxMSnhdLOf1RbVDMRzxuiW1ITEvGQWcMcF5dTxiTmk7HWC4M8u21CYQ_jtrOdoQOI6B/exec"

# 3. HELPER FUNCTIONS
def fetch_api_data(url):
    if not url or "script.google.com" not in url:
        return []
    try:
        res = requests.get(url, timeout=6)
        return res.json() if res.status_code == 200 else []
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

# 4. SESSION STATE
if 'daftar_materi' not in st.session_state: 
    st.session_state['daftar_materi'] = fetch_api_data(API_URL_MATERI)
if 'daftar_galeri' not in st.session_state: 
    st.session_state['daftar_galeri'] = fetch_api_data(API_URL_GALERI)
if 'tagline' not in st.session_state: 
    st.session_state['tagline'] = "Sebuah Gerakan dari Remaja untuk Melangitkan Harapan dan Membumikan Kebermanfaatan."

# 5. WALLPAPER BACKGROUND HELPER
def get_base64_bg(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/webp;base64,{encoded}"
    return "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2000"

bg_image = get_base64_bg("25117787.webp")

# 6. CUSTOM CSS
st.markdown(f"""
    <style>
    html {{ scroll-behavior: smooth; }}
    .stApp {{
        background: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.95)), url("{bg_image}"); 
        background-size: cover !important; 
        background-position: center !important; 
        background-attachment: fixed !important;
        color: #F8FAFC !important;
    }}
    .hero-title {{ font-size: 3.2rem; font-weight: 800; color: #FFFFFF; line-height: 1.2; margin-bottom: 15px; text-shadow: 0 4px 12px rgba(0,0,0,0.5); }}
    .hero-subtitle {{ font-size: 1.25rem; color: #38BDF8; font-weight: 600; margin-bottom: 20px; }}
    .section-title {{ font-size: 2rem; font-weight: 700; text-align: center; color: #FFFFFF; margin-top: 35px; margin-bottom: 25px; }}
    .stApp p, .stApp span, .stApp label, .stApp div {{ color: #E2E8F0 !important; }}
    
    [data-testid="stMetricValue"] {{ color: #38BDF8 !important; font-size: 2.3rem !important; font-weight: 800 !important; }}
    [data-testid="stMetricLabel"] {{ color: #94A3B8 !important; font-size: 0.95rem !important; font-weight: 600 !important; }}
    div.stMetric {{
        background: rgba(30, 41, 59, 0.65) !important; padding: 20px 15px !important;
        border-radius: 16px !important; border: 1px solid rgba(255, 255, 255, 0.12) !important;
        backdrop-filter: blur(10px); box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25) !important; text-align: center !important;
    }}

    div[data-testid="stRadio"] > label {{ display: none; }}
    div[data-testid="stRadio"] > div {{
        background-color: rgba(30, 41, 59, 0.7); padding: 8px; border-radius: 14px; gap: 8px;
        border: 1px solid rgba(255, 255, 255, 0.12); backdrop-filter: blur(8px);
    }}
    div[data-testid="stRadio"] label[data-baseweb="radio"] {{
        background-color: transparent; padding: 8px 18px !important; border-radius: 10px;
        color: #94A3B8 !important; font-weight: 600; transition: all 0.25s ease;
    }}
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {{
        background-color: #38BDF8 !important; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4);
    }}
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) span {{ color: #0F172A !important; font-weight: 700 !important; }}
    
    .stExpander, div[data-testid="stForm"] {{
        background-color: rgba(30, 41, 59, 0.55) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important; border-radius: 14px !important;
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    .btn-merpati-putih {{
        display: inline-block; background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: #FFFFFF !important; padding: 12px 28px; border-radius: 10px; text-decoration: none;
        font-weight: 700; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.35);
    }}
    .btn-merpati-putih:hover {{ transform: translateY(-2px); color: #FFFFFF !important; }}

    .story-card {{ background: rgba(30, 41, 59, 0.6); border-radius: 12px; padding: 16px; border-left: 4px solid #38BDF8; margin-bottom: 15px; }}
    .admin-reply-card {{ background: rgba(16, 185, 129, 0.15); border-radius: 10px; padding: 12px; border-left: 4px solid #10B981; margin-top: 10px; }}
    </style>
""", unsafe_allow_html=True)

# 7. HEADER & NAV
col_logo, col_nav = st.columns([1, 4], vertical_alignment="center")
with col_logo:
    if os.path.exists("Logo bumper (1).png"):
        st.image("Logo bumper (1).png", width=140)
    else:
        st.markdown("<h3 style='color:#FFFFFF; margin:0; font-weight:800;'>🕊️ MERPATI PUTIH</h3>", unsafe_allow_html=True)

with col_nav:
    menu = st.radio(
        "Menu Navigation", 
        ["Beranda & Galeri", "Substansi Materi", "Kuis GenRe", "Ruang Cerita (Anonim)", "Kritik & Saran", "Admin Panel"], 
        horizontal=True
    )

st.markdown("<hr style='margin-top:5px; margin-bottom:25px; border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

# ---------------------------------------------------------
# MENU 1: BERANDA & GALERI
# ---------------------------------------------------------
if menu == "Beranda & Galeri":
    h_col1, h_col2 = st.columns([1.2, 1], gap="large")
    with h_col1:
        st.markdown('<div class="hero-title">Merpati Putih: Menuju Era Remaja Terencana.</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-subtitle">{st.session_state["tagline"]}</div>', unsafe_allow_html=True)
        st.write("Jadilah pemuda yang aktif, harmonis, unggul, terencana, inspiratif, & hebat. Karena masa depan yang cemerlang dimulai dari langkah nyata hari ini.")
        st.write("")
        st.markdown('<a href="#galeri" class="btn-merpati-putih">Mengenal Lebih Dekat 🚀</a>', unsafe_allow_html=True)

    with h_col2:
        if os.path.exists("genre_juara1.jpg"):
            st.image("genre_juara1.jpg", use_container_width=True)
        else:
            st.image("https://images.unsplash.com/photo-1529156069898-49953e39b3ac?q=80&w=1000", caption="Aksi Remaja Terencana", use_container_width=True)

    st.markdown('<div class="section-title">📊 Merpati Putih Dalam Angka</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Tahun Dedikasi", value="1+")
    m2.metric(label="Remaja Terdampak", value="200+")
    m3.metric(label="Program Berjalan", value="3")
    cerita_data = fetch_api_data(API_URL_CERITA)
    m4.metric(label="Aspirasi Masuk", value=str(len(cerita_data)))

    # TAMBAHAN 1: AGENDA PROGRAM KERJA
    st.markdown('<div class="section-title">📅 Agenda & Timeline Program Kerja</div>', unsafe_allow_html=True)
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        st.info("🎯 **Sosialisasi GenRe Goes to School**\n\n*Target:* SMA/SMK Cilacap\n\n*Status:* 🔥 On Going")
    with col_a2:
        st.success("💬 **Pojok Konseling Sebaya**\n\n*Target:* Remaja Desa/Kecamatan\n\n*Status:* 🟢 Setiap Akhir Pekan")
    with col_a3:
        st.warning("🏆 **Jambore Remaja Terencana**\n\n*Target:* Seluruh Kader PIK-R\n\n*Status:* ⏳ Merekrut Peserta")

    st.markdown('<div id="galeri" class="section-title">🖼️ Peta Jejak Keberdampakan (Galeri)</div>', unsafe_allow_html=True)
    if st.session_state['daftar_galeri']:
        g_cols = st.columns(3)
        for i, url_img in enumerate(st.session_state['daftar_galeri']):
            g_cols[i % 3].image(url_img, use_container_width=True)
    else:
        st.info("Belum ada foto galeri yang diunggah.")

# ---------------------------------------------------------
# MENU 2: SUBSTANSI MATERI
# ---------------------------------------------------------
elif menu == "Substansi Materi":
    st.markdown('<div class="section-title">📚 Substansi & Edukasi Materi</div>', unsafe_allow_html=True)
    if st.session_state['daftar_materi']:
        for m in st.session_state['daftar_materi']:
            with st.expander(f"📖  {m.get('Judul', 'Tanpa Judul')}"):
                st.markdown(f"*{m.get('Isi', '')}*")
                if m.get("Foto") and m["Foto"] != "None":
                    list_foto = [url.strip() for url in m["Foto"].split(",") if url.strip() and url.strip() != "None"]
                    if list_foto:
                        st.write("---")
                        cols_foto = st.columns(min(len(list_foto), 3))
                        for idx_f, url_f in enumerate(list_foto):
                            cols_foto[idx_f % 3].image(url_f, use_container_width=True)
    else: 
        st.info("Database materi belum tersedia.")

# ---------------------------------------------------------
# TAMBAHAN 2: MENU KUIS GENRE INTERAKTIF
# ---------------------------------------------------------
elif menu == "Kuis GenRe":
    st.markdown('<div class="section-title">🧩 Kuis Kesiapan Remaja Terencana</div>', unsafe_allow_html=True)
    st.write("Uji sejauh mana pemahaman dan kesiapan kamu dalam merencanakan masa depan!")
    
    with st.form("kuis_form"):
        q1 = st.radio("1. Apa usia ideal pernikahan bagi laki-laki dan perempuan menurut BKKBN?", 
                      ["A. 17 Laki-laki & 15 Perempuan", "B. 25 Laki-laki & 21 Perempuan", "C. Bebas kapan saja"])
        q2 = st.radio("2. Apa itu Triad KPA dalam program GenRe?", 
                      ["A. Katakan Tidak pada Pernikahan Dini, Seks Bebas, & Napza", "B. Tiga Budaya Khas Daerah", "C. Program Kursus"])
        q3 = st.radio("3. Mengapa perencanaan karir dan pendidikan penting sebelum menikah?", 
                      ["A. Agar punya gelar banyak", "B. Agar siap secara mental, finansial, dan sosial", "C. Mengikuti tren"])
        
        btn_kuis = st.form_submit_button("Cek Hasil Kuis 🎯", type="primary", use_container_width=True)
        if btn_kuis:
            skor = 0
            if "25 Laki-laki" in q1: skor += 33
            if "Pernikahan Dini" in q2: skor += 33
            if "mental, finansial" in q3: skor += 34
            
            st.balloons()
            st.success(f"🎉 **Skor Kesiapan Kamu: {skor} / 100**")
            if skor == 100:
                st.info("🌟 Luar Biasa! Kamu adalah Role Model Remaja Terencana Sejati!")
            else:
                st.warning("💪 Bagus! Pelajari materi di menu Substansi Materi untuk menambah wawasanmu ya!")

# ---------------------------------------------------------
# MENU 4: RUANG CERITA (ANONIM)
# ---------------------------------------------------------
elif menu == "Ruang Cerita (Anonim)":
    st.markdown('<div class="section-title">💬 Ruang Cerita Anonim</div>', unsafe_allow_html=True)
    col_info, col_form = st.columns([1, 1], gap="large")
    with col_info:
        if os.path.exists("genre_juara1.jpg"): 
            st.image("genre_juara1.jpg", caption="Duta GenRe Kecamatan Cilacap Selatan", use_container_width=True)
        st.write("Partisipasi remaja bukan hanya hadir, tapi ikut berpikir. Ruang ini adalah wadah aman dan rahasia untukmu berbagi cerita.")
        
    with col_form:
        daftar_cerita = fetch_api_data(API_URL_CERITA)
        with st.form("cerita_form", clear_on_submit=True):
            user_input = st.text_area("Tuliskan cerita/curhatan kamu di sini (100% Anonim)...", height=120)
            if st.form_submit_button("Kirim Cerita 💌", type="primary", use_container_width=True):
                if user_input.strip():
                    waktu_sekarang = datetime.now().strftime("%d/%m/%Y %H:%M")
                    daftar_cerita.append({"Waktu": waktu_sekarang, "Cerita": user_input, "Respon Admin": ""})
                    if save_api_data(API_URL_CERITA, daftar_cerita):
                        st.success("Cerita kamu berhasil terkirim!")
                        st.rerun()

    st.write("---")
    st.subheader("📜 Jejak Cerita & Tanggapan Admin")
    daftar_cerita_tampil = fetch_api_data(API_URL_CERITA)
    if not daftar_cerita_tampil:
        st.info("Belum ada cerita masuk.")
    else:
        for item in reversed(daftar_cerita_tampil):
            st.markdown(f"""
                <div class="story-card">
                    <div style="font-weight:700; color:#38BDF8; margin-bottom:5px;">👤 Anonim <span style="font-size:0.8rem; color:#94A3B8;">({item.get('Waktu', '-')})</span></div>
                    <div>{item.get('Cerita', '')}</div>
                </div>
            """, unsafe_allow_html=True)
            if item.get("Respon Admin"):
                st.markdown(f"""
                    <div class="admin-reply-card">
                        <div style="font-weight:700; color:#10B981;">👑 Tanggapan Admin:</div>
                        <div>{item.get('Respon Admin')}</div>
                    </div>
                """, unsafe_allow_html=True)

# ---------------------------------------------------------
# MENU 5: KRITIK & SARAN
# ---------------------------------------------------------
elif menu == "Kritik & Saran": 
    st.markdown('<div class="section-title">📥 Layanan Pengaduan & Konseling</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.subheader("Form Masukan & Evaluasi")
        daftar_kritik = fetch_api_data(API_URL_KRITIK)
        with st.form("kritik_form", clear_on_submit=True):
            topik = st.selectbox("Pilih Topik", ["Pelayanan/Konseling", "Konten Materi", "Tampilan Web", "Program Kerja", "Lainnya"])
            isi_kritik = st.text_area("Tulis kritik & saran kamu...", height=120)
            if st.form_submit_button("Kirim Masukan 🚀", type="primary", use_container_width=True):
                if isi_kritik.strip():
                    daftar_kritik.append({"Waktu": datetime.now().strftime("%d/%m/%Y %H:%M"), "Topik": topik, "Isi Kritik": isi_kritik})
                    if save_api_data(API_URL_KRITIK, daftar_kritik):
                        st.success("Terima kasih! Masukan kamu berhasil dikirim.")
    with c2:
        st.subheader("Konseling Privat Direct")
        if os.path.exists("genre_juara1.jpg"): st.image("genre_juara1.jpg", use_container_width=True)
        st.link_button("Hubungi Admin via WhatsApp 💬", "https://wa.me/qr/RTCENRAXQVZFM1", type="primary", use_container_width=True)

# ---------------------------------------------------------
# MENU 6: ADMIN PANEL
# ---------------------------------------------------------
elif menu == "Admin Panel":
    st.markdown('<div class="section-title">⚙️ Control Panel Admin</div>', unsafe_allow_html=True)
    col_lock, _ = st.columns([1, 2])
    with col_lock:
        admin_pass = st.text_input("Masukkan Passcode Admin", type="password")
        
    if admin_pass == "chandikia":
        st.success("🛠️ Akses Otentikasi Berhasil")
        tab_cerita, tab_materi, tab_galeri, tab_kritik, tab_analytics = st.tabs([
            "💬 Balas Cerita", "📚 Kelola Materi", "🖼️ Kelola Galeri", "📥 Lihat Kritik", "📊 Analytics Data"
        ])
        
        with tab_cerita:
            list_cerita = fetch_api_data(API_URL_CERITA)
            if list_cerita:
                opsi_cerita = [f"{i+1}. [{c.get('Waktu')}] {c.get('Cerita')[:40]}..." for i, c in enumerate(list_cerita)]
                idx_pilih = st.selectbox("Pilih cerita:", range(len(opsi_cerita)), format_func=lambda x: opsi_cerita[x])
                target = list_cerita[idx_pilih]
                st.info(f"**Cerita:** {target.get('Cerita')}")
                input_balasan = st.text_area("Tulis Respon Admin:", value=target.get("Respon Admin", ""))
                if st.button("Simpan Respon ✉️", type="primary"):
                    list_cerita[idx_pilih]["Respon Admin"] = input_balasan
                    save_api_data(API_URL_CERITA, list_cerita)
                    st.success("Respon disimpan!")
                    st.rerun()

        with tab_materi:
            aksi_materi = st.radio("Aksi:", ["Tambah Materi Baru", "Edit / Hapus Materi"], horizontal=True)
            if aksi_materi == "Tambah Materi Baru":
                j_b = st.text_input("Judul Materi")
                i_b = st.text_area("Isi Materi")
                if st.button("Publish 🚀", type="primary") and j_b and i_b:
                    st.session_state['daftar_materi'].append({"Judul": j_b, "Isi": i_b, "Foto": "None"})
                    save_api_data(API_URL_MATERI, st.session_state['daftar_materi'])
                    st.success("Ditambahkan!")
                    st.rerun()

        with tab_galeri:
            l_b = st.text_input("URL Gambar Baru")
            if st.button("Tambah Gambar 🖼️") and l_b:
                st.session_state['daftar_galeri'].append(l_b)
                save_api_data(API_URL_GALERI, st.session_state['daftar_galeri'])
                st.success("Ditambahkan!")

        with tab_kritik:
            data_k = fetch_api_data(API_URL_KRITIK)
            st.dataframe(data_k, use_container_width=True) if data_k else st.info("Kosong")

        # TAMBAHAN 3: TAB ANALYTICS UNTUK PRESENTASI JURI
        with tab_analytics:
            st.subheader("📊 Statistik Sebaran Masukan Aspirasi")
            data_k_analytics = fetch_api_data(API_URL_KRITIK)
            if data_k_analytics:
                df = pd.DataFrame(data_k_analytics)
                if 'Topik' in df.columns:
                    chart_data = df['Topik'].value_counts()
                    st.bar_chart(chart_data)
                else:
                    st.write("Data kolom Topik belum terkumpul.")
            else:
                # Mock Data Statistik jika belum ada data agar tetap kelihatan keren saat demo
                st.caption("*(Menampilkan simulasi grafik sebaran topik aspirasi)*")
                mock_df = pd.DataFrame({"Kategori": ["Pelayanan/Konseling", "Konten Materi", "Tampilan Web", "Program Kerja"], "Jumlah": [12, 8, 5, 15]})
                st.bar_chart(mock_df.set_index("Kategori"))

# FOOTER
st.markdown("<br><hr style='border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8;'>© 2026 Merpati Putih — Melangitkan Harapan, Membumikan Kebermanfaatan.</p>", unsafe_allow_html=True)

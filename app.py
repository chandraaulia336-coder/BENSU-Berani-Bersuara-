import streamlit as st
from datetime import datetime
import base64
import os
import requests

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

# 3. HELPER FUNCTIONS UNTUK DATABASE
def fetch_api_data(url):
    if not url or "script.google.com" not in url:
        return []
    try:
        res = requests.get(url, timeout=6)
        if res.status_code == 200:
            return res.json()
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

# 4. INISIALISASI SESSION STATE
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

# 6. CUSTOM CSS (MODERN DARK GLASSMORPHISM)
st.markdown(f"""
    <style>
    html {{
        scroll-behavior: smooth;
    }}
    .stApp {{
        background: linear-gradient(rgba(15, 23, 42, 0.82), rgba(15, 23, 42, 0.95)), url("{bg_image}"); 
        background-size: cover !important; 
        background-position: center !important; 
        background-attachment: fixed !important;
        color: #F8FAFC !important;
    }}
    .hero-title {{
        font-size: 3.2rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.2;
        margin-bottom: 15px;
        text-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }}
    .hero-subtitle {{
        font-size: 1.25rem;
        color: #38BDF8;
        font-weight: 600;
        margin-bottom: 20px;
        line-height: 1.5;
    }}
    .section-title {{
        font-size: 2rem;
        font-weight: 700;
        text-align: center;
        color: #FFFFFF;
        margin-top: 35px;
        margin-bottom: 25px;
        letter-spacing: -0.5px;
    }}
    .stApp p, .stApp span, .stApp label, .stApp div {{
        color: #E2E8F0 !important;
    }}
    
    /* Metrics Card */
    [data-testid="stMetricValue"] {{
        color: #38BDF8 !important;
        font-size: 2.3rem !important;
        font-weight: 800 !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: #94A3B8 !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
    }}
    div.stMetric {{
        background: rgba(30, 41, 59, 0.65) !important;
        padding: 20px 15px !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25) !important;
        text-align: center !important;
    }}

    /* Navigation Radio Bar */
    div[data-testid="stRadio"] > label {{ display: none; }}
    div[data-testid="stRadio"] > div {{
        background-color: rgba(30, 41, 59, 0.7);
        padding: 8px;
        border-radius: 14px;
        gap: 8px;
        border: 1px solid rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(8px);
    }}
    div[data-testid="stRadio"] label[data-baseweb="radio"] {{
        background-color: transparent;
        padding: 8px 18px !important;
        border-radius: 10px;
        color: #94A3B8 !important;
        font-weight: 600;
        transition: all 0.25s ease;
    }}
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {{
        background-color: #38BDF8 !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.4);
    }}
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) span {{
        color: #0F172A !important;
        font-weight: 700 !important;
    }}
    
    /* Expander & Form Cards */
    .stExpander, div[data-testid="stForm"] {{
        background-color: rgba(30, 41, 59, 0.55) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 14px !important;
        backdrop-filter: blur(8px);
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Tombol Kustom Smooth Scroll */
    .btn-merpati-putih {{
        display: inline-block;
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        color: #FFFFFF !important;
        padding: 12px 28px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.35);
        border: none;
    }}
    .btn-merpati-putih:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.5);
        color: #FFFFFF !important;
        text-decoration: none;
    }}

    /* Card Cerita / Response Box */
    .story-card {{
        background: rgba(30, 41, 59, 0.6);
        border-radius: 12px;
        padding: 16px;
        border-left: 4px solid #38BDF8;
        margin-bottom: 15px;
    }}
    .admin-reply-card {{
        background: rgba(16, 185, 129, 0.15);
        border-radius: 10px;
        padding: 12px;
        border-left: 4px solid #10B981;
        margin-top: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# 7. HEADER & TOP NAVIGATION
col_logo, col_nav = st.columns([1, 4], vertical_alignment="center")
with col_logo:
    if os.path.exists("Logo bumper (1).png"):
        st.image("Logo bumper (1).png", width=140)
    else:
        st.markdown("<h3 style='color:#FFFFFF; margin:0; font-weight:800;'>🕊️ MERPATI PUTIH</h3>", unsafe_allow_html=True)

with col_nav:
    menu = st.radio(
        "Menu Navigation", 
        ["Beranda & Galeri", "Substansi Materi", "Ruang Cerita (Anonim)", "Kritik & Saran", "Admin Panel"], 
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
        st.write("Jadilah pemuda yang aktif, harmonis, unggul, terencana, inspiratif, & hebat. Karena masa depan yang cemerlang dimulai dari perencanaan matang hari ini.")
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
    
    # Ambil data cerita aktual untuk metrik
    cerita_data = fetch_api_data(API_URL_CERITA)
    m4.metric(label="Aspirasi Masuk", value=str(len(cerita_data)))

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
        st.info("Database materi belum tersedia atau sedang disinkronkan.")

# ---------------------------------------------------------
# MENU 3: RUANG CERITA (ANONIM)
# ---------------------------------------------------------
elif menu == "Ruang Cerita (Anonim)":
    st.markdown('<div class="section-title">💬 Ruang Cerita Anonim</div>', unsafe_allow_html=True)
    
    col_info, col_form = st.columns([1, 1], gap="large")
    with col_info:
        if os.path.exists("genre_juara1.jpg"): 
            st.image("genre_juara1.jpg", caption="Duta GenRe Kecamatan Cilacap Selatan", use_container_width=True)
        st.write("Partisipasi remaja bukan hanya sekadar hadir, tapi ikut berpikir dan berani menyuarakan aspirasi. Ruang ini adalah wadah aman dan rahasia untukmu berbagi cerita.")
        
    with col_form:
        daftar_cerita = fetch_api_data(API_URL_CERITA)
        with st.form("cerita_form", clear_on_submit=True):
            user_input = st.text_area("Tuliskan cerita/curhatan kamu di sini (100% Anonim)...", height=120)
            if st.form_submit_button("Kirim Cerita 💌", type="primary", use_container_width=True):
                if user_input.strip():
                    waktu_sekarang = datetime.now().strftime("%d/%m/%Y %H:%M")
                    cerita_baru = {"Waktu": waktu_sekarang, "Cerita": user_input, "Respon Admin": ""}
                    daftar_cerita.append(cerita_baru)
                    if save_api_data(API_URL_CERITA, daftar_cerita):
                        st.success("Cerita kamu berhasil terkirim! Admin akan segera menanggapi.")
                        st.rerun()
                    else:
                        st.error("Gagal mengirim cerita ke server. Coba lagi nanti.")
                else:
                    st.warning("Mohon isi cerita terlebih dahulu.")

    st.write("---")
    st.subheader("📜 Jejak Cerita & Tanggapan Admin")
    
    daftar_cerita_tampil = fetch_api_data(API_URL_CERITA)
    if not daftar_cerita_tampil:
        st.info("Belum ada cerita yang masuk. Yuk, jadi yang pertama berbagi cerita!")
    else:
        for item in reversed(daftar_cerita_tampil):
            st.markdown(f"""
                <div class="story-card">
                    <div style="font-weight:700; color:#38BDF8; margin-bottom:5px;">👤 Anonim <span style="font-size:0.8rem; color:#94A3B8; font-weight:normal;">({item.get('Waktu', '-')})</span></div>
                    <div>{item.get('Cerita', '')}</div>
                </div>
            """, unsafe_allow_html=True)
            
            respon = item.get("Respon Admin", "").strip()
            if respon:
                st.markdown(f"""
                    <div class="admin-reply-card">
                        <div style="font-weight:700; color:#10B981; margin-bottom:3px;">👑 Tanggapan Admin:</div>
                        <div>{respon}</div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.caption("🕒 *Menunggu tanggapan admin...*")
            st.write("")

# ---------------------------------------------------------
# MENU 4: KRITIK & SARAN
# ---------------------------------------------------------
elif menu == "Kritik & Saran": 
    st.markdown('<div class="section-title">📥 Layanan Pengaduan & Konseling</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.subheader("Form Masukan & Evaluasi")
        st.write("Punya masukan konstruktif atau saran untuk pengembangan program kami? Sampaikan di sini.")
        
        daftar_kritik = fetch_api_data(API_URL_KRITIK)
        with st.form("kritik_form", clear_on_submit=True):
            topik = st.selectbox("Pilih Topik", ["Pelayanan/Konseling", "Konten Materi", "Tampilan Web", "Program Kerja", "Lainnya"])
            isi_kritik = st.text_area("Tulis kritik & saran kamu...", height=120)
            
            if st.form_submit_button("Kirim Masukan 🚀", type="primary", use_container_width=True):
                if isi_kritik.strip():
                    waktu_masuk = datetime.now().strftime("%d/%m/%Y %H:%M")
                    kritik_baru = {"Waktu": waktu_masuk, "Topik": topik, "Isi Kritik": isi_kritik}
                    daftar_kritik.append(kritik_baru)
                    if save_api_data(API_URL_KRITIK, daftar_kritik):
                        st.success("Terima kasih! Masukan kamu berhasil dikirim.")
                    else:
                        st.error("Gagal mengirim masukan.")
                else:
                    st.warning("Mohon isi pesan sebelum mengirim.")
                
    with c2:
        st.subheader("Konseling Privat Direct")
        if os.path.exists("genre_juara1.jpg"): 
            st.image("genre_juara1.jpg", use_container_width=True)
        st.write("Butuh teman bicara secara personal dan mendalam? Tim Konselor kami siap terhubung langsung via WhatsApp.")
        st.link_button("Hubungi Admin via WhatsApp 💬", "https://wa.me/qr/RTCENRAXQVZFM1", type="primary", use_container_width=True)

# ---------------------------------------------------------
# MENU 5: ADMIN PANEL
# ---------------------------------------------------------
elif menu == "Admin Panel":
    st.markdown('<div class="section-title">⚙️ Control Panel Admin</div>', unsafe_allow_html=True)
    
    col_lock, _ = st.columns([1, 2])
    with col_lock:
        admin_pass = st.text_input("Masukkan Passcode Admin", type="password")
        
    if admin_pass == "chandikia":
        st.success("🛠️ Akses Otentikasi Berhasil")
        
        tab_cerita, tab_materi, tab_galeri, tab_kritik, tab_setting = st.tabs([
            "💬 Balas Cerita", "📚 Kelola Materi", "🖼️ Kelola Galeri", "📥 Lihat Kritik", "⚙️ Pengaturan"
        ])
        
        # TAB 1: BALAS CERITA
        with tab_cerita:
            st.subheader("Balas Cerita Masuk")
            list_cerita = fetch_api_data(API_URL_CERITA)
            if list_cerita:
                opsi_cerita = [f"{i+1}. [{c.get('Waktu')}] {c.get('Cerita')[:40]}..." for i, c in enumerate(list_cerita)]
                idx_pilih = st.selectbox("Pilih cerita yang ingin dibalas / diedit balasaannya:", range(len(opsi_cerita)), format_func=lambda x: opsi_cerita[x])
                
                target_cerita = list_cerita[idx_pilih]
                st.info(f"**Cerita:** {target_cerita.get('Cerita')}")
                
                balasan_lama = target_cerita.get("Respon Admin", "")
                input_balasan = st.text_area("Tulis Respon Admin:", value=balasan_lama)
                
                if st.button("Simpan & Publis Respon ✉️", type="primary"):
                    list_cerita[idx_pilih]["Respon Admin"] = input_balasan
                    if save_api_data(API_URL_CERITA, list_cerita):
                        st.success("Respon berhasil disimpan!")
                        st.rerun()
                    else:
                        st.error("Gagal menyimpan respon.")
            else:
                st.info("Belum ada cerita masuk untuk dibalas.")

        # TAB 2: KELOLA MATERI
        with tab_materi:
            st.subheader("Manajemen Edukasi Materi")
            aksi_materi = st.radio("Pilih Tindakan:", ["Tambah Materi Baru", "Edit / Hapus Materi"], horizontal=True)
            
            if aksi_materi == "Tambah Materi Baru":
                judul_baru = st.text_input("Judul Materi Baru")
                isi_baru = st.text_area("Isi Detail Materi")
                link_f1 = st.text_input("URL Foto Utama (Opsional)")
                link_f2 = st.text_input("URL Foto 2 (Opsional)")
                
                if st.button("Publish Materi Baru 🚀", type="primary") and judul_baru and isi_baru:
                    foto_gabung = ",".join([link_f1 if link_f1 else "None", link_f2 if link_f2 else "None"])
                    st.session_state['daftar_materi'].append({"Judul": judul_baru, "Isi": isi_baru, "Foto": foto_gabung})
                    save_api_data(API_URL_MATERI, st.session_state['daftar_materi'])
                    st.success("Materi baru berhasil dipublikasikan!")
                    st.rerun()
                    
            elif aksi_materi == "Edit / Hapus Materi":
                if st.session_state['daftar_materi']:
                    opsi_materi = [m["Judul"] for m in st.session_state['daftar_materi']]
                    materi_idx = st.selectbox("Pilih Materi:", range(len(opsi_materi)), format_func=lambda x: opsi_materi[x])
                    
                    m_data = st.session_state['daftar_materi'][materi_idx]
                    edit_judul = st.text_input("Edit Judul", value=m_data.get("Judul", ""))
                    edit_isi = st.text_area("Edit Isi", value=m_data.get("Isi", ""))
                    
                    c_simpan, c_hapus = st.columns(2)
                    if c_simpan.button("Simpan Perubahan ✅"):
                        st.session_state['daftar_materi'][materi_idx]["Judul"] = edit_judul
                        st.session_state['daftar_materi'][materi_idx]["Isi"] = edit_isi
                        save_api_data(API_URL_MATERI, st.session_state['daftar_materi'])
                        st.success("Materi berhasil diperbarui!")
                        st.rerun()
                        
                    if c_hapus.button("Hapus Materi ❌"):
                        st.session_state['daftar_materi'].pop(materi_idx)
                        save_api_data(API_URL_MATERI, st.session_state['daftar_materi'])
                        st.warning("Materi telah dihapus!")
                        st.rerun()

        # TAB 3: KELOLA GALERI
        with tab_galeri:
            st.subheader("Manajemen Galeri Foto")
            link_galeri_baru = st.text_input("Masukkan URL Foto Baru (Direct Link)", placeholder="https://...")
            if st.button("Tambah ke Galeri 🖼️", type="primary") and link_galeri_baru:
                st.session_state['daftar_galeri'].append(link_galeri_baru)
                save_api_data(API_URL_GALERI, st.session_state['daftar_galeri'])
                st.success("Foto baru ditambahkan ke galeri!")
                st.rerun()
                
            if st.session_state['daftar_galeri']:
                st.write("---")
                foto_hapus = st.selectbox("Pilih foto yang ingin dihapus:", st.session_state['daftar_galeri'])
                if st.button("Hapus Foto Ini 🗑️"):
                    st.session_state['daftar_galeri'].remove(foto_hapus)
                    save_api_data(API_URL_GALERI, st.session_state['daftar_galeri'])
                    st.warning("Foto berhasil dihapus!")
                    st.rerun()

        # TAB 4: LIHAT KRITIK
        with tab_kritik:
            st.subheader("Kritik & Masukan Masuk")
            data_kritik_in = fetch_api_data(API_URL_KRITIK)
            if data_kritik_in:
                st.dataframe(data_kritik_in, use_container_width=True)
            else:
                st.info("Belum ada kritik & saran yang masuk.")

        # TAB 5: PENGATURAN
        with tab_setting:
            st.subheader("Pengaturan Tampilan Web")
            tagline_edit = st.text_input("Edit Subtitle / Tagline Hero:", value=st.session_state['tagline'])
            if st.button("Perbarui Tagline ✏️", type="primary"):
                st.session_state['tagline'] = tagline_edit
                st.success("Tagline berhasil diperbarui!")
                st.rerun()

    elif admin_pass:
        st.error("Passcode Admin Salah!")

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.markdown("<br><hr style='border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 0.9rem;'>© 2026 Merpati Putih — Melangitkan Harapan, Membumikan Kebermanfaatan.</p>", unsafe_allow_html=True)

import streamlit as st
from datetime import datetime
import base64
import os
import requests

# Konfigurasi Halaman (Lebar Penuh)
st.set_page_config(page_title="Merah Putih - Remaja Terencana", layout="wide", initial_sidebar_state="collapsed")

# ==========================================================
# PASTE MASING-MASING URL WEB APP LU DI SINI
API_URL_MATERI = "https://script.google.com/macros/s/AKfycbzbiv0Q2jZoW0lnvQ0iQjFGnPVCij_2mADOPTn-rlYxGj19nVCrjmSkAlOJnBiKDfXB/exec"
API_URL_GALERI = "https://script.google.com/macros/s/AKfycbwIJXXeB58YCeWBqOwLZ5wtLv9Se901K5FaZS5-6YBIjt-I8dtDp1bCQoHgpd_AcF4z/exec"
API_URL_CERITA = "https://script.google.com/macros/s/AKfycbzJA8fG0PmUBxjoacsCrl2BI8BBjHk1vl_oYFosjsOix8byuazakHOty6dlo5sTI5G7/exec"
API_URL_KRITIK = "https://script.google.com/macros/s/AKfycbxMSnhdLOf1RbVDMRzxuiW1ITEvGQWcMcF5dTxiTmk7HWC4M8u21CYQ_jtrOdoQOI6B/exec"
# ==========================================================

# --- FUNGSI DATABASE (Dengan Pendeteksi Error) ---
# Cache dihapus sementara biar error-nya langsung kelihatan secara real-time
def fetch_data(url, name):
    if not url.startswith("https://script.google.com"): 
        st.warning(f"URL {name} belum valid.")
        return []
    try:
        res = requests.get(url)
        if res.status_code == 200:
            try:
                return res.json()
            except ValueError:
                st.error(f"❌ Error {name}: Script Google ngga ngirim format JSON. Pastikan settingan deployment-nya 'Anyone' (Siapa Saja) dan bukan butuh login.")
                return []
        else:
            st.error(f"❌ Error {name}: Google Sheets nolak akses! Status code: {res.status_code}")
            return []
    except Exception as e: 
        st.error(f"❌ Gagal narik {name}. Error sistem: {e}")
        return []

def save_data(url, data_list):
    if url.startswith("https://script.google.com"):
        try: 
            res = requests.post(url, json={"data": data_list})
            if res.status_code != 200:
                st.error(f"❌ Gagal nyimpen data {url[-10:]}! Google nolak dengan kode: {res.status_code}")
        except Exception as e: 
            st.error(f"❌ Gagal ngirim data ke Sheets: {e}")

# --- INISIALISASI SESSION STATE ---
if 'daftar_materi' not in st.session_state: st.session_state['daftar_materi'] = fetch_data(API_URL_MATERI, "Materi")
if 'daftar_galeri' not in st.session_state: st.session_state['daftar_galeri'] = fetch_data(API_URL_GALERI, "Galeri")
if 'tagline' not in st.session_state: st.session_state['tagline'] = "Sebuah Gerakan dari Remaja untuk Melangitkan Harapan dan Membumikan Kebermanfaatan."

# --- FUNGSI MEMBACA BACKGROUND GAMBAR LOKAL ---
def get_base64_bg(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/webp;base64,{encoded}"
    # Jika file tidak ketemu, pakai fallback url gradasi gelap estetik
    return "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2000"

# Memanggil gambar (pastikan file bernama '25117787.webp' berada satu folder dengan app.py)
bg_image = get_base64_bg("25117787.webp")

# --- CUSTOM CSS ---
st.markdown(f"""
    <style>
    /* Background dengan overlay gelap */
    .stApp {{
        background: linear-gradient(rgba(15, 23, 42, 0.75), rgba(15, 23, 42, 0.9)), url("{bg_image}"); 
        background-size: cover !important; 
        background-position: center !important; 
        background-attachment: fixed !important;
        color: #F8FAFC !important;
    }}
    
    .hero-title {{ 
        font-size: 3.5rem; 
        font-weight: 800; 
        color: #FFFFFF; 
        line-height: 1.2;
        margin-bottom: 20px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }}
    .hero-subtitle {{ 
        font-size: 1.3rem; 
        color: #38BDF8; 
        font-weight: 600;
        margin-bottom: 20px;
    }}
    .section-title {{
        font-size: 2.2rem;
        font-weight: bold;
        text-align: center;
        color: #FFFFFF;
        margin-top: 40px;
        margin-bottom: 25px;
    }}
    
    .stApp p, .stApp span, .stApp label, .stApp div {{
        color: #E2E8F0 !important;
    }}
    
    [data-testid="stMetricValue"] {{
        color: #38BDF8 !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
    }}
    [data-testid="stMetricLabel"] {{
        color: #94A3B8 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }}
    
    div.stMetric {{
        background-color: rgba(30, 41, 59, 0.7) !important;
        padding: 25px 15px !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(8px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2) !important;
        text-align: center !important;
    }}

    div[data-testid="stRadio"] > label {{ display: none; }}
    div[data-testid="stRadio"] > div {{
        background-color: rgba(30, 41, 59, 0.6);
        padding: 6px;
        border-radius: 12px;
        gap: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }}
    div[data-testid="stRadio"] label[data-baseweb="radio"] {{
        background-color: transparent;
        padding: 10px 20px !important;
        border-radius: 8px;
        color: #94A3B8 !important;
        font-weight: 600;
        transition: all 0.2s ease;
    }}
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {{
        background-color: #38BDF8 !important;
        color: #0F172A !important;
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3);
    }}
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) span {{
        color: #0F172A !important;
    }}
    
    .stExpander, div[data-testid="stForm"] {{
        background-color: rgba(30, 41, 59, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)


# --- TOP NAVIGATION BAR ---
col_logo, col_nav = st.columns([1, 3.5], vertical_alignment="center")
with col_logo:
    if os.path.exists("Logo bumper (1).png"):
        st.image("Logo bumper (1).png", width=140)
    else:
        st.markdown("<h3 style='color:#FFFFFF; margin:0;'>MERAH PUTIH</h3>", unsafe_allow_html=True)

with col_nav:
    menu = st.radio(
        "Menu Navigasi", 
        ["Home", "Ruang Program", "Ruang Cerita", "Kritik & Saran", "Admin Panel"], 
        horizontal=True
    )

st.markdown("<hr style='margin-top:5px; margin-bottom:25px; border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

# ==========================================
# MENU 1: HOME (Beranda & Galeri)
# ==========================================
if menu == "Home":
    h_col1, h_col2 = st.columns([1.2, 1], gap="large")
    
    with h_col1:
        st.markdown('<div class="hero-title">Merah Putih: Menuju Era Remaja Terencana.</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-subtitle">{st.session_state["tagline"]}</div>', unsafe_allow_html=True)
        st.write('"Jadilah pemuda yang aktif, harmonis, unggul, terencana, inspiratif, & hebat. Karena masa depan dimulai dari langkah kecil hari ini."')
        st.write("")
        st.button("Mengenal Lebih Dekat", type="primary")

    with h_col2:
        if os.path.exists("genre_juara1.jpg"):
            st.image("genre_juara1.jpg", use_container_width=True)
        else:
            st.info("Tambahkan file 'genre_juara1.jpg' untuk gambar Hero.")

    st.markdown('<div class="section-title">Merah Putih dalam Angka</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Tahun Dedikasi", value="1+")
    m2.metric(label="Remaja Terdampak", value="500+")
    m3.metric(label="Program Berjalan", value="12")
    m4.metric(label="Aspirasi Masuk", value=str(max(0, len(fetch_data(API_URL_CERITA, "Cerita")))))

    st.markdown('<div class="section-title">Peta Jejak Keberdampakan (Galeri)</div>', unsafe_allow_html=True)
    if st.session_state['daftar_galeri']:
        g_cols = st.columns(3)
        for i, url_img in enumerate(st.session_state['daftar_galeri']):
            g_cols[i % 3].image(url_img, use_container_width=True)
    else:
        st.info("Belum ada dokumentasi di galeri.")

# ==========================================
# MENU 2: RUANG PROGRAM (Substansi Materi)
# ==========================================
elif menu == "Ruang Program":
    st.markdown('<div class="section-title">Ruang Program & Edukasi</div>', unsafe_allow_html=True)
    st.write("Jelajahi berbagai modul dan materi edukasi untuk mendukung perencanaan masa depan yang lebih baik.")
    st.write("")
    
    if st.session_state['daftar_materi']:
        for m in st.session_state['daftar_materi']:
            with st.container():
                st.subheader(f"📘 {m['Judul']}")
                col_text, col_img = st.columns([2, 1])
                with col_text:
                    st.write(m["Isi"])
                with col_img:
                    if m.get("Foto") and m["Foto"] != "None":
                        foto_pertama = m["Foto"].split(",")[0].strip()
                        st.image(foto_pertama, use_container_width=True)
                st.divider()
    else: 
        st.info("Materi edukasi sedang disiapkan.")

# ==========================================
# MENU 3: RUANG CERITA (Voice of Youth)
# ==========================================
elif menu == "Ruang Cerita":
    st.markdown('<div class="section-title">Suara Remaja Berarti</div>', unsafe_allow_html=True)
    
    col_info, col_form = st.columns([1, 1], gap="large")
    with col_info:
        st.subheader("Bercerita Tanpa Batas")
        st.write("Partisipasi remaja bukan hanya hadir, tapi ikut berpikir dan menyampaikan aspirasi. Ruang ini adalah tempat aman untukmu bercerita (sepenuhnya anonim).")
        st.info("Identitasmu aman. Kami berkomitmen menjaga kerahasiaan.")
        
    with col_form:
        daftar_cerita = fetch_data(API_URL_CERITA, "Cerita")
        with st.form("cerita_form", clear_on_submit=True):
            user_input = st.text_area("Tulis aspirasi atau ceritamu di sini...")
            if st.form_submit_button("Kirim Aspirasi 🚀", type="primary") and user_input:
                waktu_sekarang = datetime.now().strftime("%d/%m/%Y %H:%M")
                cerita_baru = {"Waktu": waktu_sekarang, "Cerita": user_input, "Respon Admin": ""}
                daftar_cerita.append(cerita_baru)
                save_data(API_URL_CERITA, daftar_cerita)
                st.success("Aspirasi berhasil dikirim!")
                st.rerun()

    st.markdown("---")
    st.subheader("Jejak Aspirasi")
    if daftar_cerita:
        for item in reversed(daftar_cerita):
            with st.expander(f"🗣️ Aspirasi Anonim - {item.get('Waktu', '-')} (Klik untuk lihat respon)"):
                st.write(item.get("Cerita", ""))
                if item.get("Respon Admin", "").strip():
                    st.success(f"**Tanggapan Kami:**\n{item.get('Respon Admin')}")
                else:
                    st.caption("Belum ada tanggapan.")
    else:
        st.write("Belum ada aspirasi yang masuk.")

# ==========================================
# MENU 4: KRITIK & Saran
# ==========================================
elif menu == "Kritik & Saran":
    st.markdown('<div class="section-title">Layanan Pengaduan & Bantuan</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.subheader("Kotak Masukan")
        daftar_kritik = fetch_data(API_URL_KRITIK, "Kritik")
        with st.form("kritik_form", clear_on_submit=True):
            topik = st.selectbox("Pilih Topik", ["Pelayanan", "Konten Web", "Lainnya"])
            isi_kritik = st.text_area("Tulis masukan untuk kami...")
            if st.form_submit_button("Kirim Masukan", type="primary") and isi_kritik:
                daftar_kritik.append({"Waktu": datetime.now().strftime("%d/%m/%Y %H:%M"), "Topik": topik, "Isi Kritik": isi_kritik})
                save_data(API_URL_KRITIK, daftar_kritik)
                st.success("Terima kasih atas masukannya!")
    
    with c2:
        st.subheader("Butuh Bantuan Cepat?")
        st.write("Jika kamu butuh ngobrol langsung secara personal atau butuh bantuan segera, tim konselor kami siap membantu via WhatsApp.")
        st.write("")
        st.link_button("Hubungi Admin via WhatsApp 💬", "https://wa.me/qr/RTCENRAXQVZFM1", type="primary")

# ==========================================
# MENU 5: ADMIN PANEL
# ==========================================
elif menu == "Admin Panel":
    st.markdown('<div class="section-title">⚙️ Control Panel</div>', unsafe_allow_html=True)
    
    col_lock, _ = st.columns([1, 2])
    with col_lock:
        admin_pass = st.text_input("Masukkan Password Admin", type="password")
    
    if admin_pass == "admin123":
        st.success("Akses Diberikan!")
        tab1, tab2 = st.tabs(["Kelola Galeri", "Kelola Materi"])
        
        with tab1:
            link_baru = st.text_input("Tambah Foto Galeri (URL Gambar)")
            if st.button("Simpan Foto", type="primary"):
                st.session_state['daftar_galeri'].append(link_baru)
                save_data(API_URL_GALERI, st.session_state['daftar_galeri'])
                st.success("Berhasil ditambah!")
                st.rerun()
                
        with tab2:
            st.write("Gunakan menu ini untuk menambah materi baru.")
            j_baru = st.text_input("Judul")
            i_baru = st.text_area("Isi")
            f_baru = st.text_input("URL Gambar (Pisahkan koma jika banyak)")
            if st.button("Posting Materi", type="primary"):
                st.session_state['daftar_materi'].append({"Judul": j_baru, "Isi": i_baru, "Foto": f_baru if f_baru else "None"})
                save_data(API_URL_MATERI, st.session_state['daftar_materi'])
                st.success("Materi diposting!")
                st.rerun()
    elif admin_pass:
        st.error("Password Salah!")

# Footer 
st.markdown("<br><hr style='border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8;'>© 2026 Merah Putih - Melangitkan Harapan, Membumikan Kebermanfaatan.</p>", unsafe_allow_html=True)

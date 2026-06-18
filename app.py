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
API_URL_CERITA = "https://script.google.com/macros/s/AKfycbxVCt4UHwrkjwLmS0wdUKKIsa5k6gUB1Yq2HFR3uCQSr-WPg334yaS5f-I48y8O3nw/exec"
API_URL_KRITIK = "https://script.google.com/macros/s/AKfycbxMSnhdLOf1RbVDMRzxuiW1ITEvGQWcMcF5dTxiTmk7HWC4M8u21CYQ_jtrOdoQOI6B/exec"
# ==========================================================

# --- FUNGSI DATABASE (Sama seperti sebelumnya) ---
@st.cache_data(ttl=60)
def fetch_data(url, name):
    if not url.startswith("https://script.google.com"): return []
    try:
        res = requests.get(url)
        return res.json() if res.status_code == 200 else []
    except: return []

def save_data(url, data_list):
    if url.startswith("https://script.google.com"):
        try: requests.post(url, json={"data": data_list})
        except: pass

# --- INISIALISASI SESSION STATE ---
if 'daftar_materi' not in st.session_state: st.session_state['daftar_materi'] = fetch_data(API_URL_MATERI, "Materi")
if 'daftar_galeri' not in st.session_state: st.session_state['daftar_galeri'] = fetch_data(API_URL_GALERI, "Galeri")
if 'tagline' not in st.session_state: st.session_state['tagline'] = "Sebuah Gerakan dari Remaja untuk Melangitkan Harapan dan Membumikan Kebermanfaatan."

# --- CUSTOM CSS (Tema Terang ala Video) ---
st.markdown("""
    <style>
    /* Mengubah background jadi putih cerah */
    .stApp {
        background-color: #F8FAFC; 
        color: #1E293B;
    }
    
    /* Styling Typography */
    .hero-title { 
        font-size: 4rem; 
        font-weight: 800; 
        color: #1E3A8A; /* Biru gelap ala Senandung Asa */
        line-height: 1.2;
        margin-bottom: 20px;
    }
    .hero-subtitle { 
        font-size: 1.5rem; 
        color: #0284C7; 
        font-weight: 600;
        margin-bottom: 20px;
    }
    .section-title {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #0F172A;
        margin-top: 50px;
        margin-bottom: 30px;
    }
    
    /* Styling Kartu/Container */
    div.stMetric {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    
    /* Sembunyikan elemen bawaan Streamlit yang mengganggu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# --- TOP NAVIGATION BAR (Mengganti Sidebar) ---
col_logo, col_nav = st.columns([1, 4])
with col_logo:
    if os.path.exists("Logo bumper (1).png"):
        st.image("Logo bumper (1).png", width=150)
    else:
        st.markdown("**MERAH PUTIH**")

with col_nav:
    # Menggunakan radio horizontal sebagai top navbar
    menu = st.radio(
        "Navigasi", 
        ["Home", "Ruang Program", "Ruang Cerita", "Kritik & Saran", "Admin Panel"], 
        horizontal=True, 
        label_visibility="collapsed"
    )

st.markdown("---")

# ==========================================
# MENU 1: HOME (Beranda & Galeri)
# ==========================================
if menu == "Home":
    # HERO SECTION (Teks Kiri, Gambar Kanan)
    h_col1, h_col2 = st.columns([1.2, 1], gap="large")
    
    with h_col1:
        st.markdown('<div class="hero-title">Merah Putih: Menuju Era Remaja Terencana.</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="hero-subtitle">{st.session_state["tagline"]}</div>', unsafe_allow_html=True)
        st.write('"Jadilah pemuda yang aktif, harmonis, unggul, terencana, inspiratif, & hebat. Karena masa depan dimulai dari langkah kecil hari ini."')
        st.button("Mengenal Lebih Dekat", type="primary")

    with h_col2:
        if os.path.exists("genre_juara1.jpg"):
            st.image("genre_juara1.jpg", use_container_width=True)
        else:
            st.info("Tambahkan file 'genre_juara1.jpg' untuk gambar Hero.")

    # SECTION: ANGKA (STATISTIK)
    st.markdown('<div class="section-title">Merah Putih dalam Angka</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Tahun Dedikasi", value="1+")
    m2.metric(label="Remaja Terdampak", value="500+")
    m3.metric(label="Program Berjalan", value="12")
    m4.metric(label="Aspirasi Masuk", value=str(len(fetch_data(API_URL_CERITA, "Cerita"))))

    # SECTION: GALERI
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
    
    if st.session_state['daftar_materi']:
        for m in st.session_state['daftar_materi']:
            # Dibuat mirip kartu program
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
    
    col_info, col_form = st.columns([1, 1])
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
# MENU 4: KRITIK & SARAN
# ==========================================
elif menu == "Kritik & Saran":
    st.markdown('<div class="section-title">Layanan Pengaduan & Bantuan</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Kotak Masukan")
        daftar_kritik = fetch_data(API_URL_KRITIK, "Kritik")
        with st.form("kritik_form", clear_on_submit=True):
            topik = st.selectbox("Pilih Topik", ["Pelayanan", "Konten Web", "Lainnya"])
            isi_kritik = st.text_area("Tulis masukan untuk kami...")
            if st.form_submit_button("Kirim Masukan") and isi_kritik:
                daftar_kritik.append({"Waktu": datetime.now().strftime("%d/%m/%Y %H:%M"), "Topik": topik, "Isi Kritik": isi_kritik})
                save_data(API_URL_KRITIK, daftar_kritik)
                st.success("Terima kasih atas masukannya!")
    
    with c2:
        st.subheader("Butuh Bantuan Cepat?")
        st.write("Jika kamu butuh ngobrol langsung secara personal atau butuh bantuan segera, tim konselor kami siap membantu via WhatsApp.")
        st.link_button("Hubungi Admin via WhatsApp 💬", "https://wa.me/qr/RTCENRAXQVZFM1", type="primary")

# ==========================================
# MENU 5: ADMIN PANEL
# ==========================================
elif menu == "Admin Panel":
    st.markdown('<div class="section-title">⚙️ Control Panel</div>', unsafe_allow_html=True)
    admin_pass = st.text_input("Masukkan Password Admin", type="password")
    
    if admin_pass == "admin123":
        st.success("Akses Diberikan!")
        tab1, tab2 = st.tabs(["Kelola Galeri", "Kelola Materi"])
        
        with tab1:
            link_baru = st.text_input("Tambah Foto Galeri (URL URL)")
            if st.button("Simpan Foto"):
                st.session_state['daftar_galeri'].append(link_baru)
                save_data(API_URL_GALERI, st.session_state['daftar_galeri'])
                st.success("Berhasil ditambah!")
                st.rerun()
                
        with tab2:
            st.write("Gunakan menu ini untuk menambah materi baru.")
            j_baru = st.text_input("Judul")
            i_baru = st.text_area("Isi")
            f_baru = st.text_input("URL Gambar (Pisahkan koma jika banyak)")
            if st.button("Posting Materi"):
                st.session_state['daftar_materi'].append({"Judul": j_baru, "Isi": i_baru, "Foto": f_baru if f_baru else "None"})
                save_data(API_URL_MATERI, st.session_state['daftar_materi'])
                st.success("Materi diposting!")
                st.rerun()
    elif admin_pass:
        st.error("Password Salah!")

# Footer ala video
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748B;'>© 2026 Merah Putih - Melangitkan Harapan, Membumikan Kebermanfaatan.</p>", unsafe_allow_html=True)

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

# --- FUNGSI DATABASE MATERI ---
def fetch_materi_sheets():
    if not API_URL_MATERI.startswith("https://script.google.com/macros/s/AKfycbxVCt4UHwrkjwLmS0wdUKKIsa5k6gUB1Yq2HFR3uCQSr-WPg334yaS5f-I48y8O3nw/exec"): 
        st.warning("⚠️ URL Materi belum lu ganti di app.py dengan benar, bro!")
        return []
    try:
        res = requests.get(API_URL_MATERI)
        if res.status_code != 200:
            st.error(f"❌ Google Sheets nolak Materi! Status Code: {res.status_code}")
            return []
        return res.json()
    except Exception as e: 
        st.error(f"❌ Gagal narik data MATERI dari Sheets. Erornya: {e}")
        return []

def save_materi_sheets(data_list):
    if API_URL_MATERI.startswith("https://script.google.com"):
        try: 
            res = requests.post(API_URL_MATERI, json={"data": data_list})
            if res.status_code != 200:
                st.error(f"❌ Gagal nyimpen Materi! Sheets nolak dengan kode: {res.status_code}")
        except Exception as e: 
            st.error(f"❌ Gagal ngirim data MATERI ke Sheets. Erornya: {e}")

# --- FUNGSI DATABASE GALERI ---
def fetch_galeri_sheets():
    if not API_URL_GALERI.startswith("https://script.google.com/macros/s/AKfycbwIJXXeB58YCeWBqOwLZ5wtLv9Se901K5FaZS5-6YBIjt-I8dtDp1bCQoHgpd_AcF4z/exec"): 
        st.warning("⚠️ URL Galeri belum lu ganti di app.py dengan benar, bro!")
        return []
    try:
        res = requests.get(API_URL_GALERI)
        if res.status_code != 200:
            st.error(f"❌ Google Sheets nolak Galeri! Status Code: {res.status_code}")
            return []
        return res.json()
    except Exception as e: 
        st.error(f"❌ Gagal narik data GALERI dari Sheets. Erornya: {e}")
        return []

def save_galeri_sheets(data_list):
    if API_URL_GALERI.startswith("https://script.google.com"):
        try: 
            res = requests.post(API_URL_GALERI, json={"data": data_list})
            if res.status_code != 200:
                st.error(f"❌ Gagal nyimpen Galeri! Sheets nolak dengan kode: {res.status_code}")
        except Exception as e: 
            st.error(f"❌ Gagal ngirim data GALERI ke Sheets. Erornya: {e}")

# --- FUNGSI DATABASE RUANG CERITA ---
def fetch_cerita_sheets():
    if not API_URL_CERITA.startswith("https://script.google.com"): 
        return []
    try:
        res = requests.get(API_URL_CERITA)
        if res.status_code == 200: return res.json()
        return []
    except: return []

def save_cerita_sheets(data_list):
    if API_URL_CERITA.startswith("https://script.google.com"):
        try: requests.post(API_URL_CERITA, json={"data": data_list})
        except: pass

# --- FUNGSI DATABASE KOTAK KRITIK ---
def fetch_kritik_sheets():
    if not API_URL_KRITIK.startswith("https://script.google.com"): 
        return []
    try:
        res = requests.get(API_URL_KRITIK)
        if res.status_code == 200: return res.json()
        return []
    except: return []

def save_kritik_sheets(data_list):
    if API_URL_KRITIK.startswith("https://script.google.com"):
        try: requests.post(API_URL_KRITIK, json={"data": data_list})
        except: pass


# --- INISIALISASI SESSION STATE ---
if 'daftar_materi' not in st.session_state: st.session_state['daftar_materi'] = fetch_materi_sheets()
if 'daftar_galeri' not in st.session_state: st.session_state['daftar_galeri'] = fetch_galeri_sheets()
if 'tagline' not in st.session_state: st.session_state['tagline'] = "Sebuah Gerakan dari Remaja untuk Melangitkan Harapan dan Membumikan Kebermanfaatan."

# --- FUNGSI WALLPAPER BACKGROUND ---
def get_base64_bg(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/webp;base64,{encoded}"
    return "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=2000"

bg_image = get_base64_bg("25117787.webp")

# --- CUSTOM CSS (TAMPILAN MODERN) ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(15, 23, 42, 0.75), rgba(15, 23, 42, 0.9)), url("{bg_image}"); 
        background-size: cover !important; 
        background-position: center !important; 
        background-attachment: fixed !important;
        color: #F8FAFC !important;
    }}
    .hero-title {{ font-size: 3.5rem; font-weight: 800; color: #FFFFFF; line-height: 1.2; margin-bottom: 20px; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }}
    .hero-subtitle {{ font-size: 1.3rem; color: #38BDF8; font-weight: 600; margin-bottom: 20px; }}
    .section-title {{ font-size: 2.2rem; font-weight: bold; text-align: center; color: #FFFFFF; margin-top: 40px; margin-bottom: 25px; }}
    
    .stApp p, .stApp span, .stApp label, .stApp div {{ color: #E2E8F0 !important; }}
    
    [data-testid="stMetricValue"] {{ color: #38BDF8 !important; font-size: 2.5rem !important; font-weight: 700 !important; }}
    [data-testid="stMetricLabel"] {{ color: #94A3B8 !important; font-size: 1rem !important; font-weight: 600 !important; }}
    
    div.stMetric {{
        background-color: rgba(30, 41, 59, 0.7) !important; padding: 25px 15px !important;
        border-radius: 16px !important; border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(8px); box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2) !important; text-align: center !important;
    }}

    div[data-testid="stRadio"] > label {{ display: none; }}
    div[data-testid="stRadio"] > div {{ background-color: rgba(30, 41, 59, 0.6); padding: 6px; border-radius: 12px; gap: 10px; border: 1px solid rgba(255, 255, 255, 0.1); }}
    div[data-testid="stRadio"] label[data-baseweb="radio"] {{ background-color: transparent; padding: 10px 20px !important; border-radius: 8px; color: #94A3B8 !important; font-weight: 600; transition: all 0.2s ease; }}
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {{ background-color: #38BDF8 !important; color: #0F172A !important; box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3); }}
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) span {{ color: #0F172A !important; }}
    
    .stExpander, div[data-testid="stForm"] {{ background-color: rgba(30, 41, 59, 0.4) !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 12px !important; }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    </style>
""", unsafe_allow_html=True)

# === TOP NAVIGATION BAR ===
col_logo, col_nav = st.columns([1, 4], vertical_alignment="center")
with col_logo:
    if os.path.exists("Logo bumper (1).png"):
        st.image("Logo bumper (1).png", width=140)
    else:
        st.markdown("<h3 style='color:#FFFFFF; margin:0;'>MERAH PUTIH</h3>", unsafe_allow_html=True)

with col_nav:
    menu = st.radio(
        "Menu", 
        ["Beranda & Galeri", "Substansi Materi", "Ruang Cerita (Anonim)", "Kritik & Saran", "Admin Panel"], 
        horizontal=True
    )

st.markdown("<hr style='margin-top:5px; margin-bottom:25px; border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)

# === MENU 1: BERANDA & GALERI ===
if menu == "Beranda & Galeri":
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

    st.markdown('<div class="section-title">Merah Putih dalam Angka</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric(label="Tahun Dedikasi", value="1+")
    m2.metric(label="Remaja Terdampak", value="500+")
    m3.metric(label="Program Berjalan", value="12")
    m4.metric(label="Aspirasi Masuk", value=str(max(0, len(fetch_cerita_sheets()))))

    st.markdown('<div class="section-title">Peta Jejak Keberdampakan (Galeri)</div>', unsafe_allow_html=True)
    if st.session_state['daftar_galeri']:
        g_cols = st.columns(3)
        for i, url_img in enumerate(st.session_state['daftar_galeri']):
            g_cols[i % 3].image(url_img, use_container_width=True)
    else:
        st.info("Belum ada foto yang dipajang di galeri.")

# === MENU 2: SUBSTANSI MATERI ===
elif menu == "Substansi Materi":
    st.markdown('<div class="section-title">📚 Substansi Materi</div>', unsafe_allow_html=True)
    
    if st.session_state['daftar_materi']:
        for m in st.session_state['daftar_materi']:
            with st.expander(m["Judul"]):
                st.write(m["Isi"])
                if m.get("Foto") and m["Foto"] != "None":
                    list_foto = [url.strip() for url in m["Foto"].split(",") if url.strip() and url.strip() != "None"]
                    if list_foto:
                        st.write("---")
                        cols_foto = st.columns(len(list_foto))
                        for idx_f, url_f in enumerate(list_foto):
                            cols_foto[idx_f].image(url_f, use_container_width=True)
    else: 
        st.info("Database materi kosong atau belum dikonfigurasi.")

# === MENU 3: RUANG CERITA ===
elif menu == "Ruang Cerita (Anonim)":
    st.markdown('<div class="section-title">💬 Ruang Cerita Anonim</div>', unsafe_allow_html=True)
    
    col_info, col_form = st.columns([1, 1], gap="large")
    with col_info:
        if os.path.exists("genre_juara1.jpg"): 
            st.image("genre_juara1.jpg", caption="Duta GenRe Kecamatan Cilacap Selatan 2026", use_container_width=True)
        st.write("Partisipasi remaja bukan hanya hadir, tapi ikut berpikir dan menyampaikan aspirasi. Ruang ini adalah tempat aman untukmu bercerita.")
        
    with col_form:
        daftar_cerita = fetch_cerita_sheets()
        with st.form("cerita_form", clear_on_submit=True):
            user_input = st.text_area("Ketik cerita/curhatan lu di sini (tenang, anonim kok)...")
            if st.form_submit_button("Kirim Cerita 💌", type="primary") and user_input:
                waktu_sekarang = datetime.now().strftime("%d/%m/%Y %H:%M")
                cerita_baru = {"Waktu": waktu_sekarang, "Cerita": user_input, "Respon Admin": ""}
                daftar_cerita.append(cerita_baru)
                save_cerita_sheets(daftar_cerita)
                st.success("Cerita lu udah meluncur ke database, bre! Tunggu direspon ya.")
                st.rerun()
            
    st.write("---")
    st.subheader("📚 Jejak Cerita & Respon Admin")
    if not daftar_cerita:
        st.info("Belum ada cerita yang masuk nih. Jadi yang pertama curhat yuk!")
    else:
        for item in reversed(daftar_cerita):
            with st.container():
                st.markdown(f"**👤 Anonim** *({item.get('Waktu', '-')})*")
                st.info(item.get("Cerita", ""))
                respon = item.get("Respon Admin", "").strip()
                if respon:
                    st.success(f"**👑 Respon Admin:**\n{respon}")
                else:
                    st.caption("🕒 Belum ada respon dari admin. Sabar ya, bre!")
                st.write("")

# === MENU 4: KRITIK & SARAN ===
elif menu == "Kritik & Saran": 
    st.markdown('<div class="section-title">📥 Layanan Pengaduan & Bantuan</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.write("Punya masukan, kritik tajam, atau saran buat perkembangan kita? Tumpahin di sini, bre!")
        daftar_kritik = fetch_kritik_sheets()
        with st.form("kritik_form", clear_on_submit=True):
            topik = st.selectbox("Pilih Topik", ["Pelayanan/Konseling", "Konten Materi", "Tampilan Web", "Lainnya"])
            isi_kritik = st.text_area("Tulis kritik & saran lu di sini...")
            if st.form_submit_button("Kirim Masukan 🚀", type="primary") and isi_kritik:
                waktu_masuk = datetime.now().strftime("%d/%m/%Y %H:%M")
                kritik_baru = {"Waktu": waktu_masuk, "Topik": topik, "Isi Kritik": isi_kritik}
                daftar_kritik.append(kritik_baru)
                save_kritik_sheets(daftar_kritik)
                st.success("Tengkyu bre! Kritik & saran lu udah masuk ke meja admin.")
                
    with c2:
        st.subheader("Konseling Privat")
        if os.path.exists("genre_juara1.jpg"): 
            st.image("genre_juara1.jpg", use_container_width=True)
        st.write("Mau ngobrol langsung secara personal? Langsung terhubung ke WhatsApp Admin!")
        st.link_button("Hubungi Admin via WhatsApp 💬", "https://wa.me/qr/RTCENRAXQVZFM1", type="primary", use_container_width=True)

# === MENU 5: ADMIN PANEL ===
elif menu == "Admin Panel":
    st.markdown('<div class="section-title">⚙️ Control Panel Admin</div>', unsafe_allow_html=True)
    
    col_lock, _ = st.columns([1, 2])
    with col_lock:
        admin_pass = st.text_input("Masukkan Password Admin", type="password")
        
    if admin_pass == "admin123":
        st.success("🛠️ Akses Terbuka")
        
        # Admin Edit Tagline
        with st.expander("🛠️ Admin Panel: Edit Tagline Web"):
            tagline_baru = st.text_input("Ubah kalimat sub-header:", value=st.session_state['tagline'])
            if st.button("Update Tagline", type="primary"):
                st.session_state['tagline'] = tagline_baru
                st.success("Tagline diperbarui!")
                st.rerun()
                
        # Admin Kelola Galeri
        with st.expander("🛠️ Admin Panel: Kelola Foto Galeri"):
            st.write("🖼️ **Tambah Foto Baru:**")
            link_galeri_baru = st.text_input("Masukkan URL Gambar", placeholder="https://i.postimg.cc/...jpg")
            if st.button("Pajang di Galeri 🚀", type="primary") and link_galeri_baru:
                st.session_state['daftar_galeri'].append(link_galeri_baru)
                save_galeri_sheets(st.session_state['daftar_galeri'])
                st.success("Foto berhasil nangkring!")
                st.rerun()
            
            if st.session_state['daftar_galeri']:
                st.write("---")
                foto_hapus = st.selectbox("Pilih link foto yang mau dihapus:", st.session_state['daftar_galeri'])
                if st.button("Hapus Foto Ini ❌"):
                    st.session_state['daftar_galeri'].remove(foto_hapus)
                    save_galeri_sheets(st.session_state['daftar_galeri'])
                    st.warning("Foto dihapus!")
                    st.rerun()

        # Admin Kelola Materi
        with st.expander("🛠️ Admin Panel: Kelola & Edit Materi"):
            aksi_materi = st.radio("Pilihan Tindakan:", ["Tambah Materi Baru", "Edit / Hapus Materi Lawas"])
            if aksi_materi == "Tambah Materi Baru":
                judul_baru = st.text_input("Judul Materi Baru")
                isi_baru = st.text_area("Isi Materi Baru")
                link_f1 = st.text_input("Link Foto 1")
                link_f2 = st.text_input("Link Foto 2 (Opsional)")
                link_f3 = st.text_input("Link Foto 3 (Opsional)")
                if st.button("Posting Permanen", type="primary") and judul_baru and isi_baru:
                    foto_gabung = ",".join([link_f1 if link_f1 else "None", link_f2 if link_f2 else "None", link_f3 if link_f3 else "None"])
                    st.session_state['daftar_materi'].append({"Judul": judul_baru, "Isi": isi_baru, "Foto": foto_gabung})
                    save_materi_sheets(st.session_state['daftar_materi'])
                    st.success("Sukses disimpan!")
                    st.rerun()
            elif aksi_materi == "Edit / Hapus Materi Lawas":
                if st.session_state['daftar_materi']:
                    opsi_judul = [m["Judul"] for m in st.session_state['daftar_materi']]
                    materi_terpilih = st.selectbox("Pilih judul:", opsi_judul)
                    idx = opsi_judul.index(materi_terpilih)
                    data_lama = st.session_state['daftar_materi'][idx]
                    
                    judul_edit = st.text_input("Edit Judul", value=data_lama["Judul"])
                    isi_edit = st.text_area("Edit Isi", value=data_lama["Isi"])
                    foto_lama = data_lama["Foto"].split(",") if "," in data_lama["Foto"] else [data_lama["Foto"], "None", "None"]
                    while len(foto_lama) < 3: foto_lama.append("None")
                    
                    edit_f1 = st.text_input("Edit Link Foto 1", value=foto_lama[0] if foto_lama[0] != "None" else "")
                    edit_f2 = st.text_input("Edit Link Foto 2", value=foto_lama[1] if foto_lama[1] != "None" else "")
                    edit_f3 = st.text_input("Edit Link Foto 3", value=foto_lama[2] if foto_lama[2] != "None" else "")
                    
                    col_save, col_del = st.columns(2)
                    if col_save.button("Simpan Perubahan ✅"):
                        foto_edit_gabung = ",".join([edit_f1 if edit_f1 else "None", edit_f2 if edit_f2 else "None", edit_f3 if edit_f3 else "None"])
                        st.session_state['daftar_materi'][idx] = {"Judul": judul_edit, "Isi": isi_edit, "Foto": foto_edit_gabung}
                        save_materi_sheets(st.session_state['daftar_materi'])
                        st.success("Disimpan!")
                        st.rerun()
                    if col_del.button("Hapus Materi ❌"):
                        st.session_state['daftar_materi'].pop(idx)
                        save_materi_sheets(st.session_state['daftar_materi'])
                        st.warning("Dihapus!")
                        st.rerun()
    elif admin_pass:
        st.error("Password Salah!")

# Footer 
st.markdown("<br><hr style='border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94A3B8;'>© 2026 Merah Putih - Melangitkan Harapan, Membumikan Kebermanfaatan.</p>", unsafe_allow_html=True)

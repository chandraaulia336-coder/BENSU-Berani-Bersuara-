import streamlit as st
from datetime import datetime
import base64
import os
import requests

# Setup Halaman
st.set_page_config(page_title="Ruang Kita", page_icon="🌊", layout="wide")

# ==========================================
# PASTE URL APLIKASI WEB APPS SCRIPT LU DI SINI
API_URL = "PASTE_URL_WEB_APP_LU_DI_SINI"
# ==========================================

# Fungsi Ambil Data dari Sheets via Web App
def fetch_materi_sheets():
    if API_URL == "https://script.googleusercontent.com/macros/echo?user_content_key=AUkAhnRk7cyYISCBvywkWI8m7jb1BPPRJ_vftkbf1Cv8xird5C68dRP_PJmXheiW8Z5DiQDOAYmcuVPIhaGMyqi3_ERSR39a4gQEpTKzs_DR7ZF0w0FmQJQziKSsQe7l3hbY1mkOmxUZQtm6sVb7OOq_XZWsQCr9x1hzgQXWZ-R-0rg14SC9PzGLutaivkZeYBLp0CFgOwDLJw8JVF8rx4ujhHmMEONdroXVD26gcWGjMsTjp0Yb0yavJrgAk2VEWXTqSRWNo9tJ2Cs_0GmTMsJx2ZSzMjFBqA&lib=MfSX_BDqrwf30UxEjy7bjgCSFgaMB1syB":
        return []
    try:
        res = requests.get(API_URL)
        return res.json()
    except:
        return []

# Fungsi Simpan Semua Data ke Sheets via Web App
def save_materi_sheets(data_list):
    if API_URL != "PASTE_URL_WEB_APP_LU_DI_SINI":
        try:
            requests.post(API_URL, json={"data": data_list})
            return True
        except:
            return False
    return False

# Jalankan penarikan data sekali di awal sesi
if 'daftar_materi' not in st.session_state:
    st.session_state['daftar_materi'] = fetch_materi_sheets()

# Fungsi ngebaca foto lokal jadiin Wallpaper Background
def get_base64_bg(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/webp;base64,{encoded}"
    return "https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2000"

bg_image = get_base64_bg("25117787.webp")

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(18, 18, 18, 0.85), rgba(18, 18, 18, 0.95)), url("{bg_image}"); 
        background-size: cover; background-position: center; background-attachment: fixed; color: #ffffff;
    }}
    .header-title {{ font-size: 45px; font-weight: bold; color: #BB86FC; margin-bottom: -10px; }}
    .sub-header {{ font-size: 20px; color: #B3B3B3; }}
    .wave-container {{
        width: 100%; height: 100px;
        background: url('data:image/svg+xml;utf8,<svg viewBox="0 0 1440 320" xmlns="http://www.w3.org/2000/svg"><path fill="%23BB86FC" fill-opacity="0.3" d="M0,160L48,170.7C96,181,192,203,288,197.3C384,192,480,160,576,144C672,128,768,128,864,138.7C960,149,1056,171,1152,165.3C1248,160,1344,128,1392,112L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
        background-size: cover; background-repeat: no-repeat; margin-top: -20px; margin-bottom: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

if 'gallery' not in st.session_state: st.session_state['gallery'] = []
if 'chat_history' not in st.session_state: st.session_state['chat_history'] = []
if 'feedbacks' not in st.session_state: st.session_state['feedbacks'] = []
if 'tagline' not in st.session_state: st.session_state['tagline'] = "Tempat aman buat belajar dan cerita."

# === SIDEBAR NAVIGASI ===
st.sidebar.title("Navigasi 🧭")
menu = st.sidebar.radio("Mau ke mana?", ["Beranda & Galeri", "Substansi Materi", "Ruang Cerita (Anonim)", "Kritik & Saran"])
st.sidebar.divider()

admin_pass = st.sidebar.text_input("Punya Kode Sesi?", type="password")
is_admin = admin_pass == "admin123" 
if is_admin: st.sidebar.success("🛠️ Akses Terbuka")

# === MENU 1: BERANDA ===
if menu == "Beranda & Galeri":
    st.markdown('<div class="wave-container"></div>', unsafe_allow_html=True)
    st.markdown('<p class="header-title">Ruang Kita 🚀</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">{st.session_state["tagline"]}</p>', unsafe_allow_html=True)
    st.divider()
    st.subheader("📸 Galeri Aksi")
    if st.session_state['gallery']:
        cols = st.columns(3)
        for i, img in enumerate(st.session_state['gallery']): cols[i % 3].image(img, use_container_width=True)
    else: st.info("Belum ada foto di galeri.")

# === MENU 2: SUBSTANSI MATERI (DATABASE PERMANEN) ===
elif menu == "Substansi Materi":
    st.markdown('<div class="wave-container"></div>', unsafe_allow_html=True)
    st.title("📚 Substansi Materi")
    
    if st.session_state['daftar_materi']:
        for m in st.session_state['daftar_materi']:
            with st.expander(m["Judul"]):
                if m.get("Foto") and m["Foto"] != "None":
                    st.write(f"*(Link Foto Dokumentasi: {m['Foto']} )*")
                st.write(m["Isi"])
    else:
        st.info("Database kosong atau kamu belum setting URL Apps Script.")
            
    if is_admin:
        st.divider()
        with st.expander("🛠️ Admin Panel: Kelola & Edit Materi", expanded=True):
            aksi_materi = st.radio("Pilihan Tindakan:", ["Tambah Materi Baru", "Edit / Hapus Materi Lawas"])
            
            if aksi_materi == "Tambah Materi Baru":
                judul_baru = st.text_input("Judul Materi Baru")
                isi_baru = st.text_area("Isi Materi Baru")
                link_foto = st.text_input("Link Foto Pendukung (Opsional / Masukan URL)")
                
                if st.button("Posting Permanen"):
                    if judul_baru and isi_baru:
                        new_item = {"Judul": judul_baru, "Isi": isi_baru, "Foto": link_foto if link_foto else "None"}
                        st.session_state['daftar_materi'].append(new_item)
                        save_materi_sheets(st.session_state['daftar_materi'])
                        st.success("Sukses disimpan permanen ke Google Sheets!")
                        st.rerun()
            
            elif aksi_materi == "Edit / Hapus Materi Lawas":
                if st.session_state['daftar_materi']:
                    opsi_judul = [m["Judul"] for m in st.session_state['daftar_materi']]
                    materi_terpilih = st.selectbox("Pilih judul yang mau diubah:", opsi_judul)
                    idx = opsi_judul.index(materi_terpilih)
                    data_lama = st.session_state['daftar_materi'][idx]
                    
                    judul_edit = st.text_input("Edit Judul", value=data_lama["Judul"])
                    isi_edit = st.text_area("Edit Isi", value=data_lama["Isi"])
                    foto_edit = st.text_input("Edit Link Foto", value=data_lama["Foto"])
                    
                    col_save, col_del = st.columns(2)
                    if col_save.button("Simpan Perubahan ✅"):
                        st.session_state['daftar_materi'][idx] = {"Judul": judul_edit, "Isi": isi_edit, "Foto": foto_edit}
                        save_materi_sheets(st.session_state['daftar_materi'])
                        st.success("Perubahan disimpan permanen!")
                        st.rerun()
                        
                    if col_del.button("Hapus Materi Ini Selamanya ❌"):
                        st.session_state['daftar_materi'].pop(idx)
                        save_materi_sheets(st.session_state['daftar_materi'])
                        st.warning("Materi dihapus permanen!")
                        st.rerun()

# === MENU 3 & 4 ===
elif menu == "Ruang Cerita (Anonim)":
    st.markdown('<div class="wave-container"></div>', unsafe_allow_html=True)
    st.title("💬 Ruang Cerita")
    img_col1, img_col2, img_col3 = st.columns([1, 1.5, 1])
    with img_col2:
        if os.path.exists("genre_juara.jpg"): st.image("genre_juara.jpg", caption="Duta GenRe Kecamatan Cilacap Selatan 2026", use_container_width=True)
    
    with st.form("cerita_form", clear_on_submit=True):
        user_input = st.text_area("Ketik cerita lu di sini...")
        if st.form_submit_button("Kirim Cerita 💌") and user_input:
            st.session_state['chat_history'].append({"role": "Anonim", "text": user_input, "time": datetime.now().strftime("%H:%M")})
            st.success("Cerita terkirim!")

elif menu == "Kritik & Saran":
    st.markdown('<div class="wave-container"></div>', unsafe_allow_html=True)
    st.title("💡 Kotak Saran")
    img_col1, img_col2, img_col3 = st.columns([1, 1.5, 1])
    with img_col2:
        if os.path.exists("genre_juara.jpg"): st.image("genre_juara.jpg", use_container_width=True)
            
    with st.form("feedback_form", clear_on_submit=True):
        feedback = st.text_area("Ada masukan?")
        if st.form_submit_button("Kirim Masukan 🚀") and feedback:
            st.session_state['feedbacks'].append({"isi": feedback, "waktu": datetime.now().strftime("%d/%m/%Y %H:%M")})
            st.success("Masukan diterima!")

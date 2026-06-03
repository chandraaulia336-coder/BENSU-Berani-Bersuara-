import streamlit as st
from datetime import datetime
import base64
import os
import requests

# ==========================================================
# PASTE MASING-MASING URL WEB APP LU DI SINI
API_URL_MATERI = "https://script.google.com/macros/s/AKfycbzbiv0Q2jZoW0lnvQ0iQjFGnPVCij_2mADOPTn-rlYxGj19nVCrjmSkAlOJnBiKDfXB/exec"
API_URL_GALERI = "https://script.google.com/macros/s/AKfycbwIJXXeB58YCeWBqOwLZ5wtLv9Se901K5FaZS5-6YBIjt-I8dtDp1bCQoHgpd_AcF4z/exec"
# ==========================================================

# --- FUNGSI DATABASE MATERI (VERSI DETEKTIF EROR) ---
def fetch_materi_sheets():
    if API_URL_MATERI == "https://script.google.com/macros/s/AKfycbwk84Ns9a0COzFLhGoc8ElgkxL6phdebe3teM-Xcm9Z06l1_ihYcPN97o1eXmKZg8bF/exec": 
        st.warning("⚠️ URL Materi belum lu ganti di app.py, bro!")
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
    if API_URL_MATERI != "https://script.google.com/macros/s/AKfycbzbiv0Q2jZoW0lnvQ0iQjFGnPVCij_2mADOPTn-rlYxGj19nVCrjmSkAlOJnBiKDfXB/exec":
        try: 
            res = requests.post(API_URL_MATERI, json={"data": data_list})
            if res.status_code != 200:
                st.error(f"❌ Gagal nyimpen Materi! Sheets nolak dengan kode: {res.status_code}")
        except Exception as e: 
            st.error(f"❌ Gagal ngirim data MATERI ke Sheets. Erornya: {e}")

# --- FUNGSI DATABASE GALERI ---
def fetch_galeri_sheets():
    if API_URL_GALERI == "PASTE_URL_APPS_SCRIPT_GALERI_LU": 
        st.warning("⚠️ URL Galeri belum lu ganti di app.py, bro!")
        return []
    try:
        res = requests.get(API_URL_GALERI)
        if res.status_code != 200:
            st.error(f"❌ Google Sheets nolak! Status Code: {res.status_code}")
            return []
        return res.json()
    except Exception as e: 
        st.error(f"❌ Gagal narik data dari Sheets. Erornya: {e}")
        return []

def save_galeri_sheets(data_list):
    if API_URL_GALERI != "PASTE_URL_APPS_SCRIPT_GALERI_LU":
        try: 
            res = requests.post(API_URL_GALERI, json={"data": data_list})
            if res.status_code != 200:
                st.error(f"❌ Gagal nyimpen! Sheets nolak dengan kode: {res.status_code}")
        except Exception as e: 
            st.error(f"❌ Gagal ngirim data ke Sheets. Erornya: {e}")

API_URL_CERITA = "https://script.google.com/macros/s/AKfycbxVCt4UHwrkjwLmS0wdUKKIsa5k6gUB1Yq2HFR3uCQSr-WPg334yaS5f-I48y8O3nw/exec"

# --- FUNGSI DATABASE RUANG CERITA ---
def fetch_cerita_sheets():
    if API_URL_CERITA == "PASTE_URL_APPS_SCRIPT_CERITA_LU": 
        return []
    try:
        res = requests.get(API_URL_CERITA)
        if res.status_code == 200:
            return res.json()
        return []
    except:
        return []

def save_cerita_sheets(data_list):
    if API_URL_CERITA != "PASTE_URL_APPS_SCRIPT_CERITA_LU":
        try: 
            requests.post(API_URL_CERITA, json={"data": data_list})
        except:
            pass

API_URL_KRITIK = "https://script.google.com/macros/s/AKfycbxMSnhdLOf1RbVDMRzxuiW1ITEvGQWcMcF5dTxiTmk7HWC4M8u21CYQ_jtrOdoQOI6B/exec"

# --- FUNGSI DATABASE KOTAK KRITIK ---
def fetch_kritik_sheets():
    if API_URL_KRITIK == "https://script.google.com/macros/s/AKfycbxMSnhdLOf1RbVDMRzxuiW1ITEvGQWcMcF5dTxiTmk7HWC4M8u21CYQ_jtrOdoQOI6B/exec": 
        return []
    try:
        res = requests.get(API_URL_KRITIK)
        if res.status_code == 200: return res.json()
        return []
    except: return []

def save_kritik_sheets(data_list):
    if API_URL_KRITIK != "PASTE_URL_APPS_SCRIPT_KRITIK_LU":
        try: 
            requests.post(API_URL_KRITIK, json={"data": data_list})
        except: pass

# Ambil data dari kedua database sekali di awal sesi
if 'daftar_materi' not in st.session_state:
    st.session_state['daftar_materi'] = fetch_materi_sheets()
if 'daftar_galeri' not in st.session_state:
    st.session_state['daftar_galeri'] = fetch_galeri_sheets()

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

if 'chat_history' not in st.session_state: st.session_state['chat_history'] = []
if 'feedbacks' not in st.session_state: st.session_state['feedbacks'] = []
if 'tagline' not in st.session_state: st.session_state['tagline'] = "Tempat aman buat belajar dan cerita."

# === LOGO DI SIDEBAR ===
if os.path.exists("Logo bumper (1).jpg"):
    st.sidebar.image("Logo bumper (1).jpg", use_container_width=True)
    st.sidebar.write("")

# === SIDEBAR NAVIGASI ===
st.sidebar.title("Navigasi 🧭")
menu = st.sidebar.radio("Mau ke mana?", ["Beranda & Galeri", "Substansi Materi", "Ruang Cerita (Anonim)", "Kritik & Saran"])
st.sidebar.divider()

admin_pass = st.sidebar.text_input("Punya Kode Sesi?", type="password")
is_admin = admin_pass == "admin123" 
if is_admin: st.sidebar.success("🛠️ Akses Terbuka")

# === MENU 1: BERANDA & GALERI (DATABASE PERMANEN) ===
if menu == "Beranda & Galeri":
    
    # --- LOGO DI TENGAH HALAMAN UTAMA ---
    col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
    with col_l2:
        if os.path.exists("Logo bumper (1).jpg"):
            st.image("Logo bumper (1).jpg", use_container_width=True)

    st.markdown('<div class="wave-container"></div>', unsafe_allow_html=True)
    st.markdown('<p class="header-title">Ruang Kita 🚀</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">{st.session_state["tagline"]}</p>', unsafe_allow_html=True)
    
    if is_admin:
        with st.expander("🛠️ Admin Panel: Edit Tagline Web"):
            tagline_baru = st.text_input("Ubah kalimat sub-header:", value=st.session_state['tagline'])
            if st.button("Update Tagline"):
                st.session_state['tagline'] = tagline_baru
                st.success("Tagline diperbarui!")
                st.rerun()

    st.divider()
    st.subheader("📸 Galeri Aksi")
    
    # Menampilkan foto permanen dari Google Sheets Galeri
    if st.session_state['daftar_galeri']:
        cols = st.columns(3)
        for i, url_img in enumerate(st.session_state['daftar_galeri']):
            cols[i % 3].image(url_img, use_container_width=True)
    else:
        st.info("Belum ada foto yang dipajang di galeri.")

    if is_admin:
        st.write("")
        with st.expander("🛠️ Admin Panel: Kelola Foto Galeri", expanded=False):
            st.write("🖼️ **Tambah Foto Baru (Gunakan Direct Link Postimages):**")
            link_galeri_baru = st.text_input("Masukkan URL Gambar", placeholder="https://i.postimg.cc/...jpg")
            if st.button("Pajang di Galeri Permanen 🚀"):
                if link_galeri_baru:
                    st.session_state['daftar_galeri'].append(link_galeri_baru)
                    save_galeri_sheets(st.session_state['daftar_galeri'])
                    st.success("Foto berhasil nangkring di galeri permanen!")
                    st.rerun()
            
            if st.session_state['daftar_galeri']:
                st.write("---")
                st.write("🗑️ **Hapus Foto Lama:**")
                foto_hapus = st.selectbox("Pilih link foto yang mau diturunkan:", st.session_state['daftar_galeri'])
                if st.button("Hapus Foto Ini Selamanya ❌"):
                    st.session_state['daftar_galeri'].remove(foto_hapus)
                    save_galeri_sheets(st.session_state['daftar_galeri'])
                    st.warning("Foto berhasil dihapus dari database!")
                    st.rerun()

# === MENU 2: SUBSTANSI MATERI ===
elif menu == "Substansi Materi":
    st.markdown('<div class="wave-container"></div>', unsafe_allow_html=True)
    st.title("📚 Substansi Materi")
    
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
    else: st.info("Database materi kosong atau belum dikonfigurasi.")
            
    if is_admin:
        st.divider()
        with st.expander("🛠️ Admin Panel: Kelola & Edit Materi", expanded=True):
            aksi_materi = st.radio("Pilihan Tindakan:", ["Tambah Materi Baru", "Edit / Hapus Materi Lawas"])
            
            if aksi_materi == "Tambah Materi Baru":
                judul_baru = st.text_input("Judul Materi Baru")
                isi_baru = st.text_area("Isi Materi Baru")
                st.write("🖼️ **Link Foto Pendukung:**")
                link_f1 = st.text_input("Link Foto 1", placeholder="https://i.postimg.cc/...jpg")
                link_f2 = st.text_input("Link Foto 2 (Opsional)", placeholder="https://i.postimg.cc/...jpg")
                link_f3 = st.text_input("Link Foto 3 (Opsional)", placeholder="https://i.postimg.cc/...jpg")
                
                if st.button("Posting Permanen"):
                    if judul_baru and isi_baru:
                        foto_gabung = ",".join([link_f1 if link_f1 else "None", link_f2 if link_f2 else "None", link_f3 if link_f3 else "None"])
                        new_item = {"Judul": judul_baru, "Isi": isi_baru, "Foto": foto_gabung}
                        st.session_state['daftar_materi'].append(new_item)
                        save_materi_sheets(st.session_state['daftar_materi'])
                        st.success("Sukses disimpan permanen!")
                        st.rerun()
            
            elif aksi_materi == "Edit / Hapus Materi Lawas":
                if st.session_state['daftar_materi']:
                    opsi_judul = [m["Judul"] for m in st.session_state['daftar_materi']]
                    materi_terpilih = st.selectbox("Pilih judul yang mau diubah:", opsi_judul)
                    idx = opsi_judul.index(materi_terpilih)
                    data_lama = st.session_state['daftar_materi'][idx]
                    
                    judul_edit = st.text_input("Edit Judul", value=data_lama["Judul"])
                    isi_edit = st.text_area("Edit Isi", value=data_lama["Isi"])
                    
                    foto_lama = data_lama["Foto"].split(",") if "," in data_lama["Foto"] else [data_lama["Foto"], "None", "None"]
                    while len(foto_lama) < 3: foto_lama.append("None")
                    
                    st.write("🖼️ **Edit Link Foto:**")
                    edit_f1 = st.text_input("Link Foto 1", value=foto_lama[0] if foto_lama[0] != "None" else "")
                    edit_f2 = st.text_input("Link Foto 2", value=foto_lama[1] if foto_lama[1] != "None" else "")
                    edit_f3 = st.text_input("Link Foto 3", value=foto_lama[2] if foto_lama[2] != "None" else "")
                    
                    col_save, col_del = st.columns(2)
                    if col_save.button("Simpan Perubahan ✅"):
                        foto_edit_gabung = ",".join([edit_f1 if edit_f1 else "None", edit_f2 if edit_f2 else "None", edit_f3 if edit_f3 else "None"])
                        st.session_state['daftar_materi'][idx] = {"Judul": judul_edit, "Isi": isi_edit, "Foto": foto_edit_gabung}
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
        if os.path.exists("genre_juara1.jpg"): 
            st.image("genre_juara1.jpg", caption="Duta GenRe Kecamatan Cilacap Selatan 2026", use_container_width=True)
    
    # 1. Ambil semua data cerita lama dari Google Sheets
    daftar_cerita = fetch_cerita_sheets()
    
    # Form input cerita baru
    with st.form("cerita_form", clear_on_submit=True):
        user_input = st.text_area("Ketik cerita/curhatan lu di sini (tenang, anonim kok)...")
        if st.form_submit_button("Kirim Cerita 💌") and user_input:
            waktu_sekarang = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            # Bikin struktur data baru (Respon Admin dikosongin dulu)
            cerita_baru = {
                "Waktu": waktu_sekarang, 
                "Cerita": user_input, 
                "Respon Admin": ""
            }
            
            # Gabungin data baru ke list lama, lalu push ke Sheets
            daftar_cerita.append(cerita_baru)
            save_cerita_sheets(daftar_cerita)
            
            st.success("Cerita lu udah meluncur ke database admin, bre! Tunggu direspon ya.")
            st.rerun() # Paksa refresh biar langsung muncul di bawah
            
    st.write("---")
    st.subheader("📚 Jejak Cerita & Respon Admin")
    
    # 2. Tampilkan semua cerita beserta respon dari admin
    if not daftar_cerita:
        st.info("Belum ada cerita yang masuk nih. Jadi yang pertama curhat yuk!")
    else:
        # Tampilkan dari yang paling baru (dibalik urutannya)
        for item in reversed(daftar_cerita):
            with st.container():
                st.markdown(f"**👤 Anonim** *({item.get('Waktu', '-')})*")
                st.info(item.get("Cerita", ""))
                
                # Ngecek apakah kolom 'Respon Admin' di Google Sheets udah diisi atau belum
                respon = item.get("Respon Admin", "").strip()
                if respon:
                    st.markdown("**👑 Respon Admin:**")
                    st.success(respon)
                else:
                    st.markdown("*🕒 Belum ada respon dari admin. Sabar ya, bre!*")
                st.write("")

elif menu == "Kritik & Saran": 
    st.markdown('<div class="wave-container"></div>', unsafe_allow_html=True)
    st.title("📥 Kotak Kritik & Saran")
    
    # --- FOTO DUTA GENRE ---
    img_col1, img_col2, img_col3 = st.columns([1, 1.5, 1])
    with img_col2:
        if os.path.exists("genre_juara1.jpg"): 
            st.image("genre_juara1.jpg", caption="Duta GenRe Kecamatan Cilacap Selatan 2026", use_container_width=True)
            
    st.write("Punya masukan, kritik tajam, atau saran buat perkembangan kita? Tumpahin di sini, bre. Identitas lu aman kok!")
    
    # Ambil data kritik lama dulu biar gak ketimpa zonk
    daftar_kritik = fetch_kritik_sheets()
    
    with st.form("kritik_form", clear_on_submit=True):
        topik = st.selectbox("Pilih Topik", ["Pelayanan/Konseling", "Konten Materi", "Tampilan Web", "Lainnya"])
        isi_kritik = st.text_area("Tulis kritik & saran lu di sini...")
        
        if st.form_submit_button("Kirim Masukan 🚀") and isi_kritik:
            waktu_masuk = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            # Susun data kritik baru
            kritik_baru = {
                "Waktu": waktu_masuk,
                "Topik": topik,
                "Isi Kritik": isi_kritik
            }
            
            # Gabungin terus kirim ke Sheets
            daftar_kritik.append(kritik_baru)
            save_kritik_sheets(daftar_kritik)
            
            st.success("Tengkyu bre! Kritik & saran lu udah masuk ke meja admin buat bahan evaluasi. 🔥")

    # ====================================================================
    # --- TOMBOL CONTACT PERSON (CHAT LANGSUNG) ---
    # ====================================================================
    st.write("---")
    st.subheader("📞 Layanan Pengaduan & Konseling Privat")
    st.write("Mau konseling lebih mendalam, butuh bantuan cepat, atau pengen ngobrol langsung secara personal? Langsung klik tombol di bawah ini buat terhubung ke WhatsApp Admin, bre!")
    
    # Tombol interaktif langsung nge-link ke WA lu
    st.link_button("Hubungi Admin via WhatsApp 💬", "https://wa.me/qr/RTCENRAXQVZFM1", use_container_width=True)

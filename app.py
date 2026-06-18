import streamlit as st
from datetime import datetime
import base64
import os
import requests

# Set Page Config ke Wide agar layout card dan kolom terlihat rapi
st.set_page_config(page_title="Merah Putih Web", layout="wide")

# ==========================================================
# PASTE MASING-MASING URL WEB APP LU DI SINI
API_URL_MATERI = "https://script.google.com/macros/s/AKfycbzbiv0Q2jZoW0lnvQ0iQjFGnPVCij_2mADOPTn-rlYxGj19nVCrjmSkAlOJnBiKDfXB/exec"
API_URL_GALERI = "https://script.google.com/macros/s/AKfycbwIJXXeB58YCeWBqOwLZ5wtLv9Se901K5FaZS5-6YBIjt-I8dtDp1bCQoHgpd_AcF4z/exec"
API_URL_CERITA = "https://script.google.com/macros/s/AKfycbxVCt4UHwrkjwLmS0wdUKKIsa5k6gUB1Yq2HFR3uCQSr-WPg334yaS5f-I48y8O3nw/exec"
API_URL_KRITIK = "https://script.google.com/macros/s/AKfycbxMSnhdLOf1RbVDMRzxuiW1ITEvGQWcMcF5dTxiTmk7HWC4M8u21CYQ_jtrOdoQOI6B/exec"
# ==========================================================

# --- FUNGSI DATABASE MATERI ---
def fetch_materi_sheets():
    if not API_URL_MATERI.startswith("https://script.google.com"): 
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
    if not API_URL_GALERI.startswith("https://script.google.com"): 
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
if 'daftar_materi' not in st.session_state:
    st.session_state['daftar_materi'] = fetch_materi_sheets()
if 'daftar_galeri' not in st.session_state:
    st.session_state['daftar_galeri'] = fetch_galeri_sheets()

# --- STYLE UTAMA MENIRU SENANDUNG ASA (LIGHT THEME & MODERN APP VIBES) ---
st.markdown("""
    <style>
    /* Mengubah background utama menjadi gradasi lembut (Light Theme) */
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #ffffff 50%, #f0fdf4 100%);
        color: #1e293b;
        font-family: 'Inter', sans-serif;
    }
    
    /* Tombol Navigasi Sidebar Bulat */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Tag Kapsul Bulat di Atas Judul */
    .kapsul-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #e0f2fe;
        color: #0369a1;
        font-size: 13px;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 50px;
        margin-bottom: 15px;
    }
    .kapsul-dot {
        width: 8px;
        height: 8px;
        background-color: #0ea5e9;
        border-radius: 50%;
        display: inline-block;
    }
    
    /* Desain Judul Utama (Hero Title) */
    .hero-title {
        font-size: 42px;
        font-weight: 800;
        color: #0f172a;
        line-height: 1.2;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        font-size: 16px;
        color: #475569;
        line-height: 1.6;
        margin-bottom: 25px;
    }
    
    /* Kartu Statistik Biru Kontras (Stats Cards) */
    .stats-card {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
        color: white;
        padding: 24px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.15);
        margin-bottom: 15px;
        text-align: left;
    }
    .stats-number {
        font-size: 38px;
        font-weight: 900;
        margin-bottom: 2px;
    }
    .stats-label {
        font-size: 14px;
        font-weight: 500;
        opacity: 0.9;
    }
    
    /* Menghilangkan border bawaan streamlit pada widget tertentu agar senada */
    div[data-testid="stExpander"] {
        background-color: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 16px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }
    
    /* Override warna judul Streamlit standar agar konsisten gelap */
    h1, h2, h3, h4 {
        color: #0f172a !important;
        font-weight: 700 !important;
    }
    </style>
""", unsafe_allow_html=True)

if 'chat_history' not in st.session_state: st.session_state['chat_history'] = []
if 'feedbacks' not in st.session_state: st.session_state['feedbacks'] = []
if 'tagline' not in st.session_state: st.session_state['tagline'] = "Sebuah Gerakan dari Kecamatan Cilacap Selatan untuk #MelangitkanHarapan, #MembumikanKebermanfaatan."

# === LOGO DI SIDEBAR ===
if os.path.exists("Logo bumper (1).png"):
    st.sidebar.image("Logo bumper (1).png", width=180)
    st.sidebar.write("")

# === SIDEBAR NAVIGASI ===
st.sidebar.title("Navigasi 🧭")
menu = st.sidebar.radio("Mau ke mana?", ["Beranda & Galeri", "Substansi Materi", "Ruang Cerita (Anonim)", "Kritik & Saran"])
st.sidebar.divider()

admin_pass = st.sidebar.text_input("Punya Kode Sesi?", type="password")
is_admin = admin_pass == "admin123" 
if is_admin: st.sidebar.success("🛠️ Akses Terbuka")

# === MENU 1: BERANDA & GALERI ===
if menu == "Beranda & Galeri":
    
    # LOGO HALAMAN UTAMA (TENGAH ATAS)
    if os.path.exists("Logo bumper (1).png"):
        col1, col2, col3 = st.columns([1, 1.2, 1])
        with col2:
            st.image("Logo bumper (1).png", use_container_width=True)

    st.write("")
    
    # HERO SECTION GAYA MERAH PUTIH / CILACAP SELATAN
    st.markdown("""
        <div class="kapsul-tag">
            <span class="kapsul-dot"></span> Kecamatan Cilacap Selatan
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="hero-title">Merah Putih: <br><span style="color: #0ea5e9;">Seruan Remaja</span> untuk Masa Depan Terencana.</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="hero-subtitle">{st.session_state["tagline"]}</p>', unsafe_allow_html=True)
    
    # Tombol Aksi Utama
    col_btn1, col_btn2 = st.columns([1.5, 4])
    with col_btn1:
        st.link_button("Meningkatkan Harapan 🚀", "https://wa.me/qr/RTCENRAXQVZFM1", use_container_width=True)
        
    if is_admin:
        with st.expander("🛠️ Admin Panel: Edit Tagline Web"):
            tagline_baru = st.text_input("Ubah kalimat sub-header:", value=st.session_state['tagline'])
            if st.button("Update Tagline"):
                st.session_state['tagline'] = tagline_baru
                st.success("Tagline diperbarui!")
                st.rerun()

    st.divider()
    
    # STATS SECTION (Merah Putih Dalam Angka)
    st.markdown('<p style="font-size: 24px; font-weight: 700; color: #0f172a; margin-bottom: 20px;">Merah Putih dalam Angka</p>', unsafe_allow_html=True)
    
    col_stat1, col_stat2, col_stat3 = st.columns([1, 1, 1])
    with col_stat1:
        st.markdown("""
            <div class="stats-card">
                <div class="stats-number">3+</div>
                <div class="stats-label">Tahun Dedikasi Konsisten</div>
            </div>
        """, unsafe_allow_html=True)
    with col_stat2:
        st.markdown("""
            <div class="stats-card" style="background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);">
                <div class="stats-number">17.000+</div>
                <div class="stats-label">Terdampak Tatap Muka</div>
            </div>
        """, unsafe_allow_html=True)
    with col_stat3:
        st.markdown("""
            <div class="stats-card" style="background: linear-gradient(135deg, #059669 0%, #047857 100%);">
                <div class="stats-number">100%</div>
                <div class="stats-label">Aksi Sosial Berkelanjutan</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.divider()
    st.subheader("📸 Galeri Aksi")
    
    if st.session_state['daftar_galeri']:
        cols = st.columns(3)
        for i, url_img in enumerate(st.session_state['daftar_galeri']):
            cols[i % 3].image(url_img, use_container_width=True)
    else:
        st.info("Belum ada foto yang dipajang di galeri.")

    if is_admin:
        st.write("")
        with st.expander("🛠️ Admin Panel: Kelola Foto Galeri", expanded=False):
            st.write("🖼️ **Tambah Foto Baru:**")
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
    st.title("📚 Substansi Materi")
    st.markdown("<p style='color: #475569;'>Pelajari berbagai infografis dan substansi edukasi di bawah ini.</p>", unsafe_allow_html=True)
    st.write("")
    
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

# === MENU 3: RUANG CERITA ===
elif menu == "Ruang Cerita (Anonim)":
    st.title("💬 Ruang Cerita")
    st.markdown("<p style='color: #475569;'>Tempat aman untuk mencurahkan isi hati secara anonim.</p>", unsafe_allow_html=True)
    
    img_col1, img_col2, img_col3 = st.columns([1, 1.2, 1])
    with img_col2:
        if os.path.exists("genre_juara1.jpg"): 
            st.image("genre_juara1.jpg", caption="Duta GenRe Kecamatan Cilacap Selatan 2026", use_container_width=True)
    
    daftar_cerita = fetch_cerita_sheets()
    
    with st.form("cerita_form", clear_on_submit=True):
        user_input = st.text_area("Ketik cerita/curhatan lu di sini (tenang, anonim kok)...")
        if st.form_submit_button("Kirim Cerita 💌") and user_input:
            waktu_sekarang = datetime.now().strftime("%d/%m/%Y %H:%M")
            cerita_baru = {"Waktu": waktu_sekarang, "Cerita": user_input, "Respon Admin": ""}
            daftar_cerita.append(cerita_baru)
            save_cerita_sheets(daftar_cerita)
            st.success("Cerita lu udah meluncur ke database admin, bre! Tunggu direspon ya.")
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
                    st.markdown("**👑 Respon Admin:**")
                    st.success(respon)
                else:
                    st.markdown("*🕒 Belum ada respon dari admin. Sabar ya, bre!*")
                st.write("")

# === MENU 4: KRITIK & SARAN ===
elif menu == "Kritik & Saran": 
    st.title("📥 Kotak Kritik & Saran")
    
    img_col1, img_col2, img_col3 = st.columns([1, 1.2, 1])
    with img_col2:
        if os.path.exists("genre_juara1.jpg"): 
            st.image("genre_juara1.jpg", caption="Duta GenRe Kecamatan Cilacap Selatan 2026", use_container_width=True)
            
    st.markdown("<p style='color: #475569;'>Punya masukan, kritik tajam, atau saran buat perkembangan kita? Tumpahin di sini, bre. Identitas lu aman kok!</p>", unsafe_allow_html=True)
    
    daftar_kritik = fetch_kritik_sheets()
    
    with st.form("kritik_form", clear_on_submit=True):
        topik = st.selectbox("Pilih Topik", ["Pelayanan/Konseling", "Konten Materi", "Tampilan Web", "Lainnya"])
        isi_kritik = st.text_area("Tulis kritik & saran lu di sini...")
        
        if st.form_submit_button("Kirim Masukan 🚀") and isi_kritik:
            waktu_masuk = datetime.now().strftime("%d/%m/%Y %H:%M")
            kritik_baru = {"Waktu": waktu_masuk, "Topik": topik, "Isi Kritik": isi_kritik}
            daftar_kritik.append(kritik_baru)
            save_kritik_sheets(daftar_kritik)
            st.success("Tengkyu bre! Kritik & saran lu udah masuk ke meja admin buat bahan evaluasi. 🔥")

    st.write("---")
    st.subheader("📞 Layanan Pengaduan & Konseling Privat")
    st.write("Mau konseling lebih mendalam, butuh bantuan cepat, atau pengen ngobrol langsung secara personal? Langsung klik tombol di bawah ini buat terhubung ke WhatsApp Admin, bre!")
    st.link_button("Hubungi Admin via WhatsApp 💬", "https://wa.me/qr/RTCENRAXQVZFM1", use_container_width=True)

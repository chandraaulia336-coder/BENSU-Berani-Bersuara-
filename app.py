import streamlit as st
from datetime import datetime
import base64
import os

# Setup Halaman
st.set_page_config(page_title="Ruang Kita", page_icon="🌊", layout="wide")

# Fungsi buat ngebaca foto lokal jadiin Wallpaper Background
def get_base64_bg(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/webp;base64,{encoded}"
    return "https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2000"

# Membaca file gambar wallpaper Tugu
bg_image = get_base64_bg("25117787.webp")

# CSS buat styling Wallpaper, Overlay, dan Elemen Ombak
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(18, 18, 18, 0.85), rgba(18, 18, 18, 0.95)), 
                    url("{bg_image}"); 
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #ffffff;
    }}
    .header-title {{
        font-size: 45px;
        font-weight: bold;
        color: #BB86FC;
        margin-bottom: -10px;
    }}
    .sub-header {{
        font-size: 20px;
        color: #B3B3B3;
    }}
    .wave-container {{
        width: 100%;
        height: 100px;
        background: url('data:image/svg+xml;utf8,<svg viewBox="0 0 1440 320" xmlns="http://www.w3.org/2000/svg"><path fill="%23BB86FC" fill-opacity="0.3" d="M0,160L48,170.7C96,181,192,203,288,197.3C384,192,480,160,576,144C672,128,768,128,864,138.7C960,149,1056,171,1152,165.3C1248,160,1344,128,1392,112L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
        background-size: cover;
        background-repeat: no-repeat;
        margin-top: -20px;
        margin-bottom: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# State nyimpen data sementara
if 'gallery' not in st.session_state:
    st.session_state['gallery'] = []
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'feedbacks' not in st.session_state:
    st.session_state['feedbacks'] = []
if 'tagline' not in st.session_state:
    st.session_state['tagline'] = "Tempat aman buat belajar dan cerita."
if 'materi' not in st.session_state:
    st.session_state['materi'] = [
        {
            "judul": "🚫 Triad KRR", 
            "isi": "- **Pernikahan Dini:** Masa muda tuh buat eksplor, bukan buru-buru nikah.\n- **Seks Bebas:** Jaga diri, jaga masa depan.\n- **NAPZA:** Narkoba cuma ngasih happy palsu yang ngerusak otak.",
            "foto": None
        },
        {
            "judul": "⏳ Pendewasaan Usia Perkawinan (PUP)", 
            "isi": "Idealnya, cewek nikah umur 21 dan cowok umur 25. Kenapa? Biar mental, fisik, sama finansial udah sama-sama mateng.",
            "foto": None
        }
    ]

# === SIDEBAR NAVIGASI ===
st.sidebar.title("Navigasi 🧭")
menu = st.sidebar.radio("Mau ke mana?", ["Beranda & Galeri", "Substansi Materi", "Ruang Cerita (Anonim)", "Kritik & Saran"])

st.sidebar.divider()

# === JALUR RAHASIA ADMIN ===
admin_pass = st.sidebar.text_input("Punya Kode Sesi?", type="password", help="Kosongkan jika tidak ada")
is_admin = admin_pass == "admin123" 

if is_admin:
    st.sidebar.success("🛠️ Akses Terbuka")

# === MENU 1: BERANDA & GALERI ===
if menu == "Beranda & Galeri":
    st.markdown('<div class="wave-container"></div>', unsafe_allow_html=True)
    st.markdown('<p class="header-title">Ruang Kita 🚀</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">{st.session_state["tagline"]}</p>', unsafe_allow_html=True)
    
    if is_admin:
        with st.expander("🛠️ Admin Panel: Edit Tagline Web", expanded=False):
            tagline_baru = st.text_input("Ubah kalimat sub-header/tagline web:", value=st.session_state['tagline'])
            if st.button("Update Tagline"):
                st.session_state['tagline'] = tagline_baru
                st.success("Tagline berhasil diperbarui!")
                st.rerun()

    st.divider()
    st.subheader("📸 Galeri Aksi")
    
    if st.session_state['gallery']:
        cols = st.columns(3)
        for i, img in enumerate(st.session_state['gallery']):
            cols[i % 3].image(img, use_container_width=True)
    else:
        st.info("Belum ada foto yang di-upload nih.")

    if is_admin:
        with st.expander("🛠️ Admin Panel: Upload Foto Baru ke Galeri", expanded=False):
            uploaded_file = st.file_uploader("Pilih foto dokumentasi...", type=['png', 'jpg', 'jpeg'])
            if st.button("Upload ke Galeri") and uploaded_file is not None:
                st.session_state['gallery'].append(uploaded_file)
                st.success("Mantap, foto berhasil mejeng di galeri!")
                st.rerun()

# === MENU 2: SUBSTANSI MATERI ===
elif menu == "Substansi Materi":
    st.markdown('<div class="wave-container"></div>', unsafe_allow_html=True)
    st.title("📚 Substansi Materi")
    st.write("Materi asik yang nggak ngebosenin buat bekal masa depan lu.")
    
    for m in st.session_state['materi']:
        with st.expander(m["judul"]):
            if m.get("foto") is not None:
                st.image(m["foto"], use_container_width=True)
            st.write(m["isi"])
            
    if is_admin:
        st.divider()
        with st.expander("🛠️ Admin Panel: Kelola & Edit Materi", expanded=True):
            aksi_materi = st.radio("Pilih Tindakan:", ["Tambah Materi Baru", "Edit / Update Materi Lawas"])
            
            if aksi_materi == "Tambah Materi Baru":
                judul_baru = st.text_input("Judul Materi Baru")
                isi_baru = st.text_area("Isi Materi Baru", height=120)
                foto_baru = st.file_uploader("Upload Foto Pendukung Materi (Opsional)", type=['png', 'jpg', 'jpeg'], key="add_foto")
                if st.button("Posting Materi"):
                    if judul_baru and isi_baru:
                        st.session_state['materi'].append({"judul": judul_baru, "isi": isi_baru, "foto": foto_baru})
                        st.success("Materi baru berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.warning("Judul dan isi materi wajib diisi!")
            
            elif aksi_materi == "Edit / Update Materi Lawas":
                if st.session_state['materi']:
                    opsi_materi = [m["judul"] for m in st.session_state['materi']]
                    materi_terpilih = st.selectbox("Pilih materi yang mau di-update:", opsi_materi)
                    
                    idx = opsi_materi.index(materi_terpilih)
                    data_lama = st.session_state['materi'][idx]
                    
                    judul_edit = st.text_input("Edit Judul", value=data_lama["judul"])
                    isi_edit = st.text_area("Edit Isi Materi", value=data_lama["isi"], height=150)
                    foto_edit = st.file_uploader("Ganti / Tambah Foto Materi", type=['png', 'jpg', 'jpeg'], key="edit_foto")
                    
                    col_save, col_del = st.columns(2)
                    if col_save.button("Simpan Perubahan ✅"):
                        st.session_state['materi'][idx]["judul"] = judul_edit
                        st.session_state['materi'][idx]["isi"] = isi_edit
                        if foto_edit is not None:
                            st.session_state['materi'][idx]["foto"] = foto_edit
                        st.success("Materi sukses diperbarui!")
                        st.rerun()
                        
                    if col_del.button("Hapus Materi Ini ❌"):
                        st.session_state['materi'].pop(idx)
                        st.warning("Materi berhasil dihapus dari daftar.")
                        st.rerun()
                else:
                    st.info("Belum ada materi buat diedit.")

# === MENU 3: RUANG CERITA (ADA FOTO BARU) ===
elif menu == "Ruang Cerita (Anonim)":
    st.markdown('<div class="wave-container"></div>', unsafe_allow_html=True)
    st.title("💬 Ruang Cerita")
    st.write("Ada beban pikiran? Ceritain aja di sini. 100% anonim, privasi lu aman.")
    
    # Nampilin foto Duta GenRe biar halaman lebih menarik & terpercaya
    img_col1, img_col2, img_col3 = st.columns([1, 1.5, 1])
    with img_col2:
        if os.path.exists("genre_juara.jpg"):
            st.image("genre_juara.jpg", caption="Duta GenRe Kecamatan Cilacap Selatan 2026", use_container_width=True)
    
    with st.form("cerita_form", clear_on_submit=True):
        user_input = st.text_area("Ketik cerita lu di sini...", height=150, placeholder="Gue ngerasa cape banget...")
        if st.form_submit_button("Kirim Cerita 💌") and user_input:
            st.session_state['chat_history'].append({"role": "Anonim", "text": user_input, "time": datetime.now().strftime("%H:%M")})
            st.success("Cerita lu udah kekirim! Tunggu respon dari kita ya.")
            
    st.divider()
    st.subheader("Papan Obrolan")
    
    for chat in st.session_state['chat_history']:
        with st.chat_message("user" if chat["role"] == "Anonim" else "assistant"):
            st.write(f"**{chat['role']}** ({chat['time']})")
            st.write(chat["text"])
            
    if is_admin:
        with st.expander("🛠️ Admin Panel: Balas Cerita", expanded=True):
            admin_balasan = st.text_input("Ketik balasan/solusi dari lu...")
            if st.button("Kirim Balasan"):
                st.session_state['chat_history'].append({"role": "Admin", "text": admin_balasan, "time": datetime.now().strftime("%H:%M")})
                st.rerun()

# === MENU 4: KRITIK & SARAN (ADA FOTO BARU) ===
elif menu == "Kritik & Saran":
    st.markdown('<div class="wave-container"></div>', unsafe_allow_html=True)
    st.title("💡 Kotak Saran")
    st.write("Bantu kita bikin web ini makin asik dan nyaman buat lu semua.")
    
    # Nampilin foto Duta GenRe di menu saran juga
    img_col1, img_col2, img_col3 = st.columns([1, 1.5, 1])
    with img_col2:
        if os.path.exists("genre_juara.jpg"):
            st.image("genre_juara.jpg", caption="Yuk sampaikan kritik & saran terbaikmu!", use_container_width=True)
            
    with st.form("feedback_form", clear_on_submit=True):
        feedback = st.text_area("Ada masukan, ide, atau nemu bug? Tulis di sini...", height=100)
        if st.form_submit_button("Kirim Masukan 🚀") and feedback:
            st.session_state['feedbacks'].append({"isi": feedback, "waktu": datetime.now().strftime("%d/%m/%Y %H:%M")})
            st.success("Tengkyu banget masukannya! Bakal kita baca buat perbaikan ke depannya.")

    if is_admin:
        st.divider()
        st.subheader("🛠️ Admin Panel: Daftar Masukan")
        if st.session_state['feedbacks']:
            for idx, fb in enumerate(st.session_state['feedbacks']):
                st.info(f"**[{fb['waktu']}]** {fb['isi']}")
        else:
            st.write("Belum ada masukan nih.")

import streamlit as st
from datetime import datetime

# Setup Halaman
st.set_page_config(page_title="Ruang Kita", page_icon="🌊", layout="wide")

# CSS buat styling Wallpaper, Overlay, dan Elemen Ombak
# PERHATIAN: Ganti tulisan 'LINK_FOTO_ATAU_FILE_LU.jpg' di bawah dengan link foto lu
st.markdown("""
    <style>
    .stApp {
        /* Ini buat background fotonya. Dikasih overlay gelap biar teks tetep kebaca jelas */
        background: linear-gradient(rgba(18, 18, 18, 0.85), rgba(18, 18, 18, 0.95)), 
                    url('https://images.unsplash.com/photo-1557683316-973673baf926?q=80&w=2000'); /* Ganti URL ini pake foto lu */
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #ffffff;
    }
    .header-title {
        font-size: 45px;
        font-weight: bold;
        color: #BB86FC;
        margin-bottom: -10px;
    }
    .sub-header {
        font-size: 20px;
        color: #B3B3B3;
    }
    /* Elemen Animasi Ombak (Wave) */
    .wave-container {
        width: 100%;
        height: 100px;
        background: url('data:image/svg+xml;utf8,<svg viewBox="0 0 1440 320" xmlns="http://www.w3.org/2000/svg"><path fill="%23BB86FC" fill-opacity="0.3" d="M0,160L48,170.7C96,181,192,203,288,197.3C384,192,480,160,576,144C672,128,768,128,864,138.7C960,149,1056,171,1152,165.3C1248,160,1344,128,1392,112L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
        background-size: cover;
        background-repeat: no-repeat;
        margin-top: -20px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# State nyimpen data sementara (Gallery, Chat, Feedback, Materi)
if 'gallery' not in st.session_state:
    st.session_state['gallery'] = []
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'feedbacks' not in st.session_state:
    st.session_state['feedbacks'] = []
if 'materi' not in st.session_state:
    # Materi bawaan awal
    st.session_state['materi'] = [
        {"judul": "🚫 Triad KRR", "isi": "- **Pernikahan Dini:** Masa muda tuh buat eksplor, bukan buru-buru nikah.\n- **Seks Bebas:** Jaga diri, jaga masa depan.\n- **NAPZA:** Narkoba cuma ngasih happy palsu yang ngerusak otak."},
        {"judul": "⏳ Pendewasaan Usia Perkawinan (PUP)", "isi": "Idealnya, cewek nikah umur 21 dan cowok umur 25. Kenapa? Biar mental, fisik, sama finansial udah sama-sama mateng."}
    ]

# === SIDEBAR (Akses Admin Paling Atas Biar Keliatan) ===
st.sidebar.markdown("### 👑 Portal Admin")
admin_pass = st.sidebar.text_input("Akses khusus lu (Password: admin123)", type="password")
is_admin = admin_pass == "admin123" 
st.sidebar.divider()

st.sidebar.title("Navigasi 🧭")
menu = st.sidebar.radio("Mau ke mana?", ["Beranda & Galeri", "Substansi Materi", "Ruang Cerita (Anonim)", "Kritik & Saran"])

# === MENU 1: BERANDA & GALERI ===
if menu == "Beranda & Galeri":
    st.markdown('<div class="wave-container"></div>', unsafe_allow_html=True)
    st.markdown('<p class="header-title">Ruang Kita 🚀</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Tempat aman buat belajar dan cerita.</p>', unsafe_allow_html=True)
    
    st.divider()
    st.subheader("📸 Galeri Aksi")
    
    if st.session_state['gallery']:
        cols = st.columns(3)
        for i, img in enumerate(st.session_state['gallery']):
            cols[i % 3].image(img, use_column_width=True)
    else:
        st.info("Belum ada foto yang di-upload nih.")

    if is_admin:
        with st.expander("🛠️ Admin Panel: Upload Foto Baru", expanded=True):
            uploaded_file = st.file_uploader("Pilih foto dokumentasi...", type=['png', 'jpg', 'jpeg'])
            if st.button("Upload ke Galeri") and uploaded_file is not None:
                st.session_state['gallery'].append(uploaded_file)
                st.success("Mantap, foto berhasil mejeng di galeri!")
                st.rerun()

# === MENU 2: SUBSTANSI MATERI (BISA DITAMBAH ADMIN) ===
elif menu == "Substansi Materi":
    st.markdown('<div class="wave-container"></div>', unsafe_allow_html=True)
    st.title("📚 Substansi Materi")
    st.write("Materi asik yang nggak ngebosenin buat bekal masa depan lu.")
    
    # Nampilin Materi dari sistem
    for m in st.session_state['materi']:
        with st.expander(m["judul"]):
            st.write(m["isi"])
            
    # Form Tambah Materi (KHUSUS ADMIN)
    if is_admin:
        st.divider()
        with st.expander("🛠️ Admin Panel: Tambah Materi Baru", expanded=True):
            judul_baru = st.text_input("Judul Materi (Misal: 👨‍👩‍👧‍👦 8 Fungsi Keluarga)")
            isi_baru = st.text_area("Isi Materi (Bisa pake format - atau **tebal**)", height=150)
            if st.button("Posting Materi"):
                if judul_baru and isi_baru:
                    st.session_state['materi'].append({"judul": judul_baru, "isi": isi_baru})
                    st.success("Materi baru berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.warning("Judul sama isi materi jangan dikosongin ya bro.")

# === MENU 3: RUANG CERITA ===
elif menu == "Ruang Cerita (Anonim)":
    st.markdown('<div class="wave-container"></div>', unsafe_allow_html=True)
    st.title("💬 Ruang Cerita")
    st.write("Ada beban pikiran? Ceritain aja di sini. 100% anonim, privasi lu aman.")
    
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

# === MENU 4: KRITIK & SARAN ===
elif menu == "Kritik & Saran":
    st.markdown('<div class="wave-container"></div>', unsafe_allow_html=True)
    st.title("💡 Kotak Saran")
    st.write("Bantu kita bikin web ini makin asik dan nyaman buat lu semua.")
    
    with st.form("feedback_form", clear_on_submit=True):
        feedback = st.text_area("Ada masukin, ide, atau nemu bug? Tulis di sini...", height=100)
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

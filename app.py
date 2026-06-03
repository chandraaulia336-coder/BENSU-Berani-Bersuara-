import streamlit as st
from datetime import datetime

# Setup Halaman
st.set_page_config(page_title="Ruang Kita", page_icon="✨", layout="wide")

# CSS buat styling biar UI/UX nya clean
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: #ffffff;
    }
    .header-title {
        font-size: 40px;
        font-weight: bold;
        color: #BB86FC;
        margin-bottom: -10px;
    }
    .sub-header {
        font-size: 20px;
        color: #B3B3B3;
    }
    </style>
""", unsafe_allow_html=True)

# State nyimpen data sementara (Gallery, Chat, Feedback)
if 'gallery' not in st.session_state:
    st.session_state['gallery'] = []
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'feedbacks' not in st.session_state:
    st.session_state['feedbacks'] = []

# Sidebar Navigasi & Login Admin
st.sidebar.title("Navigasi 🧭")
menu = st.sidebar.radio("Mau ke mana?", ["Beranda & Galeri", "Substansi Materi", "Ruang Cerita (Anonim)", "Kritik & Saran"])

st.sidebar.divider()
admin_pass = st.sidebar.text_input("🔒 Akses Admin", type="password", placeholder="Masukin password...")
is_admin = admin_pass == "admin123" # Password adminnya di sini

# === MENU 1: BERANDA & GALERI ===
if menu == "Beranda & Galeri":
    st.markdown('<p class="header-title">Ruang Kita 🚀</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Tempat aman buat belajar dan cerita.</p>', unsafe_allow_html=True)
    
    st.divider()
    st.subheader("📸 Galeri Aksi")
    st.write("Dokumentasi keseruan pas kita turun langsung ke lapangan.")
    
    # Nampilin Foto Galeri
    if st.session_state['gallery']:
        cols = st.columns(3)
        for i, img in enumerate(st.session_state['gallery']):
            cols[i % 3].image(img, use_column_width=True)
    else:
        st.info("Belum ada foto yang di-upload nih.")

    # Fitur Upload (KHUSUS ADMIN)
    if is_admin:
        with st.expander("🛠️ Admin Panel: Upload Foto Baru", expanded=True):
            uploaded_file = st.file_uploader("Pilih foto dokumentasi...", type=['png', 'jpg', 'jpeg'])
            if st.button("Upload ke Galeri") and uploaded_file is not None:
                st.session_state['gallery'].append(uploaded_file)
                st.success("Mantap, foto berhasil mejeng di galeri!")
                st.rerun()

# === MENU 2: SUBSTANSI MATERI ===
elif menu == "Substansi Materi":
    st.title("📚 Substansi Materi")
    st.write("Materi asik yang nggak ngebosenin buat bekal masa depan lu.")
    
    tab1, tab2, tab3 = st.tabs(["Triad KRR", "Pendewasaan Usia", "8 Fungsi Keluarga"])
    
    with tab1:
        st.subheader("🚫 Triad KRR")
        st.write("- **Pernikahan Dini:** Masa muda tuh buat eksplor, bukan buru-buru nikah.")
        st.write("- **Seks Bebas:** Jaga diri, jaga masa depan.")
        st.write("- **NAPZA:** Narkoba cuma ngasih *happy* palsu yang ngerusak otak.")
        
    with tab2:
        st.subheader("⏳ Pendewasaan Usia Perkawinan (PUP)")
        st.write("Idealnya, cewek nikah umur 21 dan cowok umur 25. Kenapa? Biar mental, fisik, sama finansial udah sama-sama mateng.")
        
    with tab3:
        st.subheader("👨‍👩‍👧‍👦 8 Fungsi Keluarga")
        st.write("Agama, Sosial Budaya, Cinta Kasih, Perlindungan, Reproduksi, Sosialisasi & Pendidikan, Ekonomi, dan Pembinaan Lingkungan.")

# === MENU 3: RUANG CERITA ===
elif menu == "Ruang Cerita (Anonim)":
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
            
    # Balas Cerita (KHUSUS ADMIN)
    if is_admin:
        with st.expander("🛠️ Admin Panel: Balas Cerita", expanded=True):
            admin_balasan = st.text_input("Ketik balasan/solusi dari lu...")
            if st.button("Kirim Balasan"):
                st.session_state['chat_history'].append({"role": "Admin", "text": admin_balasan, "time": datetime.now().strftime("%H:%M")})
                st.rerun()

# === MENU 4: KRITIK & SARAN ===
elif menu == "Kritik & Saran":
    st.title("💡 Kotak Saran")
    st.write("Bantu kita bikin web ini makin asik dan nyaman buat lu semua.")
    
    with st.form("feedback_form", clear_on_submit=True):
        feedback = st.text_area("Ada masukin, ide, atau nemu bug? Tulis di sini...", height=100)
        if st.form_submit_button("Kirim Masukan 🚀") and feedback:
            st.session_state['feedbacks'].append({"isi": feedback, "waktu": datetime.now().strftime("%d/%m/%Y %H:%M")})
            st.success("Tengkyu banget masukannya! Bakal kita baca buat perbaikan ke depannya.")

    # Liat Feedback (KHUSUS ADMIN)
    if is_admin:
        st.divider()
        st.subheader("🛠️ Admin Panel: Daftar Masukan")
        if st.session_state['feedbacks']:
            for idx, fb in enumerate(st.session_state['feedbacks']):
                st.info(f"**[{fb['waktu']}]** {fb['isi']}")
        else:
            st.write("Belum ada masukan nih.")
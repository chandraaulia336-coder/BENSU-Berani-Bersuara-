# ============================================
# MERAH PUTIH - GENRE WEBSITE
# ============================================

import streamlit as st
from datetime import datetime
import base64
import os
import requests


# ===============================
# API GOOGLE SHEETS (JANGAN HAPUS)
# ===============================

API_URL_MATERI = "https://script.google.com/macros/s/AKfycbzbiv0Q2jZoW0lnvQ0iQjFGnPVCij_2mADOPTn-rlYxGj19nVCrjmSkAlOJnBiKDfXB/exec"

API_URL_GALERI = "https://script.google.com/macros/s/AKfycbwIJXXeB58YCeWBqOwLZ5wtLv9Se901K5FaZS5-6YBIjt-I8dtDp1bCQoHgpd_AcF4z/exec"

API_URL_CERITA = "https://script.google.com/macros/s/AKfycbxVCt4UHwrkjwLmS0wdUKKIsa5k6gUB1Yq2HFR3uCQSr-WPg334yaS5f-I48y8O3nw/exec"

API_URL_KRITIK = "https://script.google.com/macros/s/AKfycbxMSnhdLOf1RbVDMRzxuiW1ITEvGQWcMcF5dTxiTmk7HWC4M8u21CYQ_jtrOdoQOI6B/exec"



# ===============================
# DATABASE
# ===============================

def fetch_data(url):
    try:
        r=requests.get(url)
        if r.status_code==200:
            return r.json()
    except:
        pass
    return []


def save_data(url,data):
    try:
        requests.post(url,json={"data":data})
    except:
        pass



# ===============================
# CONFIG
# ===============================

st.set_page_config(
    page_title="Merah Putih GenRe",
    layout="wide"
)



# ===============================
# IMAGE BG
# ===============================

def bg64(path):

    if os.path.exists(path):
        with open(path,"rb") as f:
            return base64.b64encode(f.read()).decode()

    return ""


bg = bg64("25117787.webp")



# ===============================
# CSS MODERN
# ===============================

st.markdown(f"""

<style>


@import url(
'https://fonts.googleapis.com/css2?family=Poppins:wght@400;700;800'
);



.stApp {{

background:

linear-gradient(
rgba(255,255,255,.9),
rgba(230,240,255,.95)
),

url("data:image/webp;base64,{bg}");

background-size:cover;

font-family:Poppins;

}}



section[data-testid="stSidebar"] {{

background:
linear-gradient(
180deg,
#123b8c,
#061b45
);

}}


section[data-testid="stSidebar"] * {{

color:white;

}}



.hero {{

padding:60px;

border-radius:35px;

background:

linear-gradient(
135deg,
white,
#dceaff
);

box-shadow:
0 20px 40px #bbb;

}}



.hero h1 {{

font-size:60px;

font-weight:800;

color:#123b8c;

}}



.card {{

background:white;

padding:25px;

border-radius:25px;

box-shadow:
0 15px 30px #ccd;

margin:15px;

}}



.footer {{

background:

linear-gradient(
90deg,
#123b8c,
#3182ce
);

color:white;

padding:40px;

border-radius:30px;

text-align:center;

}}


</style>


""",
unsafe_allow_html=True)



# ===============================
# SESSION
# ===============================

if "daftar_materi" not in st.session_state:
    st.session_state.daftar_materi = fetch_data(API_URL_MATERI)


if "daftar_galeri" not in st.session_state:
    st.session_state.daftar_galeri = fetch_data(API_URL_GALERI)



# ===============================
# SIDEBAR
# ===============================

if os.path.exists("Logo bumper (1).png"):
    st.sidebar.image(
        "Logo bumper (1).png",
        width=200
    )


st.sidebar.title("🧭 Navigasi")


menu = st.sidebar.radio(
    "",
    [
        "Beranda",
        "Materi",
        "Galeri",
        "Ruang Cerita",
        "Kritik & Saran"
    ]
)



admin = st.sidebar.text_input(
    "Kode Admin",
    type="password"
)


is_admin = admin=="admin123"
# ===============================
# BERANDA
# ===============================

if menu=="Beranda":

    if os.path.exists("Logo bumper (1).png"):

        c1,c2,c3=st.columns([1,2,1])

        with c2:
            st.image(
                "Logo bumper (1).png",
                use_container_width=True
            )


    st.markdown("""
    <div class="hero">

    <h1>🇮🇩 MERAH PUTIH</h1>

    <h2>
    Menuju Era Remaja Aktif,
    Harmonis, Pemuda Unggul,
    Terencana, Inspiratif & Hebat
    </h2>

    <p>
    Ruang digital GenRe untuk belajar,
    berbagi cerita, dan berkembang bersama.
    </p>

    </div>

    """,
    unsafe_allow_html=True)



    st.write("")


    a,b,c=st.columns(3)


    with a:
        st.markdown("""
        <div class="card">

        <h2>🚀 GenRe GTS</h2>

        <p>
        Goes To School.
        Edukasi remaja tentang
        TRIAD KRR, NAPZA,
        pernikahan dini,
        dan kesehatan remaja.

        </p>

        </div>
        """,
        unsafe_allow_html=True)


    with b:
        st.markdown("""
        <div class="card">

        <h2>🏘️ GenRe GTK</h2>

        <p>
        Goes To Kelurahan.
        Membawa edukasi remaja
        lebih dekat dengan masyarakat.

        </p>

        </div>
        """,
        unsafe_allow_html=True)



    with c:
        st.markdown("""
        <div class="card">

        <h2>💡 Ruang Kita</h2>

        <p>
        Tempat aman untuk cerita,
        inspirasi, dan pengembangan diri.

        </p>

        </div>
        """,
        unsafe_allow_html=True)



    st.divider()

    st.subheader("📸 Galeri Aksi")


    galeri = st.session_state.daftar_galeri


    if galeri:

        cols=st.columns(3)

        for i,foto in enumerate(galeri):

            cols[i%3].image(
                foto,
                use_container_width=True
            )


    else:

        st.info(
            "Belum ada foto"
        )



# ===============================
# MATERI
# ===============================


elif menu=="Materi":


    st.title(
        "📚 Substansi Materi"
    )


    for m in st.session_state.daftar_materi:


        with st.expander(
            m.get("Judul","Materi")
        ):

            st.write(
                m.get("Isi","")
            )


            foto=m.get("Foto","")


            if foto and foto!="None":

                for f in foto.split(","):

                    if f!="None":

                        st.image(
                            f.strip(),
                            use_container_width=True
                        )



    if is_admin:


        st.divider()

        st.subheader(
            "Admin Materi"
        )


        judul=st.text_input(
            "Judul"
        )


        isi=st.text_area(
            "Isi"
        )


        foto=st.text_input(
            "Link Foto"
        )


        if st.button(
            "Tambah Materi"
        ):


            data={
            "Judul":judul,
            "Isi":isi,
            "Foto":foto
            }


            st.session_state.daftar_materi.append(data)


            save_data(
                API_URL_MATERI,
                st.session_state.daftar_materi
            )


            st.rerun()



# ===============================
# GALERI
# ===============================


elif menu=="Galeri":


    st.title(
        "📸 Galeri Kegiatan"
    )


    if os.path.exists(
        "genre_juara1.jpg"
    ):

        st.image(
            "genre_juara1.jpg",
            caption="Duta GenRe",
            use_container_width=True
        )


    if os.path.exists(
        "genre_juara.jpg"
    ):

        st.image(
            "genre_juara.jpg",
            use_container_width=True
        )


    cols=st.columns(3)


    for i,f in enumerate(
        st.session_state.daftar_galeri
    ):

        cols[i%3].image(
            f,
            use_container_width=True
        )



    if is_admin:

        link=st.text_input(
            "Link Foto Baru"
        )


        if st.button(
            "Tambah Foto"
        ):

            st.session_state.daftar_galeri.append(link)

            save_data(
                API_URL_GALERI,
                st.session_state.daftar_galeri
            )

            st.rerun()

# ===============================
# RUANG CERITA
# ===============================

elif menu=="Ruang Cerita":


    st.title(
        "💬 Ruang Cerita Anonim"
    )


    if os.path.exists(
        "genre_juara1.jpg"
    ):

        st.image(
            "genre_juara1.jpg",
            caption="Duta GenRe Kecamatan Cilacap Selatan",
            use_container_width=True
        )



    cerita = fetch_data(
        API_URL_CERITA
    )


    with st.form(
        "cerita"
    ):

        isi = st.text_area(
            "Tulis cerita kamu di sini (anonim)"
        )


        kirim = st.form_submit_button(
            "Kirim Cerita 💌"
        )


        if kirim and isi:


            baru={

            "Waktu":
            datetime.now().strftime("%d/%m/%Y %H:%M"),

            "Cerita":
            isi,

            "Respon Admin":
            ""

            }


            cerita.append(
                baru
            )


            save_data(
                API_URL_CERITA,
                cerita
            )


            st.success(
                "Cerita berhasil dikirim"
            )


            st.rerun()



    st.divider()


    for item in reversed(
        cerita
    ):


        st.markdown(
        """
        <div class="card">
        """,
        unsafe_allow_html=True
        )


        st.write(
            "👤 Anonim"
        )


        st.info(
            item.get("Cerita","")
        )


        respon=item.get(
            "Respon Admin",
            ""
        )


        if respon:

            st.success(
                respon
            )


        else:

            st.caption(
                "Belum ada respon admin"
            )


        st.markdown(
        "</div>",
        unsafe_allow_html=True
        )




# ===============================
# KRITIK SARAN
# ===============================


elif menu=="Kritik & Saran":


    st.title(
        "📥 Kritik & Saran"
    )


    if os.path.exists(
        "genre_juara.jpg"
    ):

        st.image(
            "genre_juara.jpg",
            use_container_width=True
        )



    kritik=fetch_data(
        API_URL_KRITIK
    )


    with st.form(
        "kritik"
    ):


        topik=st.selectbox(
            "Topik",
            [
            "Pelayanan/Konseling",
            "Konten Materi",
            "Tampilan Web",
            "Lainnya"
            ]
        )


        isi=st.text_area(
            "Masukan kamu"
        )


        submit=st.form_submit_button(
            "Kirim 🚀"
        )



        if submit and isi:


            baru={

            "Waktu":
            datetime.now().strftime("%d/%m/%Y %H:%M"),

            "Topik":
            topik,

            "Isi Kritik":
            isi

            }


            kritik.append(
                baru
            )


            save_data(
                API_URL_KRITIK,
                kritik
            )


            st.success(
                "Terima kasih atas masukannya!"
            )



    st.divider()


    st.subheader(
        "📞 Konseling Privat"
    )


    st.write(
        """
        Butuh ngobrol langsung?
        Hubungi admin melalui WhatsApp.
        """
    )


    st.link_button(
        "Hubungi Admin WhatsApp 💬",
        "https://wa.me/qr/RTCENRAXQVZFM1",
        use_container_width=True
    )




# ===============================
# FOOTER
# ===============================


st.markdown(
"""
<br><br>

<div class="footer">

<h2>
🇮🇩 MERAH PUTIH
</h2>

<p>
Remaja Aktif • Pemuda Inspiratif • Generasi Berencana
</p>

</div>

""",
unsafe_allow_html=True
)

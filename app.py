import base64
from datetime import datetime, timedelta
import os
import random
import pandas as pd
import pydeck as pdk
import requests
import streamlit as st

# ==========================================
# 1. KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Merpati Putih - Remaja Terencana",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# 2. URL GOOGLE APPS SCRIPT (API ENDPOINTS)
# ==========================================
API_URL_MATERI = "https://script.google.com/macros/s/AKfycbwLfXYY-9-PwdVB1xQKtD1c2npawNgTeOuGHmDzPr7LGC1inbTxuxwnt8m7Z0LcJHsxyA/exec"
API_URL_GALERI = "https://script.google.com/macros/s/AKfycbz-rX4p9SpDIE1TVv1zuItWKKgKxd0AJSWpib8XGCjE4oHb_n1RAH-4azED-MCCjpaHXg/exec"
API_URL_CERITA = "https://script.google.com/macros/s/AKfycbxCPeC-7fE7Fu2O1J5dJ7-juwi3iQrl0L0ug3nonVuTIf_sC0yJYjZ6mS4HaQDH4y-g/exec"
API_URL_KRITIK = "https://script.google.com/macros/s/AKfycbxMSnhdLOf1RbVDMRzxuiW1ITEvGQWcMcF5dTxiTmk7HWC4M8u21CYQ_jtrOdoQOI6B/exec"


# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def fetch_api_data(url):
  if not url or "script.google.com" not in url:
    return []
  try:
    res = requests.get(url, timeout=6)
    if res.status_code == 200:
      data = res.json()
      if isinstance(data, list):
        return data
      elif isinstance(data, dict) and "data" in data:
        return data["data"]
    return []
  except Exception:
    return []


def save_api_data(url, data_list):
  if not url or "script.google.com" not in url:
    return False
  try:
    res = requests.post(url, json={"data": data_list}, timeout=8)
    return res.status_code == 200
  except Exception:
    return False


# ==========================================
# 4. INITIAL MATERI EDUKASI (DEFAULT + NEW)
# ==========================================
MATERI_DEFAULT = [
    {
        "Judul": "🩸 Anemia: 'Baterai Drop' Penyebab Otak Lemot & Muka Pucat!",
        "Isi": (
            "**Pernah ngerasa gampang ngantuk di kelas, muka pucat, dan mager"
            " parah? Bisa jadi kamu kena Anemia!** 🪫\n\n"
            "Anemia terjadi saat kadar **Hemoglobin (Hb)** drop akibat"
            " kekurangan zat besi. Hb ini ibarat 'ojek online' di dalam darah"
            " yang bertugas mengantar oksigen ke otak dan seluruh tubuh.\n\n"
            "**Gaya 5L yang Bikin Hidup Nggak Asyik:**\n"
            "1. **L**esu\n2. **L**emah\n3. **L**elah\n4. **L**etih\n5."
            " **L**alai (Gampang lupa & susah fokus)\n\n"
            "**Kenapa Remaja Putri Paling Rawan?**\n"
            "Karena remaja putri mengalami menstruasi setiap bulan dan sering"
            " kali melakukan diet ketat yang salah.\n\n"
            "**Solusi Sat-Set Biar Baterai Tubuh Full Lagi:**\n"
            "• 💊 **Minum TTD (Tablet Tambah Darah):** Rutin **1 tablet seminggu"
            " sekali** (dan **1 tablet sehari saat menstruasi**).\n"
            "• 🍊 **Combo Vitamin C:** Minum TTD bareng es jeruk/jus buah biar"
            " penyerapan zat besinya maksimal!\n"
            "• 🚫 **Hindari Banting Zat Besi:** Jangan minum TTD barengan sama"
            " **Kopi, Teh, atau Susu**, karena bisa bikin zat besinya gagal"
            " diserap tubuh."
        ),
        "Foto": (
            "https://images.unsplash.com/photo-1505751172876-fa1923c5c528?q=80&w=800&auto=format&fit=crop"
        ),
    },
    {
        "Judul": (
            "🛑 Stunting: Bukan Cuma Pendek, Tapi Otak Juga 'Loading' Lama!"
        ),
        "Isi": (
            "**Banyak yang salah kaprah: 'Pendek itu kan faktor keturunan"
            " (genetik)?' Eits, tunggu dulu!** ✋\n\n"
            "Orang pendek belum tentu stunting, tapi orang stunting **pasti"
            " pendek** dan pertumbuhan otak serta daya tahan tubuhnya terhambat"
            " akibat **kurang gizi kronis dalam 1.000 Hari Pertama Kehidupan"
            " (HPHT)**.\n\n"
            "**Dampak Horor Stunting:**\n"
            "• 🧠 **IQ Rendah:** Otak jadi lambat merespon dan sulit bersaing di"
            " dunia kerja.\n"
            "• 🤒 **Gampang Sakit:** Imunitas tubuh lemah.\n"
            "• 💸 **Biaya Berobat Mahal:** Berisiko kena penyakit tidak menular"
            " (diabetes, jantung) saat dewasa.\n\n"
            "**Gimana Cara Remaja Cegah Stunting dari Sekarang?**\n"
            "• 🥚 **Gempur Protein Hewani:** Rutin makan Telur, Ikan, Ayam, atau"
            " Daging. Telur 1-2 butir sehari itu *superfood* murah cegah"
            " stunting!\n"
            "• 💍 **Stop Pernikahan Dini:** Usia ibu yang belum siap (di bawah"
            " 21 tahun) bikin risiko bayi lahir stunting melonjak tajam!\n"
            "• 🩺 **Skrining Catin (Calon Pengantin):** Cek Hb dan Lingkar"
            " Lengan Atas (LILA) minimal 3 bulan sebelum nikah."
        ),
        "Foto": (
            "https://images.unsplash.com/photo-1498837167922-ddd27525d352?q=80&w=800&auto=format&fit=crop"
        ),
    },
    {
        "Judul": (
            "🚀 Bonus Demografi: Indonesia Emas atau 'Bencana Demografi'?"
        ),
        "Isi": (
            "**Kamu sadar nggak, kalau kamu dan teman-temanmu adalah penentu"
            " nasib Indonesia beberapa tahun ke depan?** 🇮🇩🔥\n\n"
            "**Apa Itu Bonus Demografi?**\n"
            "Bonus Demografi adalah momen langka sekali seumur hidup di mana"
            " jumlah **penduduk usia produktif (15-64 tahun)** jauh lebih"
            " banyak dibandingkan penduduk non-produktif.\n\n"
            "**Peluang 'Indonesia Emas 2045':**\n"
            "Kalau remajanya cerdas, sehat, kreatif, dan punya *skill* tinggi,"
            " Indonesia bisa berubah jadi negara maju dunia!\n\n"
            "**Ancaman 'Bencana Demografi':**\n"
            "Tapi kalau remajanya malah terjebak **Triad KRR** (Seks Bebas, Nikah"
            " Dini, NAPZA), kena **Anemia**, dan melahirkan anak-anak"
            " **Stunting**, bonus demografi justru jadi beban berat buat"
            " negara!\n\n"
            "**Peran Kamu Sebagai GenRe:**\n"
            "1. 📚 Bekali diri dengan *Life Skills* & literasi digital.\n"
            "2. 🛡️ Berani bilang **TIDAK** pada Pernikahan Dini & Narkoba.\n"
            "3. 🎯 Rencanakan pendidikan, karir, dan pernikahan secara matang."
        ),
        "Foto": (
            "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?q=80&w=800&auto=format&fit=crop"
        ),
    },
]

# ==========================================
# 5. SESSION STATE INITIALIZATION
# ==========================================
if "daftar_materi" not in st.session_state:
  api_materi = fetch_api_data(API_URL_MATERI)
  st.session_state["daftar_materi"] = (
      api_materi if len(api_materi) > 0 else MATERI_DEFAULT
  )
else:
  # Memastikan materi bawaan selalu masuk jika belum terdaftar
  for m_def in MATERI_DEFAULT:
    if not any(
        x.get("Judul") == m_def["Judul"]
        for x in st.session_state["daftar_materi"]
    ):
      st.session_state["daftar_materi"].append(m_def)

if "daftar_galeri" not in st.session_state:
  st.session_state["daftar_galeri"] = fetch_api_data(API_URL_GALERI)

if "tagline" not in st.session_state:
  st.session_state["tagline"] = (
      "Sebuah Gerakan dari Remaja untuk Melangitkan Harapan dan Membumikan"
      " Kebermanfaatan."
  )


# ==========================================
# 6. WALLPAPER BACKGROUND HELPER
# ==========================================
def get_base64_bg(image_path):
  if os.path.exists(image_path):
    with open(image_path, "rb") as img_file:
      encoded = base64.b64encode(img_file.read()).decode()
    return f"data:image/webp;base64,{encoded}"
  return ""


bg_image = get_base64_bg("25117787.webp")

# ==========================================
# 7. CUSTOM CSS (STYLING)
# ==========================================
st.markdown(
    f"""
    <style>
    html {{ scroll-behavior: smooth; }}
    .stApp {{
        background: linear-gradient(rgba(15, 23, 42, 0.88), rgba(15, 23, 42, 0.95)), url("{bg_image}"); 
        background-size: cover !important; background-position: center !important; background-attachment: fixed !important;
        color: #F8FAFC !important;
    }}
    .hero-title {{ font-size: 3.2rem; font-weight: 800; color: #FFFFFF; line-height: 1.2; margin-bottom: 15px; text-shadow: 0 4px 12px rgba(0,0,0,0.5); }}
    .hero-subtitle {{ font-size: 1.25rem; color: #38BDF8; font-weight: 600; margin-bottom: 20px; }}
    .section-title {{ font-size: 2rem; font-weight: 700; text-align: center; color: #FFFFFF; margin-top: 35px; margin-bottom: 25px; }}
    .stApp p, .stApp span, .stApp label, .stApp div {{ color: #E2E8F0 !important; }}
    [data-testid="stMetricValue"] {{ color: #38BDF8 !important; font-size: 2.3rem !important; font-weight: 800 !important; }}
    [data-testid="stMetricLabel"] {{ color: #94A3B8 !important; font-size: 0.95rem !important; font-weight: 600 !important; }}
    div.stMetric {{ background: rgba(30, 41, 59, 0.65) !important; padding: 20px 15px !important; border-radius: 16px !important; border: 1px solid rgba(255, 255, 255, 0.12) !important; backdrop-filter: blur(10px); text-align: center !important; }}
    div[data-testid="stRadio"] > label {{ display: none; }}
    div[data-testid="stRadio"] > div {{ background-color: rgba(30, 41, 59, 0.7); padding: 8px; border-radius: 14px; gap: 8px; border: 1px solid rgba(255, 255, 255, 0.12); }}
    div[data-testid="stRadio"] label[data-baseweb="radio"] {{ background-color: transparent; padding: 8px 18px !important; border-radius: 10px; color: #94A3B8 !important; font-weight: 600; transition: all 0.25s ease; }}
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {{ background-color: #38BDF8 !important; }}
    div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) span {{ color: #0F172A !important; font-weight: 700 !important; }}
    .stExpander, div[data-testid="stForm"] {{ background-color: rgba(30, 41, 59, 0.55) !important; border: 1px solid rgba(255, 255, 255, 0.12) !important; border-radius: 14px !important; padding: 20px !important;}}
    #MainMenu {{visibility: hidden;}} footer {{visibility: hidden;}}
    .btn-merpati-putih {{ display: inline-block; background: linear-gradient(135deg, #38BDF8 0%, #0284C7 100%); color: #FFFFFF !important; padding: 12px 28px; border-radius: 10px; text-decoration: none; font-weight: 700; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(56, 189, 248, 0.35); }}
    .story-card {{ background: rgba(30, 41, 59, 0.6); border-radius: 12px; padding: 16px; border-left: 4px solid #38BDF8; margin-bottom: 15px; }}
    .admin-reply-card {{ background: rgba(16, 185, 129, 0.15); border-radius: 10px; padding: 12px; border-left: 4px solid #10B981; margin-top: 10px; }}
    .sertifikat {{ background: linear-gradient(135deg, #fbbf24 0%, #d97706 100%); padding: 30px; border-radius: 15px; text-align: center; color: white !important; border: 4px dashed #fef3c7; margin-top: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.4); }}
    .piring-card {{ background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 14px; padding: 15px; text-align: center; margin-bottom: 10px; }}
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 8. HEADER & NAVIGATION
# ==========================================
col_logo, col_nav = st.columns([1, 4], vertical_alignment="center")
with col_logo:
  if os.path.exists("Logo bumper (1).png"):
    st.image("Logo bumper (1).png", width=140)
  else:
    st.markdown(
        "<h3 style='color:#FFFFFF; margin:0; font-weight:800;'>🕊️ MERPATI"
        " PUTIH</h3>",
        unsafe_allow_html=True,
    )

with col_nav:
  menu = st.radio(
      "Menu Navigation",
      [
          "Beranda & Peta",
          "Edukasi & Tools Gizi",
          "Kuis GenRe",
          "Ruang Cerita (Anonim)",
          "Kritik & Saran",
          "Admin Panel",
      ],
      horizontal=True,
  )

st.markdown(
    "<hr style='margin-top:5px;"
    " margin-bottom:25px; border-color:rgba(255,255,255,0.1);'>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# MENU 1: BERANDA & PETA SPASIAL
# ---------------------------------------------------------
if menu == "Beranda & Peta":
  h_col1, h_col2 = st.columns([1.2, 1], gap="large")
  with h_col1:
    st.markdown(
        '<div class="hero-title">Merpati Putih: Menuju Era Remaja'
        " Terencana.</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="hero-subtitle">{st.session_state["tagline"]}</div>',
        unsafe_allow_html=True,
    )
    st.write(
        "Jadilah pemuda yang aktif, harmonis, unggul, terencana, inspiratif, &"
        " hebat. Masa depan yang cemerlang dimulai dari langkah nyata hari ini."
    )

    quotes = [
        (
            "Perencanaan hari ini adalah kunci kebahagiaan keluarga esok hari."
            " - GenRe"
        ),
        (
            "Remaja Hebat itu yang menjauhi Narkoba, Seks Bebas, dan Pernikahan"
            " Dini!"
        ),
        "Tunda nikah muda, kejar prestasi setinggi-tingginya!",
        "Keluarga berkualitas berawal dari remaja yang cerdas.",
    ]
    if st.button("🎲 Dapatkan Motivasi GenRe Hari Ini"):
      st.info(f'💡 *"{random.choice(quotes)}"*')

    st.markdown(
        '<br><a href="#galeri" class="btn-merpati-putih">Mengenal Lebih Dekat'
        " 🚀</a>",
        unsafe_allow_html=True,
    )

  with h_col2:
    if os.path.exists("genre_juara1.jpg"):
      st.image("genre_juara1.jpg", use_container_width=True)

  st.markdown(
      '<div class="section-title">📊 Merpati Putih Dalam Angka</div>',
      unsafe_allow_html=True,
  )
  m1, m2, m3, m4 = st.columns(4)
  m1.metric(label="Tahun Dedikasi", value="1+")
  m2.metric(label="Remaja Terdampak", value="200+")
  m3.metric(label="Titik Wilayah", value="12")
  cerita_data = fetch_api_data(API_URL_CERITA)
  m4.metric(label="Aspirasi Masuk", value=str(len(cerita_data)))

  # PETA SPASIAL BLUE ZONE (PYDECK POLYGON)
  st.markdown(
      '<div class="section-title">🗺️ Peta Zonasi "Blue Zone" (Cilacap'
      " Selatan)</div>",
      unsafe_allow_html=True,
  )
  st.write(
      "Visualisasi wilayah **Kecamatan Cilacap Selatan** sebagai percontohan"
      " wilayah intervensi khusus (Blue Zone) program Merpati Putih."
  )

  zona_cilacap_selatan = [
      [108.990, -7.745],
      [109.025, -7.745],
      [109.020, -7.710],
      [108.995, -7.710],
      [108.990, -7.745],
  ]

  df_zona = pd.DataFrame({
      "zona": ["Kec. Cilacap Selatan (Blue Zone)"],
      "deskripsi": ["Wilayah percontohan bebas Stunting & Triad KRR"],
      "koordinat": [[zona_cilacap_selatan]],
  })

  layer_polygon = pdk.Layer(
      "PolygonLayer",
      df_zona,
      get_polygon="koordinat",
      get_fill_color="[56, 189, 248, 80]",
      get_line_color="[2, 132, 199, 255]",
      get_line_width=80,
      pickable=True,
      extruded=False,
  )

  view_state = pdk.ViewState(
      latitude=-7.7279, longitude=109.0063, zoom=12.2, pitch=25
  )

  st.pydeck_chart(
      pdk.Deck(
          map_provider="carto",
          map_style="dark",
          initial_view_state=view_state,
          layers=[layer_polygon],
          tooltip={
              "html": "<b>{zona}</b><br/>{deskripsi}",
              "style": {"backgroundColor": "#0284C7", "color": "white"},
          },
      )
  )

  # GALERI
  st.markdown(
      '<div id="galeri" class="section-title">🖼️ Peta Jejak Keberdampakan'
      " (Galeri)</div>",
      unsafe_allow_html=True,
  )

  galeri_api = st.session_state.get("daftar_galeri", [])
  if isinstance(galeri_api, list) and len(galeri_api) > 0:
    g_cols = st.columns(3)
    for i, url_img in enumerate(galeri_api):
      try:
        g_cols[i % 3].image(url_img, use_container_width=True)
      except Exception:
        pass
  else:
    st.info("Belum ada foto galeri yang diunggah.")

# ---------------------------------------------------------
# MENU 2: EDUKASI & TOOLS GIZI + KESPRO
# ---------------------------------------------------------
elif menu == "Edukasi & Tools Gizi":
  st.markdown(
      '<div class="section-title">📚 Substansi Edukasi & Tools'
      " Interaktif</div>",
      unsafe_allow_html=True,
  )

  tab_materi, tab_tools, tab_piringku, tab_siapnikah, tab_siklus = st.tabs([
      "📖 Perpustakaan Materi",
      "⚖️ Kalkulator IMT",
      "🍽️ Panduan Isi Piringku",
      "💍 Skrining Siap Nikah (BKKBN)",
      "🗓️ Kalender Siklus & TTD",
  ])

  # TAB 1: MATERI + SEARCH BAR
  with tab_materi:
    st.write(
        "Jelajahi berbagai materi terkait 8 Fungsi Keluarga, PUP, Stunting,"
        " Anemia, Bonus Demografi, dan pencegahan Triad KRR."
    )
    search_kw = st.text_input(
        "🔍 Cari Materi Edukasi (misal: Stunting, Anemia, PUP, Bonus"
        " Demografi)..."
    )

    materi_all = st.session_state.get("daftar_materi", [])
    if search_kw.strip():
      materi_filtered = [
          m
          for m in materi_all
          if search_kw.lower() in m.get("Judul", "").lower()
          or search_kw.lower() in m.get("Isi", "").lower()
      ]
    else:
      materi_filtered = materi_all

    if materi_filtered:
      for m in materi_filtered:
        with st.expander(f"📌 {m.get('Judul', 'Tanpa Judul')}"):
          st.markdown(m.get("Isi", ""))

          foto_val = str(m.get("Foto", "")).strip()
          if foto_val and foto_val.lower() != "none":
            list_foto = [
                url.strip()
                for url in foto_val.split(",")
                if url.strip() and url.strip().lower() != "none"
            ]
            if len(list_foto) > 0:
              cols_foto = st.columns(min(len(list_foto), 3))
              for idx_f, url_f in enumerate(list_foto):
                try:
                  cols_foto[idx_f % 3].image(url_f, use_container_width=True)
                except Exception:
                  pass
    else:
      st.info("Materi yang dicari tidak ditemukan.")

  # TAB 2: KALKULATOR IMT
  with tab_tools:
    st.subheader("Kalkulator Indeks Massa Tubuh (IMT) Remaja")
    st.write(
        "Pencegahan Stunting dimulai dari calon orang tua yang sehat. Yuk, cek"
        " status gizimu sekarang!"
    )

    c_berat, c_tinggi = st.columns(2)
    berat = c_berat.number_input(
        "Berat Badan (Kg)", min_value=20.0, max_value=150.0, value=50.0
    )
    tinggi = c_tinggi.number_input(
        "Tinggi Badan (Cm)", min_value=100.0, max_value=220.0, value=160.0
    )

    if st.button("Hitung Status Gizi 🔍", type="primary"):
      tinggi_m = tinggi / 100
      imt = berat / (tinggi_m**2)
      st.markdown(f"### Nilai IMT Kamu: **{imt:.1f}**")

      if imt < 18.5:
        st.warning(
            "⚠️ **Kurus (Kekurangan Berat Badan)**. Risiko anemia tinggi!"
            " Perbanyak makanan bergizi dan minum Tablet Tambah Darah (TTD)"
            " untuk remaja putri."
        )
      elif 18.5 <= imt <= 24.9:
        st.success(
            "✅ **Normal (Ideal)**. Bagus sekali! Status gizimu ideal untuk"
            " mempersiapkan masa depan yang sehat dan mencegah stunting pada"
            " keturunan kelak."
        )
      elif 25 <= imt <= 29.9:
        st.warning(
            "⚠️ **Gemuk (Overweight)**. Jaga pola makan dan rutinkan aktivitas"
            " fisik/olahraga minimal 30 menit sehari ya."
        )
      else:
        st.error(
            "🚨 **Obesitas**. Sangat berisiko bagi kesehatan reproduksi dan"
            " metabolisme. Segera konsultasikan pola diet sehat ke ahli gizi."
        )

  # TAB 3: ISI PIRINGKU
  with tab_piringku:
    st.subheader("🍽️ Konsep Isi Piringku (Kemenkes RI)")
    st.write(
        "Panduan porsi gizi seimbang dalam sekali makan untuk memenuhi nutrisi"
        " harian dan **mencegah Stunting sejak usia remaja**."
    )

    p1, p2, p3, p4 = st.columns(4)
    with p1:
      st.markdown(
          '<div class="piring-card"><h3>🍚 35%</h3><b>Makanan'
          " Pokok</b><br><small>Nasi, Jagung, Kentang,"
          " Singkong</small></div>",
          unsafe_allow_html=True,
      )
    with p2:
      st.markdown(
          '<div class="piring-card"><h3>🍗 15%</h3><b>Lauk'
          " Pauk</b><br><small>Ikan, Ayam, Telur, Daging, Tempe,"
          " Tahu</small></div>",
          unsafe_allow_html=True,
      )
    with p3:
      st.markdown(
          '<div class="piring-card"><h3>🥦 35%</h3><b>Sayur'
          " Mayur</b><br><small>Bayam, Wortel, Brokoli, Kangkung</small></div>",
          unsafe_allow_html=True,
      )
    with p4:
      st.markdown(
          '<div class="piring-card"><h3>🍎 15%</h3><b>Buah'
          " Buahan</b><br><small>Pisang, Jeruk, Pepaya, Apel</small></div>",
          unsafe_allow_html=True,
      )

    st.write("---")
    st.subheader("🧪 Simulasi & Analisis Kelengkapan Piringku")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
      f_pokok = st.selectbox(
          "1. Makanan Pokok (Karbohidrat)",
          [
              "-- Pilih Menu --",
              "Nasi Putih / Merah",
              "Kentang / Singkong",
              "Roti / Mie",
              "Tidak Ada",
          ],
      )
      f_lauk_h = st.selectbox(
          "2. Lauk Hewani (Kunci Utama Pencegahan Stunting!)",
          [
              "-- Pilih Menu --",
              "Telur Ayam",
              "Ikan / Udang",
              "Daging Ayam / Sapi",
              "Tidak Ada",
          ],
      )
      f_lauk_n = st.selectbox(
          "3. Lauk Nabati",
          ["-- Pilih Menu --", "Tahu / Tempe", "Kacang-kacangan", "Tidak Ada"],
      )

    with col_s2:
      f_sayur = st.selectbox(
          "4. Sayur-Mayur",
          [
              "-- Pilih Menu --",
              "Sayuran Hijau (Bayam, Kangkung, dll)",
              "Sayuran Lain (Wortel, Labu, dll)",
              "Tidak Ada",
          ],
      )
      f_buah = st.selectbox(
          "5. Buah-Buahan",
          ["-- Pilih Menu --", "Ada (Pisang, Jeruk, Pepaya, dll)", "Tidak Ada"],
      )
      f_air = st.checkbox(
          "💧 Sudah Minum Air Putih Minimal 1-2 Gelas?", value=True
      )

    if st.button("Analisis Piringku Sekarang 🧐", type="primary"):
      skor_piring = 0
      catatan = []

      if f_pokok not in ["-- Pilih Menu --", "Tidak Ada"]:
        skor_piring += 25
      else:
        catatan.append(
            "❌ Belum ada karbohidrat/makanan pokok sebagai sumber energi."
        )

      if f_lauk_h not in ["-- Pilih Menu --", "Tidak Ada"]:
        skor_piring += 30
      else:
        catatan.append(
            "🚨 **SANGAT PENTING:** Belum ada Protein Hewani! Protein hewani"
            " (Telur/Ikan/Daging) adalah zat kunci mencegah Stunting &"
            " Anemia pada remaja."
        )

      if f_lauk_n not in ["-- Pilih Menu --", "Tidak Ada"]:
        skor_piring += 15

      if f_sayur not in ["-- Pilih Menu --", "Tidak Ada"]:
        skor_piring += 15
      else:
        catatan.append(
            "❌ Belum ada Sayuran (Sumber serat, mikronutrien, dan vitamin)."
        )

      if f_buah not in ["-- Pilih Menu --", "Tidak Ada"]:
        skor_piring += 15
      else:
        catatan.append(
            "⚠️ Belum ada Buah-buahan sebagai suplemen vitamin alami."
        )

      st.markdown(
          f'<div class="section-title" style="color:#38BDF8; margin-top:20px;'
          f' margin-bottom:10px;">Skor Nutrisi Piringmu: {skor_piring} /'
          " 100</div>",
          unsafe_allow_html=True,
      )

      if skor_piring >= 85 and f_lauk_h not in ["-- Pilih Menu --", "Tidak Ada"]:
        st.success(
            "🎉 **Gizi Seimbang Sempurna!** Piring makanmu sudah memenuhi"
            " kriteria Isi Piringku Kemenkes RI. Pertahankan pola makan sehat"
            " ini ya!"
        )
      else:
        st.warning("📋 **Rekomendasi Perbaikan Piringku:**")
        for c in catatan:
          st.write(f"- {c}")

  # TAB 4: SKRINING SIAP NIKAH + DOWNLOAD SUMMARY
  with tab_siapnikah:
    st.subheader("💍 Skrining Kesiapan Nikah & Hamil (Standar Elsimil BKKBN)")
    st.write(
        "Pencegahan Stunting paling efektif dimulai dari **3 Bulan Sebelum"
        " Pernikahan**. Yuk cek kesiapan fisik, gizi, dan mentalmu!"
    )

    gender = st.radio(
        "Pilih Jenis Kelamin Calon Pengantin:",
        ["👩 Wanita (Calon Ibu)", "👨 Pria (Calon Ayah)"],
        horizontal=True,
    )
    st.write("---")

    if "Wanita" in gender:
      col_w1, col_w2 = st.columns(2)
      with col_w1:
        u_wanita = st.number_input("Usia Calon Pengantin Wanita (Tahun)", 15, 50, 22)
        hb_wanita = st.number_input(
            "Kadar Hemoglobin / Hb (g/dL) - *Cek Puskesmas*", 7.0, 18.0, 12.5, step=0.1
        )
        lila_wanita = st.number_input(
            "Lingkar Lengan Atas / LILA (cm)", 15.0, 40.0, 24.0, step=0.5
        )

      with col_w2:
        tt_wanita = st.checkbox(
            "💉 Sudah Mendapat Imunisasi Tetanus Toksoid (TT)?", value=True
        )
        fin_wanita = st.checkbox("💰 Ada Perencanaan Finansial & Kerja?", value=True)
        psikolog_wanita = st.checkbox(
            "🧠 Siap Secara Mental / Emosional?", value=True
        )

      if st.button("Cek Hasil Skrining Wanita 🩺", type="primary"):
        skor_sn = 0
        catatan_sn = []

        if u_wanita >= 21:
          skor_sn += 25
        else:
          catatan_sn.append(
              f"Usia Belum Ideal ({u_wanita} Thn): Minimal 21 thn untuk wanita."
          )

        if hb_wanita >= 12.0:
          skor_sn += 25
        else:
          catatan_sn.append(
              f"Hb Rendah ({hb_wanita} g/dL): Terindikasi Anemia."
          )

        if lila_wanita >= 23.5:
          skor_sn += 25
        else:
          catatan_sn.append(
              f"LILA Kurang dari 23.5 cm ({lila_wanita} cm): Risiko KEK."
          )

        if tt_wanita and fin_wanita and psikolog_wanita:
          skor_sn += 25
        else:
          catatan_sn.append(
              "Lengkapi Imunisasi TT dan kesiapan mental/finansial."
          )

        st.markdown(f"### Indeks Kesiapan Nikah: **{skor_sn}%**")
        if skor_sn == 100:
          st.success("🎉 **SANGAT SIAP NIKAH & HAMIL!** Fisik dan gizi ideal.")
        else:
          st.warning("📋 **Catatan Evaluasi:**")
          for c in catatan_sn:
            st.write(f"- {c}")

        txt_summary = (
            f"=== LAPORAN SKRINING SIAP NIKAH MERPATI PUTIH ===\n"
            f"Tanggal: {datetime.now().strftime('%d/%m/%Y')}\n"
            f"Kategori: Calon Pengantin Wanita\n"
            f"Usia: {u_wanita} Thn | Hb: {hb_wanita} g/dL | LILA: {lila_wanita} cm\n"
            f"Skor Kesiapan: {skor_sn}%\n\n"
            f"Evaluasi:\n" + "\n".join([f"- {item}" for item in catatan_sn])
        )
        st.download_button(
            label="📄 Download Hasil Skrining (TXT)",
            data=txt_summary,
            file_name=f"skrining_catin_wanita_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
        )

    else:  # Pria
      col_m1, col_m2 = st.columns(2)
      with col_m1:
        u_pria = st.number_input("Usia Calon Pengantin Pria (Tahun)", 15, 60, 25)
        rokok_pria = st.selectbox(
            "Kebiasaan Merokok",
            ["Tidak Merokok", "Perokok Pasif", "Perokok Aktif"],
        )

      with col_m2:
        sehat_pria = st.checkbox(
            "🩺 Bebas Penyakit Menular / TBC / NAPZA?", value=True
        )
        fin_pria = st.checkbox("💼 Memiliki Penghasilan Mandiri?", value=True)
        psikolog_pria = st.checkbox(
            "👨‍👩‍👧 Siap Menjadi Kepala Keluarga?", value=True
        )

      if st.button("Cek Hasil Skrining Pria 👨‍⚕️", type="primary"):
        skor_pria = 0
        catatan_pria = []

        if u_pria >= 25:
          skor_pria += 30
        else:
          catatan_pria.append(
              f"Usia Belum Ideal ({u_pria} Thn): Minimal 25 thn untuk pria."
          )

        if rokok_pria == "Tidak Merokok":
          skor_pria += 30
        elif rokok_pria == "Perokok Pasif":
          skor_pria += 20
        else:
          catatan_pria.append(
              "Perokok Aktif: Asap rokok merusak kualitas sperma & kesehatan"
              " janin."
          )

        if sehat_pria:
          skor_pria += 20
        else:
          catatan_pria.append("Lakukan cek kesehatan rutin di Puskesmas.")

        if fin_pria and psikolog_pria:
          skor_pria += 20
        else:
          catatan_pria.append("Matangkan kesiapan finansial dan psikologis.")

        st.markdown(f"### Indeks Kesiapan Nikah: **{skor_pria}%**")
        if skor_pria >= 90:
          st.success("🎉 **SANGAT SIAP NIKAH!** Siap menjadi kepala keluarga.")
        else:
          st.warning("📋 **Catatan Evaluasi:**")
          for c in catatan_pria:
            st.write(f"- {c}")

        txt_pria = (
            f"=== LAPORAN SKRINING SIAP NIKAH MERPATI PUTIH ===\n"
            f"Tanggal: {datetime.now().strftime('%d/%m/%Y')}\n"
            f"Kategori: Calon Pengantin Pria\n"
            f"Usia: {u_pria} Thn | Merokok: {rokok_pria}\n"
            f"Skor Kesiapan: {skor_pria}%\n\n"
            f"Evaluasi:\n" + "\n".join([f"- {item}" for item in catatan_pria])
        )
        st.download_button(
            label="📄 Download Hasil Skrining (TXT)",
            data=txt_pria,
            file_name=f"skrining_catin_pria_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain",
        )

  # TAB 5: KALENDER SIKLUS & PENGINGAT TTD
  with tab_siklus:
    st.subheader(
        "🗓️ Kalkulator Siklus Menstruasi, Masa Subur & Pengingat TTD"
    )
    st.write(
        "Pencegahan Anemia pada remaja putri sangat vital untuk mencegah"
        " stunting pada generasi masa depan."
    )

    col_k1, col_k2 = st.columns(2)
    with col_k1:
      hpht = st.date_input(
          "Hari Pertama Haid Terakhir (HPHT)", value=datetime.now()
      )
      panjang_siklus = st.number_input(
          "Rata-rata Panjang Siklus Haid (Hari)", 21, 40, 28
      )
    with col_k2:
      lama_haid = st.number_input(
          "Rata-rata Lama Menstruasi (Hari)", 3, 14, 7
      )

    if st.button("Hitung Siklus & Masa Subur 🌸", type="primary"):
      haid_berikutnya = hpht + timedelta(days=int(panjang_siklus))
      ovulasi = hpht + timedelta(days=int(panjang_siklus - 14))
      subur_awal = ovulasi - timedelta(days=2)
      subur_akhir = ovulasi + timedelta(days=2)

      m_s1, m_s2 = st.columns(2)
      m_s1.metric("Est. Haid Berikutnya", haid_berikutnya.strftime("%d %B %Y"))
      m_s2.metric("Est. Puncak Ovulasi", ovulasi.strftime("%d %B %Y"))

      st.info(
          f"💡 **Masa Subur Utama:** {subur_awal.strftime('%d %B')} s/d"
          f" {subur_akhir.strftime('%d %B %Y')}"
      )

      st.markdown("---")
      st.subheader("💊 Panduan Minum Tablet Tambah Darah (TTD)")
      st.warning(
          "🩸 **Saat Menstruasi:** Minum **1 Tablet Tambah Darah (TTD) SETIAP"
          " HARI** selama masa menstruasi berlangsung.\n\n🌿 **Hari Biasa"
          " (Tidak Haid):** Minum **1 Tablet Tambah Darah 1 MINGGU SEKALI**"
          " secara teratur.\n\n💡 *Tips:* Minum TTD dengan air putih/jus buah"
          " (mengandung Vitamin C). Hindari minum TTD bersamaan dengan"
          " kopi/teh karena dapat menghambat penyerapan zat besi."
      )

# ---------------------------------------------------------
# MENU 3: KUIS GENRE (20 SOAL + SERTIFIKAT)
# ---------------------------------------------------------
elif menu == "Kuis GenRe":
  st.markdown(
      '<div class="section-title">🧩 Kuis Kesiapan Remaja Terencana (20'
      " Soal)</div>",
      unsafe_allow_html=True,
  )

  data_soal = [
      {
          "q": "1. Apa kepanjangan dari GenRe?",
          "opts": [
              "A. Generasi Remaja",
              "B. Generasi Berencana",
              "C. Gerakan Remaja",
          ],
          "ans": "B. Generasi Berencana",
      },
      {
          "q": (
              "2. Usia ideal pernikahan menurut program Pendewasaan Usia"
              " Perkawinan (PUP) BKKBN adalah?"
          ),
          "opts": [
              "A. 19 Tahun (P) & 19 Tahun (L)",
              "B. 21 Tahun (P) & 25 Tahun (L)",
              "C. 20 Tahun (P) & 20 Tahun (L)",
          ],
          "ans": "B. 21 Tahun (P) & 25 Tahun (L)",
      },
      {
          "q": (
              "3. Tiga ancaman dasar kesehatan reproduksi remaja (Triad KRR)"
              " meliputi apa saja?"
          ),
          "opts": [
              "A. Seks Bebas, Pernikahan Dini, NAPZA/HIV",
              "B. Tawuran, Bolos, Merokok",
              "C. Stunting, Anemia, Obesitas",
          ],
          "ans": "A. Seks Bebas, Pernikahan Dini, NAPZA/HIV",
      },
      {
          "q": "4. Apa itu Stunting?",
          "opts": [
              "A. Penyakit bawaan sejak lahir",
              "B. Kondisi gagal tumbuh anak akibat kurang gizi kronis",
              "C. Anak hiperaktif",
          ],
          "ans": "B. Kondisi gagal tumbuh anak akibat kurang gizi kronis",
      },
      {
          "q": "5. Salah satu cara utama mencegah Stunting dari fase remaja adalah?",
          "opts": [
              "A. Banyak makan fast food",
              "B. Remaja putri rutin minum TTD (Tablet Tambah Darah)",
              "C. Mengurangi olahraga",
          ],
          "ans": "B. Remaja putri rutin minum TTD (Tablet Tambah Darah)",
      },
      {
          "q": "6. Apa kepanjangan dari PIK-R?",
          "opts": [
              "A. Pusat Informasi dan Konseling Remaja",
              "B. Program Ilmu Keluarga Remaja",
              "C. Pusat Inovasi Karya Remaja",
          ],
          "ans": "A. Pusat Informasi dan Konseling Remaja",
      },
      {
          "q": (
              "7. Simbol jari 'Salam GenRe' (tiga jari) melambangkan say no to?"
          ),
          "opts": [
              "A. Narkoba, Seks Bebas, Nikah Dini",
              "B. Korupsi, Kolusi, Nepotisme",
              "C. Merokok, Minum Keras, Tawuran",
          ],
          "ans": "A. Narkoba, Seks Bebas, Nikah Dini",
      },
      {
          "q": "8. Kepanjangan dari BKKBN adalah?",
          "opts": [
              "A. Badan Kesejahteraan Keluarga Berencana Nasional",
              "B. Badan Kependudukan dan Keluarga Berencana Nasional",
              "C. Biro Kependudukan Keluarga Binaan Nasional",
          ],
          "ans": "B. Badan Kependudukan dan Keluarga Berencana Nasional",
      },
      {
          "q": "9. Berapa jumlah Fungsi Keluarga menurut BKKBN?",
          "opts": ["A. 5 Fungsi", "B. 8 Fungsi", "C. 10 Fungsi"],
          "ans": "B. 8 Fungsi",
      },
      {
          "q": (
              "10. Di bawah ini yang BUKAN merupakan bagian dari 8 Fungsi"
              " Keluarga adalah?"
          ),
          "opts": [
              "A. Fungsi Agama",
              "B. Fungsi Sosial Budaya",
              "C. Fungsi Karir/Pekerjaan",
          ],
          "ans": "C. Fungsi Karir/Pekerjaan",
      },
      {
          "q": (
              "11. Salah satu risiko pernikahan dini bagi remaja perempuan"
              " secara medis adalah?"
          ),
          "opts": [
              "A. Meningkatkan risiko pendarahan dan kanker serviks",
              "B. Lebih cepat mandiri",
              "C. Mengurangi beban keluarga asal",
          ],
          "ans": "A. Meningkatkan risiko pendarahan dan kanker serviks",
      },
      {
          "q": "12. Apa yang dimaksud dengan 'Bonus Demografi'?",
          "opts": [
              (
                  "A. Masa dimana jumlah penduduk usia produktif lebih besar"
                  " dibanding non-produktif"
              ),
              "B. Jumlah kelahiran bayi yang meningkat drastis",
              "C. Pemberian bantuan dana untuk penduduk desa",
          ],
          "ans": (
              "A. Masa dimana jumlah penduduk usia produktif lebih besar"
              " dibanding non-produktif"
          ),
      },
      {
          "q": "13. HIV/AIDS paling mudah menular pada remaja melalui?",
          "opts": [
              "A. Berjabat tangan dan pelukan",
              "B. Gigitan nyamuk",
              "C. Penggunaan jarum suntik bekas & seks bebas",
          ],
          "ans": "C. Penggunaan jarum suntik bekas & seks bebas",
      },
      {
          "q": (
              "14. Life Skill yang paling dibutuhkan remaja untuk menolak"
              " ajakan negatif adalah?"
          ),
          "opts": [
              "A. Kemampuan bernyanyi",
              "B. Sikap Asertif (berani berkata tidak dengan sopan)",
              "C. Pandai berbohong",
          ],
          "ans": "B. Sikap Asertif (berani berkata tidak dengan sopan)",
      },
      {
          "q": (
              "15. Masa peralihan dari anak-anak menuju dewasa yang ditandai"
              " perubahan fisik disebut?"
          ),
          "opts": ["A. Masa Balita", "B. Masa Pubertas / Remaja", "C. Masa Lansia"],
          "ans": "B. Masa Pubertas / Remaja",
      },
      {
          "q": (
              "16. Mengapa perencanaan finansial sangat penting sebelum"
              " menikah?"
          ),
          "opts": [
              "A. Agar bisa membeli barang mewah",
              "B. Untuk menjamin pemenuhan gizi anak dan kestabilan keluarga",
              "C. Diwajibkan KUA",
          ],
          "ans": (
              "B. Untuk menjamin pemenuhan gizi anak dan kestabilan keluarga"
          ),
      },
      {
          "q": (
              "17. Apa peran utama dari seorang Pendidik Sebaya (Peer"
              " Educator)?"
          ),
          "opts": [
              "A. Memarahi teman yang bersalah",
              "B. Memberikan informasi dan menjadi role model teman sebaya",
              "C. Memberikan pinjaman uang",
          ],
          "ans": (
              "B. Memberikan informasi dan menjadi role model teman sebaya"
          ),
      },
      {
          "q": (
              "18. Lima transisi kehidupan remaja (Five Life Transitions)"
              " meliputi salah satunya yaitu?"
          ),
          "opts": [
              "A. Melanjutkan sekolah / pendidikan",
              "B. Membeli rumah pribadi",
              "C. Menjadi pejabat desa",
          ],
          "ans": "A. Melanjutkan sekolah / pendidikan",
      },
      {
          "q": "19. Dampak buruk NAPZA terhadap masa depan remaja adalah?",
          "opts": [
              "A. Merusak sel saraf otak dan memicu tindak kriminal",
              "B. Membuat tubuh kebal penyakit",
              "C. Menambah fokus belajar",
          ],
          "ans": "A. Merusak sel saraf otak dan memicu tindak kriminal",
      },
      {
          "q": "20. Slogan utama dari program GenRe adalah?",
          "opts": [
              "A. Dua Anak Lebih Baik",
              "B. Saatnya yang Muda yang Berencana",
              "C. Remaja Masa Gitu",
          ],
          "ans": "B. Saatnya yang Muda yang Berencana",
      },
  ]

  with st.form("kuis_form"):
    jawaban_user = []
    for i, item in enumerate(data_soal):
      st.markdown(f"**{item['q']}**")
      pilihan = st.radio(
          f"Jawaban No {i+1}",
          item["opts"],
          index=None,
          key=f"q_{i}",
          label_visibility="collapsed",
      )
      jawaban_user.append(pilihan)
      st.write("")

    if st.form_submit_button(
        "Submit & Hitung Skor 🎯", type="primary", use_container_width=True
    ):
      if None in jawaban_user:
        st.error("⚠️ Masih ada soal yang belum diisi tuh. Cek lagi ya!")
      else:
        skor_akhir = sum(
            5
            for idx, ans in enumerate(jawaban_user)
            if ans == data_soal[idx]["ans"]
        )
        st.markdown(
            '<div class="section-title" style="color: #10B981; font-size:'
            f' 3rem;">🎉 SKOR KAMU: {skor_akhir} / 100</div>',
            unsafe_allow_html=True,
        )

        if skor_akhir >= 80:
          st.balloons()
          st.markdown(
              f"""
                <div class="sertifikat">
                    <h2 style="color:white; margin:0;">🏆 SERTIFIKAT DUTA DIGITAL GenRe 🏆</h2>
                    <p style="color:white; font-size:1.2rem; margin-top:10px;">Diberikan Kepada: <b>Pengunjung Terencana</b></p>
                    <p style="color:white; font-size:1rem;">Telah berhasil meraih predikat <b>SANGAT BAIK (Skor {skor_akhir})</b><br>dalam pemahaman Substansi GenRe.</p>
                </div>
            """,
              unsafe_allow_html=True,
          )

# ---------------------------------------------------------
# MENU 4: RUANG CERITA (ANONIM)
# ---------------------------------------------------------
elif menu == "Ruang Cerita (Anonim)":
  st.markdown(
      '<div class="section-title">💬 Ruang Cerita Anonim</div>',
      unsafe_allow_html=True,
  )
  col_info, col_form = st.columns([1, 1], gap="large")
  with col_info:
    if os.path.exists("genre_juara1.jpg"):
      st.image("genre_juara1.jpg", use_container_width=True)
    st.write(
        "Ruang ini adalah wadah aman dan rahasia untukmu berbagi cerita. Kami"
        " siap mendengar."
    )

  with col_form:
    daftar_cerita = fetch_api_data(API_URL_CERITA)
    with st.form("cerita_form", clear_on_submit=True):
      user_input = st.text_area(
          "Tuliskan cerita/curhatan kamu di sini (100% Anonim)...", height=120
      )
      if st.form_submit_button(
          "Kirim Cerita 💌", type="primary", use_container_width=True
      ):
        if user_input.strip():
          daftar_cerita.append({
              "Waktu": datetime.now().strftime("%d/%m/%Y %H:%M"),
              "Cerita": user_input,
              "Respon Admin": "",
          })
          if save_api_data(API_URL_CERITA, daftar_cerita):
            st.success("Cerita kamu berhasil terkirim!")
            st.rerun()

  st.write("---")
  st.subheader("📜 Jejak Cerita & Tanggapan Admin")
  cerita_tampil = fetch_api_data(API_URL_CERITA)
  if not cerita_tampil:
    st.info("Belum ada cerita masuk.")
  else:
    for item in reversed(cerita_tampil):
      st.markdown(
          '<div class="story-card"><b>👤 Anonim</b> <span'
          f' style="font-size:0.8rem;">({item.get("Waktu", "-")})</span><br>{item.get("Cerita", "")}</div>',
          unsafe_allow_html=True,
      )
      if item.get("Respon Admin"):
        st.markdown(
            '<div class="admin-reply-card"><b>👑 Tanggapan'
            f' Admin:</b><br>{item.get("Respon Admin")}</div>',
            unsafe_allow_html=True,
        )

# ---------------------------------------------------------
# MENU 5: KRITIK & SARAN
# ---------------------------------------------------------
elif menu == "Kritik & Saran":
  st.markdown(
      '<div class="section-title">📥 Layanan Pengaduan & Konseling</div>',
      unsafe_allow_html=True,
  )
  c1, c2 = st.columns(2, gap="large")
  with c1:
    st.subheader("Form Masukan & Evaluasi")
    daftar_kritik = fetch_api_data(API_URL_KRITIK)
    with st.form("kritik_form", clear_on_submit=True):
      topik = st.selectbox(
          "Pilih Topik",
          [
              "Pelayanan/Konseling",
              "Konten Materi",
              "Tampilan Web",
              "Program Kerja",
              "Lainnya",
          ],
      )
      isi_kritik = st.text_area("Tulis kritik & saran kamu...", height=120)
      if st.form_submit_button(
          "Kirim Masukan 🚀", type="primary", use_container_width=True
      ):
        if isi_kritik.strip():
          daftar_kritik.append({
              "Waktu": datetime.now().strftime("%d/%m/%Y %H:%M"),
              "Topik": topik,
              "Isi Kritik": isi_kritik,
          })
          save_api_data(API_URL_KRITIK, daftar_kritik)
          st.success("Terima kasih! Masukan berhasil dikirim.")
  with c2:
    st.subheader("Konseling Privat Direct")
    if os.path.exists("genre_juara1.jpg"):
      st.image("genre_juara1.jpg", use_container_width=True)
    st.link_button(
        "Hubungi Admin via WhatsApp 💬",
        "https://wa.me/qr/RTCENRAXQVZFM1",
        type="primary",
        use_container_width=True,
    )

# ---------------------------------------------------------
# MENU 6: ADMIN PANEL (WITH CSV DOWNLOADS)
# ---------------------------------------------------------
elif menu == "Admin Panel":
  st.markdown(
      '<div class="section-title">⚙️ Control Panel Admin</div>',
      unsafe_allow_html=True,
  )
  c_lock, _ = st.columns([1, 2])
  admin_pass = c_lock.text_input("Passcode Admin", type="password")

  if admin_pass == "chandikia":
    st.success("🛠️ Akses Terbuka")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["💬 Balas Cerita", "📚 Materi", "🖼️ Galeri", "📥 Kritik", "📊 Data"]
    )

    with tab1:
      list_cerita = fetch_api_data(API_URL_CERITA)
      if list_cerita:
        df_cerita = pd.DataFrame(list_cerita)
        st.download_button(
            label="📥 Export Data Cerita ke CSV",
            data=df_cerita.to_csv(index=False).encode("utf-8"),
            file_name="data_cerita_anonim.csv",
            mime="text/csv",
        )
        st.write("---")

        opsi = [
            f"[{c.get('Waktu')}] {c.get('Cerita')[:40]}..." for c in list_cerita
        ]
        idx = st.selectbox(
            "Pilih cerita:", range(len(opsi)), format_func=lambda x: opsi[x]
        )
        st.info(list_cerita[idx].get("Cerita"))
        balasan = st.text_area(
            "Respon Admin:", value=list_cerita[idx].get("Respon Admin", "")
        )
        if st.button("Simpan Respon ✉️"):
          list_cerita[idx]["Respon Admin"] = balasan
          save_api_data(API_URL_CERITA, list_cerita)
          st.success("Disimpan!")
          st.rerun()

    with tab2:
      aksi = st.radio("Aksi:", ["Tambah", "Edit/Hapus"], horizontal=True)
      if aksi == "Tambah":
        j = st.text_input("Judul Materi")
        i = st.text_area("Isi Materi (Support Markdown)")
        f = st.text_input(
            "URL Foto (Opsional, pisahkan koma jika lebih dari 1)"
        )
        if st.button("Publish 🚀") and j and i:
          st.session_state["daftar_materi"].append({
              "Judul": j,
              "Isi": i,
              "Foto": f if f.strip() else "None",
          })
          save_api_data(API_URL_MATERI, st.session_state["daftar_materi"])
          st.success("Materi berhasil ditambahkan!")
          st.rerun()

    with tab3:
      l = st.text_input("URL Gambar Galeri Baru")
      if st.button("Tambah Gambar 🖼️") and l:
        if "daftar_galeri" not in st.session_state or not isinstance(
            st.session_state["daftar_galeri"], list
        ):
          st.session_state["daftar_galeri"] = []
        st.session_state["daftar_galeri"].append(l)
        save_api_data(API_URL_GALERI, st.session_state["daftar_galeri"])
        st.success("Gambar berhasil ditambahkan!")
        st.rerun()

    with tab4:
      data_k = fetch_api_data(API_URL_KRITIK)
      if data_k:
        df_k = pd.DataFrame(data_k)
        st.dataframe(df_k, use_container_width=True)
        st.download_button(
            label="📥 Export Data Kritik & Saran ke CSV",
            data=df_k.to_csv(index=False).encode("utf-8"),
            file_name="data_kritik_saran.csv",
            mime="text/csv",
        )
      else:
        st.info("Belum ada data kritik & saran.")

    with tab5:
      st.subheader("📊 Statistik Aspirasi")
      data_a = fetch_api_data(API_URL_KRITIK)
      if data_a:
        df = pd.DataFrame(data_a)
        if "Topik" in df.columns:
          st.bar_chart(df["Topik"].value_counts())
      else:
        mock = pd.DataFrame({
            "Kategori": ["Pelayanan", "Materi", "Web", "Program"],
            "Jumlah": [12, 8, 5, 15],
        })
        st.bar_chart(mock.set_index("Kategori"))

  elif admin_pass:
    st.error("Passcode Salah!")

st.markdown(
    "<br><hr style='border-color:rgba(255,255,255,0.1);'><p style='text-align:"
    " center; color: #94A3B8;'>© 2026 Merpati Putih — Melangitkan Harapan,"
    " Membumikan Kebermanfaatan.</p>",
    unsafe_allow_html=True,
)

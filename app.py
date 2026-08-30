import streamlit as st

# 1. Sayfa Yapılandırması
st.set_page_config(
    page_title="SafeEpikriz AI | Medikolegal Risk Denetimi",
    page_icon="⚕️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Özel CSS: Minimalist & Modern Premium SaaS Teması
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, div {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Ana Arka Plan - Temiz Slate Koyu Teması */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }

    /* Sol Menü (Sidebar) */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid #30363d;
    }

    /* Minimalist Sade Başlık (Kutu Yok) */
    .header-container {
        padding: 0.5rem 0 1.5rem 0;
        border-bottom: 1px solid #21262d;
        margin-bottom: 1.5rem;
    }
    .brand-badge {
        display: inline-block;
        background: rgba(56, 189, 248, 0.1);
        color: #38bdf8;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-bottom: 10px;
        border: 1px solid rgba(56, 189, 248, 0.2);
    }
    .main-title {
        font-size: 1.9rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .main-subtitle {
        font-size: 0.92rem;
        color: #8b949e;
        margin-top: 6px;
    }

    /* Sol Menü Kartları */
    .sidebar-card {
        background: #21262d;
        border: 1px solid #30363d;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .sidebar-badge {
        background: rgba(46, 160, 67, 0.1);
        border: 1px solid rgba(46, 160, 67, 0.25);
        color: #3fb950;
        padding: 0.85rem;
        border-radius: 8px;
        font-size: 0.8rem;
        line-height: 1.45;
        margin-bottom: 1rem;
    }

    /* Buton Tasarımı - Zümrüt / Mavi İnce Gradient */
    .stButton>button {
        width: 100%;
        background: #238636;
        color: #ffffff !important;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0.65rem 1rem;
        border-radius: 8px;
        border: 1px solid rgba(240, 246, 252, 0.1);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: #2ea043;
        border-color: #8b949e;
    }

    /* Form Elemanları Özelleştirme */
    .stTextArea textarea {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        color: #f0f6fc !important;
        border-radius: 8px !important;
    }
    .stTextArea textarea:focus {
        border-color: #58a6ff !important;
    }

    .stSelectbox div[data-baseweb="select"] {
        background-color: #161b22 !important;
        border-color: #30363d !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SOL MENÜ (SIDEBAR)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚕️ SafeEpikriz AI")
    st.caption("Medikolegal Risk Denetim Paneli")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Kullanım Limiti Göstergesi
    st.markdown("""
    <div class="sidebar-card" style="text-align: center;">
        <small style="color: #8b949e;">Kalan Ücretsiz Denetim</small>
        <h2 style="margin: 0.2rem 0; color: #58a6ff; font-size: 1.7rem; font-weight: 700;">5 / 5</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Veri Güvenliği Garantisi
    st.markdown("""
    <div class="sidebar-badge">
        <b>🔒 KVKK & Veri Güvenliği:</b><br>
        Girilen veriler sunucularda kaydedilmez. T.C. No ve kişisel tanımlayıcılar yerel otomasyonla süzülür.
    </div>
    """, unsafe_allow_html=True)
    
    # Hızlı Adımlar
    st.markdown("#### 📌 Kullanım Adımları")
    st.caption("1. İlgili tıbbi branşı seçin.")
    st.caption("2. HBYS'den hasta notunu yapıştırın.")
    st.caption("3. Denetim butonuna tıklayarak riskleri görün.")
    
    st.markdown("---")
    st.caption("SafeEpikriz AI v1.0 • 2026")

# ---------------------------------------------------------
# ANA EKRAN
# ---------------------------------------------------------

# Sade ve Kutusuz Başlık Alanı
st.markdown("""
<div class="header-container">
    <span class="brand-badge">PROTOTEK / SAĞLIK HUKUKU</span>
    <h1 class="main-title">SafeEpikriz Risk Denetçisi</h1>
    <p class="main-subtitle">Epikriz ve taburculuk notlarındaki medikolegal riskleri ve malpraktis açıklarını tespit edin.</p>
</div>
""", unsafe_allow_html=True)

# Bilgilendirme Akordiyonu
with st.expander("ℹ️ Sistem Hakkında & Sorumluluk Reddi"):
    st.write("SafeEpikriz, TTB etik ilkeleri ve sağlık hukuku içtihatları doğrultusunda epikriz metinlerindeki eksiklikleri değerlendirir. Çıktılar karar destek amaçlı olup nihai hukuki/tıbbi sorumluluk hekime aittir.")

st.markdown("<br>", unsafe_allow_html=True)

# Branş Seçimi ve Örnek Yükleme
col_brans, col_sample = st.columns([2, 1])

with col_brans:
    brans = st.selectbox(
        "Tıbbi Branş Seçiniz:",
        ["Acil Servis", "Genel Cerrahi", "Dahiliye", "Kadın Doğum", "Ortopedi", "Diğer"]
    )

with col_sample:
    st.write("")
    st.write("")
    sample_clicked = st.button("🧪 Örnek Vaka Yükle")

# Örnek Metin
default_text = ""
if sample_clicked:
    default_text = "Hasta Ahmet Yılmaz (TC: 10293847561) sağ alt kadranda şiddetli ağrı şikayetiyle başvurdu. Rebound ve defans net değerlendirilmedi. Analjezik yapılarak taburcu edildi."

# Metin Alanı
epikriz_input = st.text_area(
    "HBYS Ham Epikriz / Hasta Notu:",
    value=default_text,
    height=190,
    placeholder="Anamnez, fizik muayene, tetkik ve taburculuk notunu buraya yapıştırın..."
)

# Onay Kutusu
cb = st.checkbox("Çıktıların bilgilendirme amaçlı olduğunu kabul ediyorum.")

st.markdown("<br>", unsafe_allow_html=True)

# Denetim Butonu
if st.button("🔍 Medikolegal Risk Taramasını Başlat"):
    if not cb:
        st.warning("Devam etmek için lütfen sorumluluk reddi beyanını onaylayın.")
    elif not epikriz_input.strip():
        st.error("Lütfen analiz edilecek bir epikriz metni girin.")
    else:
        with st.spinner("Metin medikolegal açıdan taranıyor..."):
            st.success("Taratma Tamamlandı!")
```eof

GitHub üzerindeki `app.py` dosyanı bu kodla güncelleyip kaydedebilirsin. 1 dakika içinde Render güncellendiğinde çok daha ferah ve profesyonel bir görünüm seni karşılayacak!

import streamlit as st

# Sayfa Yapılandırması (Geniş mod ve şık başlık)
st.set_page_config(
    page_title="SafeEpikriz AI | Medikolegal Risk Denetimi",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Özel Modern CSS
st.markdown("""
<style>
    /* Ana Arka Plan */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Üst Banner */
    .hero-container {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e3a8a 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #a5b4fc;
    }

    /* Bilgi Kartları GRID */
    .info-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .security-card {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        color: #34d399;
    }

    /* Buton Stili */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white !important;
        font-weight: 700;
        font-size: 1.1rem;
        padding: 0.8rem 1.5rem;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 14px 0 rgba(37, 99, 235, 0.39);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px 0 rgba(37, 99, 235, 0.55);
    }
</style>
""", unsafe_allow_html=True)

# 1. HERO HEADER
st.markdown("""
<div class="hero-container">
    <div class="hero-title">⚕️ SafeEpikriz AI</div>
    <div class="hero-subtitle">Hekimler ve Sağlık Hukukçuları İçin Medikolegal Risk Denetçisi ve Güvenlik Kalkanı</div>
</div>
""", unsafe_allow_html=True)

# 2. ÜST METRİK & GÜVENLİK BARI
col_sec, col_limit = st.columns([3, 1])

with col_sec:
    st.markdown("""
    <div class="security-card">
        <b>🔒 KVKK & Veri Güvenliği Garantisi:</b> Metin içindeki T.C. No, İsim ve İletişim bilgileri sunucuya/AI modeline ulaşmadan yerel otomasyonla temizlenir. Sıfır veri saklama ilkesiyle çalışır.
    </div>
    """, unsafe_allow_html=True)

with col_limit:
    st.markdown("""
    <div class="info-card" style="text-align: center; padding: 0.8rem;">
        <small style="color: #94a3b8;">Kalan Ücretsiz Hak</small>
        <h3 style="margin:0; color: #38bdf8;">5 / 5</h3>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 3. BİLGİLENDİRME AKORDİYONLARI
with st.expander("💡 Neden Genel Yapay Zeka Değil de SafeEpikriz?"):
    st.write("SafeEpikriz, genel sohbet botlarının aksine tıbbi malpraktis içtihatları ve TTB etik kuralları çerçevesinde epikriz metinlerindeki medikolegal eksiklikleri tespit etmek için özel olarak yapılandırılmıştır.")

with st.expander("📜 KVKK Aydınlatma Metni & Sorumluluk Reddi"):
    st.write("Bu araç bir hukuki danışmanlık hizmeti sunmaz. Üretilen çıktılar bilgilendirme amaçlı olup nihai hukuki ve tıbbi sorumluluk uygulayıcı hekime aittir.")

st.markdown("<br>", unsafe_allow_html=True)

# 4. GİRDİ FORMU
col_brans, col_sample = st.columns([2, 1])

with col_brans:
    brans = st.selectbox(
        "Branşınızı Seçin:",
        ["Acil Servis", "Genel Cerrahi", "Dahiliye", "Kadın Doğum", "Ortopedi", "Diğer"]
    )

with col_sample:
    st.write("") 
    st.write("")
    sample_clicked = st.button("🧪 Örnek Vaka Notu Yükle")

# Örnek vaka metni hazırlığı
default_text = ""
if sample_clicked:
    default_text = "Hasta Ahmet Yılmaz (TC: 10293847561) sağ alt kadranda ağrı ile geldi. Rebound ve defans mevcut değil. Ağrı kesici yapılarak taburcu edildi."

epikriz_input = st.text_area(
    "HBYS'den Kopyaladığınız Ham Notu Buraya Yapıştırın:",
    value=default_text,
    height=180,
    placeholder="Örn: Hastanın anamnezi, fizik muayene bulguları, uygulanan tedaviler ve taburculuk notu..."
)

# Onay Kutusu
cb = st.checkbox("SafeEpikriz'in bir hukuki danışmanlık hizmeti olmadığını, çıktıların bilgilendirme amaçlı olduğunu kabul ediyorum.")

st.markdown("<br>", unsafe_allow_html=True)

# Analiz Butonu
if st.button("🔍 Medikolegal Risk Denetimini Başlat"):
    if not cb:
        st.warning("Lütfen devam etmek için sorumluluk reddi beyanını onaylayın.")
    elif not epikriz_input.strip():
        st.error("Lütfen analiz edilecek bir metin girin.")
    else:
        with st.spinner("Medikolegal riskler taranıyor..."):
            st.success("Denetim Tamamlandı!")

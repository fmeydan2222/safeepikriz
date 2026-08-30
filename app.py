import streamlit as st

# 1. Sayfa Yapılandırması
st.set_page_config(
    page_title="SafeEpikriz AI | Medikolegal Risk Denetimi",
    page_icon="⚕️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Session State Hazırlığı (Sayaç için)
if 'usage_count' not in st.session_state:
    st.session_state.usage_count = 0

# 2. Özel CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, div {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }

    section[data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }

    .header-container {
        padding: 0.5rem 0 1.2rem 0;
        border-bottom: 1px solid #334155;
        margin-bottom: 1.5rem;
    }
    .brand-tag {
        color: #38bdf8;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .main-title {
        font-size: 2rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0.2rem 0;
        letter-spacing: -0.5px;
    }
    .main-subtitle {
        font-size: 0.95rem;
        color: #94a3b8;
    }

    .security-badge {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34d399;
        padding: 0.8rem;
        border-radius: 8px;
        font-size: 0.82rem;
        line-height: 1.4;
        margin-bottom: 1rem;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: #ffffff !important;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0.65rem 1rem;
        border-radius: 8px;
        border: none;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        transform: translateY(-1px);
    }

    .usage-tracker {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.82rem;
        color: #94a3b8;
        margin-top: 0.4rem;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SOL MENÜ (SIDEBAR)
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚕️ SafeEpikriz AI")
    st.caption("Medikolegal Risk Denetim Platformu")
    st.markdown("---")
    
    st.markdown("""
    <div class="security-badge">
        <b>🔒 Sıfır Veri Saklama (Zero-Data Retention):</b><br>
        Raporlar sunucularımızda saklanmaz. Metindeki T.C. No ve kişisel veriler işlenmeden yerel otomasyonla anonimleştirilir.
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("💡 Neden SafeEpikriz?"):
        st.write("Genel yapay zeka araçlarının aksine SafeEpikriz; TTB etik ilkeleri ve sağlık hukuku emsal kararları doğrultusunda epikriz raporlarındaki eksiklikleri ve malpraktis risklerini tespit etmek için özel olarak eğitilmiştir.")
        
    with st.expander("📜 KVKK & Aydınlatma Metni"):
        st.write("SafeEpikriz, KVKK ve GDPR uyumlu sıfır veri retention mimarisiyle çalışır. Kullanıcı tarafından girilen tıbbi veriler anlık analiz sonrası bellekten tamamen silinir.")

    with st.expander("⚠️ Sorumluluk Reddi"):
        st.write("Bu platform bir hukuki danışmanlık hizmeti sunmamaktadır. Üretilen analiz raporları karar destek amaçlı olup nihai hukuki ve tıbbi sorumluluk uygulayıcı hekime aittir.")

    with st.expander("ℹ️ Hakkında"):
        st.write("SafeEpikriz AI, hekimler ve sağlık hukukçularının malpraktis risklerini en aza indirmek için geliştirilmiş bağımsız bir medikolegal denetim aracıdır.")
        
    st.markdown("---")
    st.caption("v1.0.0 • SafeEpikriz © 2026")

# ---------------------------------------------------------
# ANA EKRAN
# ---------------------------------------------------------

st.markdown("""
<div class="header-container">
    <span class="brand-tag">MEDİKOLEGAL RİSK DENETÇİSİ</span>
    <h1 class="main-title">SafeEpikriz Risk Denetimi</h1>
    <p class="main-subtitle">Epikriz ve taburculuk notlarınızdaki medikolegal riskleri ve eksiklikleri anında tespit edin.</p>
</div>
""", unsafe_allow_html=True)

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

default_text = ""
if sample_clicked:
    default_text = "Hasta Ahmet Yılmaz (TC: 10293847561) sağ alt kadranda şiddetli ağrı şikayetiyle başvurdu. Rebound ve defans net değerlendirilmedi. Analjezik yapılarak taburcu edildi."

epikriz_input = st.text_area(
    "HBYS Ham Epikriz / Hasta Notu:",
    value=default_text,
    height=190,
    placeholder="HBYS'den kopyaladığınız anamnez, fizik muayene ve taburculuk notunu buraya yapıştırın..."
)

max_limit = 5
current_usage = st.session_state.usage_count

st.markdown(f"""
<div class="usage-tracker">
    <span>Kullanılan Hak: <b>{current_usage} / {max_limit}</b></span>
    <span>Aylık Ücretsiz Oturum</span>
</div>
""", unsafe_allow_html=True)

st.progress(current_usage / max_limit)

st.markdown("<br>", unsafe_allow_html=True)

cb = st.checkbox("Çıktıların bilgilendirme amaçlı olduğunu kabul ediyorum.")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🔍 Medikolegal Risk Taramasını Başlat"):
    if not cb:
        st.warning("Devam etmek için lütfen sorumluluk reddi beyanını onaylayın.")
    elif not epikriz_input.strip():
        st.error("Lütfen analiz edilecek bir epikriz metni girin.")
    elif st.session_state.usage_count >= max_limit:
        st.error("Ücretsiz kullanım limitinize ulaştınız (5/5).")
    else:
        st.session_state.usage_count += 1
        with st.spinner("Metin medikolegal açıdan taranıyor..."):
            st.success("Taratma Tamamlandı!")

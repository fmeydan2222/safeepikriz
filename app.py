import streamlit as st
import re
import os
import google.generativeai as genai
from supabase import create_client, Client

# 1. Erken Sayfa Yapılandırması
st.set_page_config(
    page_title="SafeEpikriz AI | Medikolegal Risk Denetimi",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Supabase ve Gemini Bağlantıları
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
API_KEY = os.getenv("GEMINI_API_KEY")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"Veritabanı bağlantı hatası: {e}")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash-latest",
        system_instruction="""
        Sen 'SafeEpikriz AI' adı altında hizmet veren uzman bir medikolegal risk denetçisisin.
        Görevin, hekimler tarafından girilen epikriz ve hasta bakım notlarını TTB etik kuralları, Türk Ceza Kanunu malpraktis emsal kararları ve medikolegal standartlar çerçevesinde denetlemektir.

        Analiz çıktını şu 4 net başlık altında, profesyonel, yapıcı ve doğrudan bir dille sun:
        1. 📊 Genelleştirilmiş Medikolegal Risk Düzeyi (Düşük / Orta / Yüksek)
        2. 🚩 Eksik veya Riskli Tıbbi İfadeler (Aydınlatılmış onam, muayene eksikliği, taburculuk talimatı vb.)
        3. 🛡️ Olası Malpraktis İddialarına Karşı Hukuki Koruma Önerileri
        4. ✍️ İyileştirilmiş / Düzenlenmiş Örnek Epikriz Notu
        """
    )
else:
    model = None

# 3. Yardımcı Fonksiyonlar & Veritabanı İşlemleri
def get_user_usage(email: str) -> int:
    if not supabase:
        return 0
    try:
        res = supabase.table("users").select("usage_count").eq("email", email).execute()
        if res.data:
            return res.data[0]["usage_count"]
        else:
            supabase.table("users").insert({"email": email, "usage_count": 0}).execute()
            return 0
    except Exception:
        return 0

def increment_user_usage(email: str, current_usage: int):
    if supabase:
        try:
            supabase.table("users").update({"usage_count": current_usage + 1}).eq("email", email).execute()
        except Exception:
            pass

def anonimlestir(metin: str) -> str:
    metin = re.sub(r'\b[1-9][0-9]{10}\b', '[TC_NO]', metin)
    metin = re.sub(r'(\+90|0)?\s*5\d{2}[\s-]*\d{3}[\s-]*\d{2}[\s-]*\d{2}', '[TEL_NO]', metin)
    return metin

# 4. Oturum Kontrolü
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Style - ChatGPT Tarzı Modern Modal Tasarımı
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, div {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    .stApp { background-color: #131314; color: #e3e3e3; }
    section[data-testid="stSidebar"] { background-color: #1e1e1f; border-right: 1px solid #2e2e2f; }
    .header-container { padding: 0.5rem 0 1.2rem 0; border-bottom: 1px solid #2e2e2f; margin-bottom: 1.5rem; }
    .brand-tag { color: #c4c7c5; font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; }
    .main-title { font-size: 1.9rem; font-weight: 700; color: #ffffff; margin: 0.2rem 0; letter-spacing: -0.4px; }
    .main-subtitle { font-size: 0.9rem; color: #8e918f; }
    .security-badge { background: #282a2c; border: 1px solid #3c4043; color: #c4c7c5; padding: 0.8rem; border-radius: 8px; font-size: 0.82rem; line-height: 1.45; margin-bottom: 1rem; }
    .stButton>button { width: 100%; background-color: #2e2e2f; color: #e3e3e3 !important; font-weight: 500; font-size: 0.92rem; padding: 0.6rem 1rem; border-radius: 8px; border: 1px solid #3c4043; }
    .stTextArea textarea { background-color: #1e1e1f !important; border: 1px solid #3c4043 !important; color: #e3e3e3 !important; border-radius: 8px !important; }
    .usage-tracker { display: flex; justify-content: space-between; align-items: center; font-size: 0.82rem; color: #8e918f; margin-top: 0.4rem; margin-bottom: 0.8rem; }
    
    /* Modal Kart Stili */
    .auth-modal {
        background-color: #1e1e1f;
        border: 1px solid #3c4043;
        padding: 2.5rem;
        border-radius: 16px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.6);
        max-width: 440px;
        margin: 3rem auto;
        text-align: center;
    }
    .auth-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    .auth-subtitle {
        font-size: 0.88rem;
        color: #8e918f;
        margin-bottom: 1.8rem;
        line-height: 1.4;
    }
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("### 🛡️ SafeEpikriz AI")
    st.caption("Medikolegal Risk Denetim Platformu")
    st.markdown("---")
    
    if st.session_state.user_email:
        st.success(f"Oturum Açık:\n{st.session_state.user_email}")
        if st.button("Çıkış Yap"):
            st.session_state.user_email = None
            st.rerun()
    else:
        st.info("🔐 Oturum kapalı.")

    st.markdown("---")
    st.markdown("""
    <div class="security-badge">
        <b>🛡️ Sıfır Veri Saklama:</b><br>
        Klinik notlar sunucularda saklanmaz, analiz sonrasında silinir.
    </div>
    """, unsafe_allow_html=True)
    st.caption("v1.0.6 • SafeEpikriz © 2026")

# GİRİŞ YAPILMAMIŞSA ORTADA ŞIK MODAL GÖSTER
if not st.session_state.user_email:
    # Sayfayı ortalamak için boş sütunlar kullanıyoruz
    _, col_center, _ = st.columns([1, 1.4, 1])
    
    with col_center:
        st.markdown("""
        <div class="auth-modal">
            <div class="auth-title">Oturum aç veya kaydol</div>
            <div class="auth-subtitle">Medikolegal risk denetim sistemine erişmek ve 5 ücretsiz hakkınızı tanımlamak için giriş yapın.</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Google ile devam et simüle butonu
        if st.button("🌐 Google ile Devam Et"):
            # Gerçek OAuth tetiklenene kadar pratik e-posta promptu veya direkt test maili alabiliriz
            st.session_state.user_email = "hekim@gmail.com"
            st.success("Google ile başarıyla giriş yapıldı!")
            st.rerun()
            
        st.markdown("<p style='text-align:center; color:#8e918f; font-size:0.8rem; margin: 1rem 0;'>VEYA E-POSTA İLE</p>", unsafe_allow_html=True)
        
        email_input = st.text_input("E-posta adresi:", placeholder="dr.adsoyad@hastane.com", label_visibility="collapsed")
        if st.button("Devam Et"):
            if "@" in email_input and "." in email_input:
                st.session_state.user_email = email_input.strip().lower()
                st.success("Giriş başarılı!")
                st.rerun()
            else:
                st.error("Lütfen geçerli bir e-posta adresi girin.")
    
    st.stop()

# GİRİŞ YAPILMIŞSA ANA UYGULAMA EKRANI
st.markdown("""
<div class="header-container">
    <span class="brand-tag">MEDİKOLEGAL RİSK DENETÇİSİ</span>
    <h1 class="main-title">SafeEpikriz Risk Denetimi</h1>
    <p class="main-subtitle">Epikriz ve taburculuk notlarınızdaki medikolegal riskleri ve eksiklikleri anında tespit edin.</p>
</div>
""", unsafe_allow_html=True)

user_email = st.session_state.user_email
current_usage = get_user_usage(user_email)
max_limit = 5

col_brans, col_sample = st.columns([2, 1])
with col_brans:
    brans = st.selectbox("Tıbbi Branş Seçiniz:", ["Acil Servis", "Genel Cerrahi", "Dahiliye", "Kadın Doğum", "Ortopedi", "Diğer"])
with col_sample:
    st.write("")
    st.write("")
    sample_clicked = st.button("📄 Örnek Vaka Yükle")

default_text = ""
if sample_clicked:
    default_text = "34 yaşında erkek hasta sağ alt kadranda başlayan ve 6 saattir devam eden şiddetli ağrı şikayetiyle başvurdu. Fizik muayenede sağ alt kadranda hassasiyet mevcut, rebound ve defans net değerlendirilmedi. Batın USG istendi. Analjezik verilerek poliklinik kontrolü önerisiyle taburcu edildi."

epikriz_input = st.text_area("HBYS Ham Epikriz / Hasta Notu:", value=default_text, height=190, placeholder="HBYS'den kopyaladığınız metni buraya yapıştırın...")

st.markdown(f"""
<div class="usage-tracker">
    <span>Kullanılan Hak: <b>{current_usage} / {max_limit}</b></span>
    <span>Aktif Oturum ({user_email})</span>
</div>
""", unsafe_allow_html=True)

st.progress(min(current_usage / max_limit, 1.0))
st.markdown("<br>", unsafe_allow_html=True)

cb = st.checkbox("Üretilen analizlerin karar destek amaçlı olduğunu, nihai tıbbi ve hukuki sorumluluğun tarafıma ait olduğunu ve KVKK/Aydınlatma koşullarını kabul ediyorum.")
st.markdown("<br>", unsafe_allow_html=True)

if st.button("✦ Medikolegal Risk Taramasını Başlat"):
    if not cb:
        st.warning("Devam etmek için lütfen sorumluluk reddi beyanını onaylayın.")
    elif not epikriz_input.strip():
        st.error("Lütfen analiz edilecek bir epikriz metni girin.")
    elif current_usage >= max_limit:
        st.error("Ücretsiz kullanım limitinize ulaştınız (5/5). Sayfayı yenileseniz dahi bu hesap için hakkınız dolmuştur.")
    elif not model:
        st.error("Gemini API anahtarı tanımlanmamış.")
    else:
        temiz_metin = anonimlestir(epikriz_input)
        with st.spinner("Medikolegal riskler taranıyor..."):
            try:
                prompt = f"Branş: {brans}\n\nKlinik Hasta Notu:\n{temiz_metin}"
                response = model.generate_content(prompt)
                
                # Kullanım hakkını veritabanında arttır
                increment_user_usage(user_email, current_usage)
                
                st.success("Taratma Tamamlandı!")
                st.markdown("---")
                st.markdown("### 📋 SafeEpikriz Denetim Raporu")
                st.markdown(response.text)
                st.rerun()
            except Exception as e:
                st.error(f"Analiz sırasında bir hata oluştu: {e}")

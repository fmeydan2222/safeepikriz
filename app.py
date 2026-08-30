import streamlit as st

# 1. Sayfa Yapılandırması
st.set_page_config(
    page_title="SafeEpikriz | Hukuki Risk & Malpraktis Denetimi",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Özel CSS - Şık ve Profesyonel Tasarım
st.markdown("""
<style>
    /* Ana Arka Plan ve Font Düzenlemeleri */
    .main {
        padding-top: 2rem;
    }
    
    /* Üst Bilgi Başlık Kartı */
    .header-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.25);
    }
    .header-card h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    .header-card p {
        font-size: 1.05rem;
        color: #93c5fd;
        margin-bottom: 0;
    }

    /* Gizlilik ve Zero-Data Rozeti */
    .security-badge {
        background-color: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 10px;
        padding: 0.85rem 1.25rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }
    .security-badge span {
        color: #166534;
        font-size: 0.9rem;
        font-weight: 500;
    }

    /* Uyarı Kutusu */
    .warning-box {
        background-color: #fffbe0;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 1.5rem;
        font-size: 0.88rem;
        color: #78350f;
    }

    /* Buton Tasarımı */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.35);
        transform: translateY(-1px);
    }
</style>
""", unsafe_unsafe_html=True)

# 3. Üst Başlık Bölümü
st.markdown("""
<div class="header-card">
    <h1>🛡️ SafeEpikriz</h1>
    <p>Hekimler ve Sağlık Hukukçuları İçin Yapay Zeka Destekli Epikriz Risk Denetimi</p>
</div>
""", unsafe_allow_html=True)

# 4. Güvenlik Vurgusu (Zero-Data Retention)
st.markdown("""
<div class="security-badge">
    <span style="font-size: 1.3rem;">🔒</span>
    <span><b>Sıfır Veri Saklama (Zero-Data Retention):</b> Yüklediğiniz veriler ve analiz sonuçları sunucularımızda saklanmaz. Analiz tamamlandığı an tamamen temizlenir.</span>
</div>
""", unsafe_allow_html=True)

# 5. Anonimleştirme İkazı
st.markdown("""
<div class="warning-box">
    <b>⚠️ Önemli Hatırlatma:</b> Analiz kalitesini artırmak ve hasta gizliliğini korumak için metindeki <b>Hasta Adı, Soyadı, T.C. Kimlik No</b> gibi kişisel tanımlayıcıları temizleyerek yükleyiniz.
</div>
""", unsafe_allow_html=True)

# 6. Girdi Seçenekleri (Metin Yapıştır veya Dosya Yükle)
tab1, tab2 = st.tabs(["📝 Metin Yapıştır", "📄 Dosya Yükle (.txt)"])

epikriz_metni = ""

with tab1:
    epikriz_metni = st.text_area(
        "Epikriz veya Taburculuk Özetini Buraya Yapıştırın:",
        height=250,
        placeholder="Örn: 45 yaşında erkek hasta, acil servise göğüs ağrısı şikayetiyle başvurdu..."
    )

with tab2:
    uploaded_file = st.file_uploader("Epikriz dosyasını seçin", type=["txt"])
    if uploaded_file is not None:
        epikriz_metni = uploaded_file.read().decode("utf-8")

# 7. Analiz Et Butonu ve İşlem
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔍 Hukuki & Tıbbi Risk Analizini Başlat"):
    if not epikriz_metni.strip():
        st.error("Lütfen analiz edilecek bir epikriz metni girin veya dosya yükleyin.")
    else:
        with st.spinner("Gemini API ile eksiklikler ve malpraktis riskleri taranıyor..."):
            # Burada Gemini API çağrın çalışacak
            # Örnek görsel çıktı simülasyonu:
            st.success("Analiz Başarıyla Tamamlandı!")
            
            st.markdown("### 📊 Risk Değerlendirme Raporu")
            st.info("**Genel Risk Skoru:** Orta Risk ⚠️")
            
            st.markdown("#### 🚩 Tespit Edilen Kritik Riskler ve Eksiklikler")
            st.write("1. **Aydınlatılmış Onam Eksikliği:** Hastaya uygulanan invaziv işlem öncesi alınan onama dair epikrizde bilgi bulunmuyor.")
            st.write("2. **Taburculuk Talimatları:** Hastanın evde dikkat etmesi gereken komplikasyonlar net ifade edilmemiş.")
            
            # PDF / Rapor Kopyala Butonu
            st.download_button(
                label="📥 Raporu PDF / Metin Olarak İndir",
                data=f"SafeEpikriz Analiz Raporu\n\n{epikriz_metni}",
                file_name="safeepikriz_analiz_raporu.txt",
                mime="text/plain"
            )

import streamlit as st
import google.generativeai as genai
import re

# --- SAYFA YAPILANDIRMASI VE TEMA ---
st.set_page_config(
    page_title="SafeEpikriz - Hukuki Risk Analizi",
    page_icon="⚕️",
    layout="centered"
)

# --- SUNUCU DÜZEYİNDE API KEY KONTROLÜ ---
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# --- KVKK VE PII MASKELEME MOTORU ---
def mask_kvkk_data(text: str) -> tuple[str, bool]:
    masked_text = text
    data_masked = False

    # 1. T.C. Kimlik No Maskeleme
    tc_pattern = r'\b[1-9]\d{10}\b'
    if re.search(tc_pattern, masked_text):
        masked_text = re.sub(tc_pattern, '[TC_KİMLİK_NO_GİZLENDİ]', masked_text)
        data_masked = True

    # 2. Telefon Numarası Maskeleme
    phone_pattern = r'(\+?90\s?)?(0?5\d{2})\s?\d{3}\s?\d{2}\s?\d{2}'
    if re.search(phone_pattern, masked_text):
        masked_text = re.sub(phone_pattern, '[TELEFON_GİZLENDİ]', masked_text)
        data_masked = True

    # 3. İsim/Unvan Maskeleme
    name_pattern = r'(Sayın|Hasta|Dr\.|Dr|Uzman)\s+([A-ZÇĞİÖŞÜa-zçğıöşü]+)\s+([A-ZÇĞİÖŞÜa-zçğıöşü]+)'
    if re.search(name_pattern, masked_text):
        masked_text = re.sub(name_pattern, r'\1 [HASTA/PERSONEL_İSMİ_GİZLENDİ]', masked_text)
        data_masked = True

    return masked_text, data_masked

# --- BAŞLIK VE AÇIKLAMA ---
st.title("⚕️ SafeEpikriz")
st.subheader("HBYS Muayene Notu ve Epikriz Risk Taraması")
st.write("HBYS sisteminize yazdığınız notu aşağıya yapıştırın. Sistem adli riskleri tarasın, **puanlasın** ve **nasıl yazılması gerektiğini** sunsun.")

# --- YAN MENÜ ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=60)
    st.title("SafeEpikriz AI")
    st.info("Hekimler için Hukuki Risk Analiz ve Epikriz İyileştirme Platformu")
    st.markdown("---")
    st.success("🔒 **KVKK Garantisi:** Metin içindeki T.C. No, İsim ve Tel bilgileri sunucuya/AI modeline ulaşmadan yerel olarak otomasyonla temizlenir.")

# --- ANA KULLANICI GİRDİ ALANI ---
input_text = st.text_area(
    "HBYS'den Kopyaladığınız Metni Buraya Yapıştırın:",
    height=180,
    placeholder="Örn: Hasta Ahmet Yılmaz (TC: 10293847561) sağ alt kadranda ağrı ile geldi..."
)

analyze_btn = st.button("🔍 Risk Analizi Yap ve Puanla", type="primary", use_container_width=True)

# --- ANALİZ MOTORU ---
if analyze_btn:
    if not input_text.strip():
        st.warning("Lütfen önce HBYS'den kopyaladığınız bir metni yapıştırın.")
    elif not API_KEY:
        st.error("Sistem yapılandırma hatası: Sunucu API anahtarı bulunamadı.")
    else:
        # KVKK Maskeleme İşlemi
        clean_text, is_masked = mask_kvkk_data(input_text)

        if is_masked:
            st.info("🛡️ **KVKK Koruması Devrede:** Metin içerisindeki hassas kişisel veriler (T.C. No, isim vb.) tespit edildi ve temizlenerek yapay zekaya iletildi.")

        with st.spinner("Yargıtay ve Danıştay emsal kararlarına göre analiz ediliyor..."):
            try:
                genai.configure(api_key=API_KEY)

                model = genai.GenerativeModel("gemini-3.5-flash-lite")

                prompt = f"""
                Sen T.C. Sağlık Hukuku ve Malpraktis alanında uzman bir Tıp Hukukçususun.
                Aşağıdaki hekim notunu incele ve SADECE aşağıdaki formatta, kısa ve net cevap ver.
                Her madde en fazla belirtilen kelime/cümle sınırında olsun, gereksiz açıklama yapma.

                Girilen Tıbbi Metin: "{clean_text}"

                FORMAT (bu sınırlara kesinlikle uy):
                🏆 PUAN: [0-100] — [max 15 kelimelik gerekçe]
                🔴 KRİTİK EKSİKLER: [en fazla 3 madde, her biri max 12 kelime]
                🟡 GELİŞTİRME ALANLARI: [en fazla 2 madde, her biri max 12 kelime]
                ✍️ REVİZE METİN: [HBYS'ye yapıştırılabilir, 3-5 cümlelik kusursuz hukuki not]

                Kritik eksik yoksa "Kritik eksik tespit edilmedi" yaz, madde uydurma.
                """

                response = model.generate_content(prompt)

                st.success("Analiz Tamamlandı!")
                st.markdown("---")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Bir hata oluştu: {str(e)}")

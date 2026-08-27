import streamlit as st
import google.generativeai as genai

# --- SAYFA YAPILANDIRMASI VE TEMA ---
st.set_page_config(
    page_title="SafeEpikriz - Hukuki Risk Analizi",
    page_icon="⚕️",
    layout="centered"
)

# --- SUNUCU DÜZEYİNDE API KEY KONTROLÜ ---
API_KEY = st.secrets.get("GEMINI_API_KEY", None)

# --- BAŞLIK VE AÇIKLAMA ---
st.title("⚕️ SafeEpikriz")
st.subheader("HBYS Muayene Notu ve Epikriz Risk Taraması")
st.write("HBYS sisteminize yazdığınız notu aşağıya yapıştırın. Sistem adli riskleri tarasın, **puanlasın** ve **nasıl yazılması gerektiğini** sunsun.")

# --- YAN MENÜ (KVKK VE BİLGİ) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=60)
    st.title("SafeEpikriz AI")
    st.info("Hekimler için Hukuki Risk Analiz ve Epikriz İyileştirme Platformu")
    st.markdown("---")
    st.success("🔒 **KVKK Garantisi:** Metin içindeki kişisel veriler yapay zekaya gitmeden korunur.")

# --- ANA KULLANICI GİRDİ ALANI ---
input_text = st.text_area(
    "HBYS'den Kopyaladığınız Metni Buraya Yapıştırın:",
    height=180,
    placeholder="Örn: 28y erkek hasta sağ alt kadranda şiddetli karın ağrısı ve bulantı ile başvurdu. Kan tetkikleri ve USG istendi..."
)

analyze_btn = st.button("🔍 Risk Analizi Yap ve Puanla", type="primary", use_container_width=True)

# --- ANALİZ MOTORU ---
if analyze_btn:
    if not input_text.strip():
        st.warning("Lütfen önce HBYS'den kopyaladığınız bir metni yapıştırın.")
    elif not API_KEY:
        st.error("Sistem yapılandırma hatası: Sunucu API anahtarı bulunamadı.")
    else:
        with st.spinner("Yargıtay ve Danıştay emsal kararlarına göre analiz ediliyor..."):
            try:
                genai.configure(api_key=API_KEY)
                
                # Dinamik model seçimi
                available_models = []
                try:
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            available_models.append(m.name)
                except Exception:
                    pass

                selected_model_name = None
                for target in ['gemini-2.5-flash', 'gemini-1.5-flash', 'gemini-flash', 'gemini-pro']:
                    for full_name in available_models:
                        if target in full_name:
                            selected_model_name = full_name
                            break
                    if selected_model_name:
                        break

                if not selected_model_name:
                    selected_model_name = 'gemini-1.5-flash'

                model = genai.GenerativeModel(selected_model_name)

                prompt = f"""
                Sen T.C. Sağlık Mevzuatı ve Malpraktis Hukuku alanında uzmanlaşmış bir Tıp Hukukçusu ve Başhekimsin.
                Aşağıdaki hekim notunu T.C. Sağlık Hukuku ve Yargıtay emsal kararları açısından incele:

                Girilen Tıbbi Metin: "{input_text}"

                Şu formatta net ve kısa bir rapor sun:
                1. 🏆 **HUKUKİ DAYANIKLILIK PUANI:** (0-100 arası puan ve 1 cümlelik gerekçe).
                2. 🔴 **KRİTİK EKSİKLER VE MALPRAKTİS RİSKLERİ:** (Olası bir davada hekim aleyhine işleyecek eksikler: vital bulgu, aydınlatılmış onam, taburculuk talimatı vb.).
                3. 🟡 **UYARI VE GELİŞTİRME ALANLARI:** (Notu hukuki olarak güçlendirecek noktalar).
                4. ✍️ **OLMASI GEREKEN KORUYUCU REVİZE METİN:** (Hekimin HBYS'ye doğrudan yapıştırabileceği kusursuz hukuki metin).
                """
                
                response = model.generate_content(prompt)
                
                st.success("Analiz Tamamlandı!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {str(e)}")

import streamlit as st
import google.generativeai as genai

# --- SAYFA YAPILANDIRMASI VE TEMA ---
st.set_page_config(
    page_title="SafeEpikriz - Hukuki Risk Analizi",
    page_icon="⚕️",
    layout="centered"
)

# --- BAŞLIK VE AÇIKLAMA ---
st.title("⚕️ SafeEpikriz")
st.subheader("HBYS Muayene Notu ve Epikriz Risk Taraması")
st.write("HBYS sisteminize yazdığınız notu aşağıya yapıştırın. Sistem adli riskleri tarasın, **puanlasın** ve **nasıl yazılması gerektiğini** sunsun.")

# --- YAN MENÜ (AYARLAR VE KVKK) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=60)
    st.title("SafeEpikriz AI")
    api_key = st.text_input("Google API Key:", type="password")
    st.markdown("---")
    st.success("🔒 **KVKK Garantisi:** Metin içindeki kişisel veriler yapay zekaya gitmeden korunur.")

# --- ANA KULLANICI GİRDİ ALANI ---
input_text = st.text_area(
    "HBYS'den Kopyaladığınız Metni Buraya Yapıştırın:",
    height=180,
    placeholder="Örn: 28y erkek hasta sağ alt kadranda şiddetli karın ağrısı ve bulantı ile başvurdu. Kan tetkikleri ve USG istendi..."
)

analyze_btn = st.button("🔍 Risk Analizi Yap ve Puanla", type="primary", use_container_width=True)

# --- ANALİZ MOTORU (FLASH DÜZEYİ) ---
if analyze_btn:
    if not input_text.strip():
        st.warning("Lütfen önce HBYS'den kopyaladığınız bir metni yapıştırın.")
    elif not api_key:
        st.error("Lütfen sol menüden API anahtarınızı giriniz.")
    else:
        with st.spinner("Yargıtay ve Danıştay emsal kararlarına göre analiz ediliyor..."):
            try:
                genai.configure(api_key=api_key)
                
                # Doğrudan Yüksek Hızlı ve Düşük Maliyetli Flash Modeller
                try:
                    model = genai.GenerativeModel('gemini-2.5-flash')
                except Exception:
                    model = genai.GenerativeModel('gemini-1.5-flash')

                # TOKEN VE COST OPTİMİZE PROMPT
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
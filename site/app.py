import streamlit as era
import base64

# --- GOOGLE ANALYTICS ENTEGRASYONU ---
ga_code = """
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0CBHKKL3N3"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-0CBHKKL3N3');
</script>
"""
era.markdown(ga_code, unsafe_allow_html=True)
# Sayfa ayarları
st.set_page_config(page_title="Gelişmiş Kod Dönüştürücü / Code Converter", page_icon="⚙️", layout="centered")

# --- DİL SEÇİMİ (LANGUAGE SELECTION) ---
lang = st.radio("🌍 Dil / Language:", ["TR", "EN"], horizontal=True)

# Dil Sözlüğü
text = {
    "TR": {
        "title": "⚙️ Gelişmiş Kod Encode / Decode Merkezi",
        "sub": "Metinlerinizi farklı formatlara şifreleyin veya çözün.",
        "menu_label": "Dönüşüm Türünü Seçin:",
        "tab1": "🔒 ENCODE (Metinden Koda)",
        "tab2": "🔓 DECODE (Koddan Metne)",
        "placeholder_enc": "Şifrelenecek metni girin...",
        "placeholder_dec": "Çözülecek kodu girin...",
        "success_enc": "✨ Sonuç:",
        "success_dec": "🎉 Çözülen Metin:",
        "error": "🚨 Hata: Girdiğiniz kod seçtiğiniz formata uygun değil!",
        "mors_note": "✨ Mors Alfabesi Sonucu (Kelimeler arası '/' ile ayrılır):"
    },
    "EN": {
        "title": "⚙️ Advanced Code Encode / Decode Center",
        "sub": "Encrypt or decrypt your texts into different formats.",
        "menu_label": "Select Conversion Type:",
        "tab1": "🔒 ENCODE (Text to Code)",
        "tab2": "🔓 DECODE (Code to Text)",
        "placeholder_enc": "Enter text to encrypt...",
        "placeholder_dec": "Enter code to decrypt...",
        "success_enc": "✨ Result:",
        "success_dec": "🎉 Decoded Text:",
        "error": "🚨 Error: The code you entered does not match the selected format!",
        "mors_note": "✨ Morse Code Result (Words separated by '/'):"
    }
}

st.title(text[lang]["title"])
st.write(text[lang]["sub"])

# Mors Alfabesi Sözlüğü
MORSE_DICT = {
    'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.', 'G':'--.', 'H':'....',
    'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 'P':'.--.',
    'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-',
    'Y':'-.--', 'Z':'--..', '1':'.----', '2':'..---', '3':'...--', '4':'....-', '5':'.....',
    '6':'-....', '7':'--...', '8':'---..', '9':'----.', '0':'-----', ' ': '/'
}
REVERSE_MORSE = {v: k for k, v in MORSE_DICT.items()}

# Menü seçenekleri dile göre değişiyor
menu_options = ["Hexadecimal", "Binary (İkili / Binary)", "Base64", "Mors Alfabesi / Morse Code"]
menu = st.selectbox(text[lang]["menu_label"], menu_options)

# Sekmeler
tab1, tab2 = st.tabs([text[lang]["tab1"], text[lang]["tab2"]])

# --- ENCODE SEKMESİ (Telefon Uyumlu) ---
with tab1:
    # Her şeyi bir form içine alıyoruz
    with st.form(key='encode_form'):
        input_text = st.text_area(text[lang]["placeholder_enc"], key="enc_in")
        # Formun gönderilmesi için bir buton (Enter görevini bu yapacak)
        submit_encode = st.form_submit_button(label="🔒 ENCODE / DÖNÜŞTÜR")
    
    # Bilgisayarda enter'a basılınca ya da telefonda butona basılınca çalışır
    if submit_encode and input_text:
        if menu == "Hexadecimal":
            res = input_text.encode('utf-8').hex()
            formatted = " ".join([res[i:i+2] for i in range(0, len(res), 2)])
            st.success(text[lang]["success_enc"])
            st.code(formatted, language="text")
            
        elif menu == "Binary (İkili / Binary)":
            formatted = " ".join(f"{ord(c):08b}" for c in input_text)
            st.success(text[lang]["success_enc"])
            st.code(formatted, language="text")
            
        elif menu == "Base64":
            b_bytes = input_text.encode('utf-8')
            b_base64 = base64.b64encode(b_bytes)
            st.success(text[lang]["success_enc"])
            st.code(b_base64.decode('utf-8'), language="text")
            
        elif menu == "Mors Alfabesi / Morse Code":
            tr_map = str.maketrans("çğıöşüİ", "CGIOSU_")
            clean_text = input_text.upper().translate(tr_map)
            mors_res = []
            for char in clean_text:
                if char in MORSE_DICT:
                    mors_res.append(MORSE_DICT[char])
            st.success(text[lang]["mors_note"])
            st.code(" ".join(mors_res), language="text")

# --- DECODE SEKMESİ (Telefon Uyumlu) ---
with tab2:
    # Burayı da form içine alıyoruz
    with st.form(key='decode_form'):
        input_code = st.text_area(text[lang]["placeholder_dec"], key="dec_in")
        submit_decode = st.form_submit_button(label="🔓 DECODE / ÇÖZ")
        
    if submit_decode and input_code:
        try:
            if menu == "Hexadecimal":
                clean = input_code.replace(" ", "").replace("\n", "")
                st.success(text[lang]["success_dec"])
                st.info(bytes.fromhex(clean).decode('utf-8'))
                
            elif menu == "Binary (İkili / Binary)":
                parts = input_code.split()
                if len(parts) == 1 and len(parts[0]) > 8:
                    parts = [parts[0][i:i+8] for i in range(0, len(parts[0]), 8)]
                st.success(text[lang]["success_dec"])
                st.info("".join(chr(int(b, 2)) for b in parts))
                
            elif menu == "Base64":
                dec_bytes = base64.b64decode(input_code.encode('utf-8'))
                st.success(text[lang]["success_dec"])
                st.info(dec_bytes.decode('utf-8'))
                
            elif menu == "Mors Alfabesi / Morse Code":
                mors_parts = input_code.split()
                decoded_chars = []
                for b in mors_parts:
                    if b == '/':
                        decoded_chars.append(' ')
                    elif b in REVERSE_MORSE:
                        decoded_chars.append(REVERSE_MORSE[b])
                st.success(text[lang]["success_dec"])
                st.info("".join(decoded_chars))
                
        except Exception:
            st.error(text[lang]["error"])
# --- BAĞIŞ BUTONU (TEK VE AKILLI LİNK) ---
st.markdown("---")

if lang == "TR":
    button_text = "☕ Bana Bir Kahve Ismarla (Destek Ol)"
    info_text = "💡 Bu site bir öğrenci tarafından geliştirilmiştir. Destekleriniz için teşekkürler!"
else:
    button_text = "☕ Buy Me a Coffee (Support Me)"
    info_text = "💡 This tool is developed by a student. Thanks for your support!"

st.write(info_text)

# Kreosus'tan aldığın o tek linki buraya yapıştır geç, gerisini Kreosus halleder!
coffee_link = "https://kreosus.com/supportme"

# Buton tasarımı
st.markdown(
    f"""
    <a href="{coffee_link}" target="_blank" style="text-decoration: none;">
        <div style="background-color: #FFDD00; color: #000000; padding: 12px 24px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 16px; box-shadow: 2px 2px 5px rgba(0,0,0,0.2); width: fit-content; margin: 10px auto; cursor: pointer;">
            {button_text}
        </div>
    </a>
    """,
    unsafe_allow_html=True
)


import streamlit as st
import base64

# Sayfa ayarları
st.set_page_config(page_title="Gelişmiş Kod Dönüştürücü", page_icon="⚙️", layout="centered")
st.title("⚙️ Gelişmiş Kod Encode / Decode Merkezi")
st.write("Metinlerinizi farklı formatlara şifreleyin veya çözün.")

# Mors Alfabesi Sözlüğü
MORSE_DICT = {
    'A':'.-', 'B':'-...', 'C':'-.-.', 'D':'-..', 'E':'.', 'F':'..-.', 'G':'--.', 'H':'....',
    'I':'..', 'J':'.---', 'K':'-.-', 'L':'.-..', 'M':'--', 'N':'-.', 'O':'---', 'P':'.--.',
    'Q':'--.-', 'R':'.-.', 'S':'...', 'T':'-', 'U':'..-', 'V':'...-', 'W':'.--', 'X':'-..-',
    'Y':'-.--', 'Z':'--..', '1':'.----', '2':'..---', '3':'...--', '4':'....-', '5':'.....',
    '6':'-....', '7':'--...', '8':'---..', '9':'----.', '0':'-----', ' ': '/'
}
# Ters Mors Sözlüğü (Decode için)
REVERSE_MORSE = {v: k for k, v in MORSE_DICT.items()}

# Ana Menü Seçimi (Sol tarafta veya üstte görünecek şekilde)
menu = st.selectbox("Dönüşüm Türünü Seçin:", ["Hexadecimal", "Binary (İkili)", "Base64", "Mors Alfabesi"])

# Sekmeler
tab1, tab2 = st.tabs(["🔒 ENCODE (Metinden Koda)", "🔓 DECODE (Koddan Metne)"])

# --- ENCODE SEKMESİ ---
with tab1:
    input_text = st.text_area("Şifrelenecek metni girin:", key="enc_in", placeholder="Merhaba Dünya")
    
    if input_text:
        if menu == "Hexadecimal":
            res = input_text.encode('utf-8').hex()
            formatted = " ".join([res[i:i+2] for i in range(0, len(res), 2)])
            st.success("✨ Hexadecimal Sonucu:")
            st.code(formatted, language="text")
            
        elif menu == "Binary (İkili)":
            formatted = " ".join(f"{ord(c):08b}" for c in input_text)
            st.success("✨ Binary Sonucu:")
            st.code(formatted, language="text")
            
        elif menu == "Base64":
            # Base64 encode işlemi
            b_bytes = input_text.encode('utf-8')
            b_base64 = base64.b64encode(b_bytes)
            st.success("✨ Base64 Sonucu:")
            st.code(b_base64.decode('utf-8'), language="text")
            
        elif menu == "Mors Alfabesi":
            # İngilizce karakterlere uyumluluk için büyütiyoruz
            tr_map = str.maketrans("çğıöşüİ", "CGIOSU_")
            clean_text = input_text.upper().translate(tr_map)
            mors_res = []
            for char in clean_text:
                if char in MORSE_DICT:
                    mors_res.append(MORSE_DICT[char])
            st.success("✨ Mors Alfabesi Sonucu (Kelimeler arası '/' ile ayrılır):")
            st.code(" ".join(mors_res), language="text")

# --- DECODE SEKMESİ ---
with tab2:
    input_code = st.text_area("Çözülecek kodu girin:", key="dec_in", placeholder="Kod buraya...")
    
    if input_code:
        try:
            if menu == "Hexadecimal":
                clean = input_code.replace(" ", "").replace("\n", "")
                st.success("🎉 Çözülen Metin:")
                st.info(bytes.fromhex(clean).decode('utf-8'))
                
            elif menu == "Binary (İkili)":
                parts = input_code.split()
                if len(parts) == 1 and len(parts[0]) > 8:
                    parts = [parts[0][i:i+8] for i in range(0, len(parts[0]), 8)]
                st.success("🎉 Çözülen Metin:")
                st.info("".join(chr(int(b, 2)) for b in parts))
                
            elif menu == "Base64":
                dec_bytes = base64.b64decode(input_code.encode('utf-8'))
                st.success("🎉 Çözülen Metin:")
                st.info(dec_bytes.decode('utf-8'))
                
            elif menu == "Mors Alfabesi":
                mors_parts = input_code.split()
                decoded_chars = []
                for b in mors_parts:
                    if b == '/':
                        decoded_chars.append(' ')
                    elif b in REVERSE_MORSE:
                        decoded_chars.append(REVERSE_MORSE[b])
                st.success("🎉 Çözülen Metin:")
                st.info("".join(decoded_chars))
                
        except Exception:
            st.error("🚨 Hata: Girdiğiniz kod seçtiğiniz formata uygun değil!")

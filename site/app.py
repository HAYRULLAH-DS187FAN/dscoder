import streamlit as st

# Sayfa ayarları ve başlık
st.set_page_config(page_title="Hex & Binary Dönüştürücü", page_icon="💻", layout="centered")
st.title("💻 Hex & Binary Encode / Decode")
st.write("Metinlerinizi Hexadecimal veya Binary formatına çevirin ya da tam tersini yapın.")

# Sekmeler (Tabs) oluşturma
tab1, tab2 = st.tabs(["🔒 ENCODE (Metinden Koda)", "🔓 DECODE (Koddan Metne)"])

# --- TAB 1: ENCODE ---
with tab1:
    st.subheader("Metni Koda Dönüştür")
    input_text = st.text_area("Dönüştürmek istediğiniz metni girin:", key="encode_input", placeholder="Merhaba Dünya!")
    
    if input_text:
        # Seçenekler
        encode_type = st.radio("Dönüşüm Türü:", ["Hexadecimal", "Binary"], key="encode_type_radio")
        
        if encode_type == "Hexadecimal":
            # Metni önce byte'a, sonra hex'e çeviriyoruz
            hex_result = input_text.encode('utf-8').hex()
            # Okunabilirliği artırmak için her 2 karakterde bir boşluk bırakalım
            formatted_hex = " ".join([hex_result[i:i+2] for i in range(0, len(hex_result), 2)])
            
            st.success("✨ Başarıyla Hexadecimal formatına dönüştürüldü:")
            st.code(formatted_hex, language="text")
            
        elif encode_type == "Binary":
            # Her karakterin binary karşılığını bulup 8 bit (1 byte) olacak şekilde formatlıyoruz
            binary_result = " ".join(f"{ord(char):08b}" for char in input_text)
            
            st.success("✨ Başarıyla Binary formatına dönüştürüldü:")
            st.code(binary_result, language="text")

# --- TAB 2: DECODE ---
with tab2:
    st.subheader("Kodu Metne Dönüştür")
    encode_type_decode = st.radio("Gireceğiniz Kod Türü:", ["Hexadecimal", "Binary"], key="decode_type_radio")
    
    input_code = st.text_area(
        "Çözmek istediğiniz kodu girin (Karakterler arasında boşluk bırakabilirsiniz):", 
        key="decode_input",
        placeholder="Örn (Hex): 4d 65 72 68 61 62 61 \nÖrn (Binary): 01001101 01100101"
    )
    
    if input_code:
        try:
            if encode_type_decode == "Hexadecimal":
                # Boşlukları ve geçersiz karakterleri temizle
                clean_hex = input_code.replace(" ", "").replace("\n", "")
                # Hex'ten metne geri çevirme
                decoded_text = bytes.fromhex(clean_hex).decode('utf-8')
                
                st.success("🎉 Kod Başarıyla Çözüldü:")
                st.info(decoded_text)
                
            elif encode_type_decode == "Binary":
                # Boşlukları temizle ve her 8 bitlik grubu listeye al
                binary_pure = input_code.replace("\n", " ").split()
                # Eğer tek bir uzun string girildiyse (boşluksuz), her 8 karakterde bir böl
                if len(binary_pure) == 1 and len(binary_pure[0]) > 8:
                    binary_pure = [binary_pure[0][i:i+8] for i in range(0, len(binary_pure[0]), 8)]
                
                # Her binary bloğunu int'e, sonra karaktere çevirip birleştir
                decoded_text = "".join(chr(int(b, 2)) for b in binary_pure)
                
                st.success("🎉 Kod Başarıyla Çözüldü:")
                st.info(decoded_text)
                
        except Exception as e:
            st.error("🚨 Hata: Lütfen girdiğiniz kodun doğruluğundan ve seçtiğiniz türün (Hex/Binary) doğru olduğundan emin olun.")

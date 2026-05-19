import streamlit as era
import base64

# --- SAYFA AYARLARI ---
era.set_page_config(page_title="Code Converter", page_icon="🔒", layout="centered")

# --- MORS SÖZLÜKLERİ ---
MORSE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
    'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
    'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
    'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ' ': '/'
}
REVERSE_MORSE = {v: k for k, v in MORSE_DICT.items()}

# --- DİL SÖZLÜĞÜ (TR / EN) ---
text = {
    "TR": {
        "title": "🔒 Şifreleme & Kod Dönüştürücü",
        "subtitle": "Metinlerinizi Hex, Binary, Base64 ve Mors alfabesine dönüştürün veya çözün.",
        "select_lang": "Dil Seçin / Select Language",
        "choose_op": "Dönüşüm Türünü Seçin",
        "tab_enc": "🔒 ENCODE (Kodla)",
        "tab_dec": "🔓 DECODE (Çöz)",
        "placeholder_enc": "Dönüştürmek istediğiniz metni buraya yazın...",
        "placeholder_dec": "Çözmek istediğiniz şifreli kodu buraya yapıştırın...",
        "success_enc": "Successfully Encoded / Başarıyla Kodlandı:",
        "success_dec": "Successfully Decoded / Başarıyla Çözüldü:",
        "mors_note": "Not: Türkçe karakterler otomatik olarak dönüştürülmüştür.",
        "error": "Hata! Lütfen girdiğiniz kodun doğruluğunu ve seçtiğiniz türü kontrol edin.",
        "btn_enc": "🔒 ENCODE / DÖNÜŞTÜR",
        "btn_dec": "🔓 DECODE / ÇÖZ",
        "btn_text": "👁️‍🗨️ [ DESTEK_OL : ORHAN'A BİR KAHVE FIRLAT ]",
        "info_text": "💡 // ENİMASYON NOTU: Bu site öğrenci bütçesiyle toplandı. Boş ders bitmeden destek atın eşşekler! :D",
        "comments_title": "💬 Ziyaretçi Defteri & Düşünceleriniz"
    },
    "EN": {
        "title": "🔒 Cipher & Code Converter",
        "subtitle": "Convert or decode your texts into Hex, Binary, Base64, and Morse code.",
        "select_lang": "Dil Seçin / Select Language",
        "choose_op": "Choose Conversion Type",
        "tab_enc": "🔒 ENCODE",
        "tab_dec": "🔓 DECODE",
        "placeholder_enc": "Type the text you want to convert here...",
        "placeholder_dec": "Paste the encoded code you want to decode here...",
        "success_enc": "Successfully Encoded:",
        "success_dec": "Successfully Decoded:",
        "mors_note": "Note: Characters have been converted to standard alphabet.",
        "error": "Error! Please check the validity of your code and the selected type.",
        "btn_enc": "🔒 ENCODE / CONVERT",
        "btn_dec": "🔓 DECODE / DECRYPT",
        "btn_text": "👁️‍🗨️ [ SUPPORT : FLING A COFFEE TO ORHAN ]",
        "info_text": "💡 // ANIMATION NOTE: Developed on a student budget. Support before the chaos begins! (International credit/debit cards are accepted. Currency will be converted automatically.)",
        "comments_title": "💬 Guestbook & Your Thoughts"
    }
}

# --- ÜST KISIM VE DİL SEÇİMİ ---
lang = era.radio("Language / Dil", ["TR", "EN"], horizontal=True, label_visibility="collapsed")

era.title(text[lang]["title"])
era.write(text[lang]["subtitle"])
era.markdown("---")

# --- MENÜ SEÇİMİ ---
menu = era.selectbox(
    text[lang]["choose_op"],
    ["Hexadecimal", "Binary (İkili / Binary)", "Base64", "Mors Alfabesi / Morse Code"]
)

# --- SEKMELER (TABS) ---
tab1, tab2 = era.tabs([text[lang]["tab_enc"], text[lang]["tab_dec"]])

# --- ENCODE SEKMESİ (Telefon Uyumlu Form Yapısı) ---
with tab1:
    with era.form(key='encode_form'):
        input_text = era.text_area(text[lang]["placeholder_enc"], key="enc_in")
        submit_encode = era.form_submit_button(label=text[lang]["btn_enc"])
    
    if submit_encode and input_text:
        if menu == "Hexadecimal":
            res = input_text.encode('utf-8').hex()
            formatted = " ".join([res[i:i+2] for i in range(0, len(res), 2)])
            era.success(text[lang]["success_enc"])
            era.code(formatted, language="text")
            
        elif menu == "Binary (İkili / Binary)":
            formatted = " ".join(f"{ord(c):08b}" for c in input_text)
            era.success(text[lang]["success_enc"])
            era.code(formatted, language="text")
            
        elif menu == "Base64":
            b_bytes = input_text.encode('utf-8')
            b_base64 = base64.b64encode(b_bytes)
            era.success(text[lang]["success_enc"])
            era.code(b_base64.decode('utf-8'), language="text")
            
        elif menu == "Mors Alfabesi / Morse Code":
            tr_map = str.maketrans("çğıöşüİ", "CGIOSU_")
            clean_text = input_text.upper().translate(tr_map)
            mors_res = []
            for char in clean_text:
                if char in MORSE_DICT:
                    mors_res.append(MORSE_DICT[char])
            era.success(text[lang]["mors_note"])
            era.code(" ".join(mors_res), language="text")

# --- DECODE SEKMESİ (Telefon Uyumlu Form Yapısı) ---
with tab2:
    with era.form(key='decode_form'):
        input_code = era.text_area(text[lang]["placeholder_dec"], key="dec_in")
        submit_decode = era.form_submit_button(label=text[lang]["btn_dec"])
        
    if submit_decode and input_code:
        try:
            if menu == "Hexadecimal":
                clean = input_code.replace(" ", "").replace("\n", "")
                era.success(text[lang]["success_dec"])
                era.info(bytes.fromhex(clean).decode('utf-8'))
                
            elif menu == "Binary (İkili / Binary)":
                parts = input_code.split()
                if len(parts) == 1 and len(parts[0]) > 8:
                    parts = [parts[0][i:i+8] for i in range(0, len(parts[0]), 8)]
                era.success(text[lang]["success_dec"])
                era.info("".join(chr(int(b, 2)) for b in parts))
                
            elif menu == "Base64":
                dec_bytes = base64.b64decode(input_code.encode('utf-8'))
                era.success(text[lang]["success_dec"])
                era.info(dec_bytes.decode('utf-8'))
                
            elif menu == "Mors Alfabesi / Morse Code":
                mors_parts = input_code.split()
                decoded_chars = []
                for b in mors_parts:
                    if b == '/':
                        decoded_chars.append(' ')
                    elif b in REVERSE_MORSE:
                        decoded_chars.append(REVERSE_MORSE[b])
                era.success(text[lang]["success_dec"])
                era.info("".join(decoded_chars))
                
        except Exception:
            era.error(text[lang]["error"])

# --- DS_187 (ORHAN) TARZI ENİMASYON BAĞIŞ BUTONU ---
era.markdown("---")
era.markdown(f"<p style='color: #FF0033; font-family: 'Impact', sans-serif; font-size: 14px; text-align: center; letter-spacing: 1px;'>{text[lang]['info_text']}</p>", unsafe_allow_html=True)

# KREOSUS LİNKİN (Bunu değiştir gardaşım)
coffee_link = "https://kreosus.com/KULLANICI_ADIN"

era.markdown(
    f"""
    <style>
        .ds187-orhan-btn {{
            background-color: #111111;
            color: #FF0033;
            border: 3px solid #FF0033;
            padding: 14px 28px;
            border-radius: 0px;
            text-align: center;
            font-family: 'Impact', Charcoal, sans-serif;
            font-weight: bold;
            font-size: 18px;
            letter-spacing: 1px;
            width: fit-content;
            margin: 15px auto;
            cursor: pointer;
            transition: all 0.15s ease-in-out;
            box-shadow: 5px 5px 0px #550011;
        }}
        .ds187-orhan-btn:hover {{
            background-color: #FF0033;
            color: #111111;
            box-shadow: -5px -5px 0px #550011;
            transform: translate(5px, 5px);
        }}
    </style>
    <a href="{coffee_link}" target="_blank" style="text-decoration: none;">
        <div class="ds187-orhan-btn">
            {text[lang]['btn_text']}
        </div>
    </a>
    """,
    unsafe_allow_html=True
)

# --- YORUM ALANI (GUESTBOOK) ---
era.markdown("---")
era.subheader(text[lang]["comments_title"])

# GitHub entegrasyonu ile reklamsız, temiz yorum alanı (Utterances)
# !!! REPO KISMINI KENDİ KULLANICI ADIN VE DEPO ADINLA DEĞİŞTİR !!!
# Örnek: repo="HAYRULLAH-DS187FAN/dscoder"
html_comments = """
<script src="https://utteranc.es/client.js"
        repo="KULLANICI_ADIN/DEPO_ADIN"
        issue-term="pathname"
        theme="github-dark"
        crossorigin="anonymous"
        async>
</script>
"""
era.markdown(html_comments, unsafe_allow_html=True)

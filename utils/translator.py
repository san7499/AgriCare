# --------------------------------------------------
# Simple Offline Translator (English → Marathi)
# --------------------------------------------------

TRANSLATIONS = {

    # 🌽 CORN
    "Corn Blight": "मका करपा",
    "Corn Common Rust": "मक्याचा सामान्य गंज",
    "Corn Gray Leaf Spot": "मक्यावरील करड्या ठिपक्यांचा रोग",
    "Corn Healthy": "मका निरोगी",

    # 🍇 GRAPE
    "Grape Black rot": "द्राक्ष काळा कुज",
    "Grape Esca": "द्राक्ष एस्का रोग",
    "Grape Leaf blight": "द्राक्ष पान करपा",
    "Grape healthy": "द्राक्ष निरोगी",

    # 🥭 MANGO
    "Mango Gall Midge": "आंबा गॉल मिज",
    "Mango Healthy": "आंबा निरोगी",
    "Mango Powdery Mildew": "आंबा भुरी रोग",
    "Mango Sooty Mould": "आंबा काळी बुरशी",

    # 🥜 PEANUT
    "Peanut early leaf spot": "भुईमूग लवकर पान डाग",
    "Peanut early rust": "भुईमूग लवकर गंज",
    "Peanut healthy leaf": "भुईमूग निरोगी",
    "Peanut late leaf spot": "भुईमूग उशिरा पान डाग",
    "Peanut nutrition deficiency": "भुईमूग पोषण कमतरता",
    "Peanut rust": "भुईमूग गंज",

    # 🌶️ PEPPER
    "Pepper bell Bacterial spot": "ढोबळी मिरची जिवाणू डाग",
    "Pepper bell healthy": "ढोबळी मिरची निरोगी",

    # 🥔 POTATO
    "Potato Early blight": "बटाटा लवकर करपा",
    "Potato Late blight": "बटाटा उशिरा करपा",
    "Potato healthy": "बटाटा निरोगी",

    # 🍅 TOMATO
    "Tomato Bacterial spot": "टोमॅटो जिवाणू डाग",
    "Tomato Early blight": "टोमॅटो लवकर करपा",
    "Tomato Late blight": "टोमॅटो उशिरा करपा",
    "Tomato Leaf Mold": "टोमॅटो पान बुरशी",
    "Tomato Septoria leaf spot": "टोमॅटो सेप्टोरिया डाग",
    "Tomato Spider mites Two spotted spider mite": "टोमॅटो कोळी किड",
    "Tomato Target Spot": "टोमॅटो टार्गेट डाग",
    "Tomato Tomato YellowLeaf Curl Virus": "टोमॅटो पिवळा पान गुंडाळी विषाणू",
    "Tomato Tomato mosaic virus": "टोमॅटो मोझॅक विषाणू",
    "Tomato healthy": "टोमॅटो निरोगी"
}


def translate_text(text, lang="en"):
    """
    Translate English text to Marathi if lang='mr'
    Otherwise return original text
    """
    if not text:
        return ""

    if lang == "mr":
        return TRANSLATIONS.get(text, text)

    return text

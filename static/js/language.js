const translations = {
    en: {
        upload_tab: "Upload Image",
        camera_tab: "Capture Image",
        upload_title: "Upload Leaf Image",
        upload_btn: "Upload & Predict",
        camera_title: "Capture Leaf Image",
        capture_btn: "Capture & Predict",
        weather_title: "Current Weather",
        weather_loading: "Fetching weather...",
        prediction_title: "Prediction Result",
        status: "Status:",
        confidence: "Confidence:",
        fertilizer: "Fertilizer",
        pesticide: "Pesticide",
        organic: "Organic"
    },
    hi: {
        upload_tab: "छवि अपलोड करें",
        camera_tab: "छवि कैप्चर करें",
        upload_title: "पत्ती की छवि अपलोड करें",
        upload_btn: "अपलोड और पूर्वानुमान",
        camera_title: "पत्ती की छवि कैप्चर करें",
        capture_btn: "कैप्चर और पूर्वानुमान",
        weather_title: "मौसम",
        weather_loading: "मौसम लोड हो रहा है...",
        prediction_title: "पूर्वानुमान परिणाम",
        status: "स्थिति:",
        confidence: "विश्वास:",
        fertilizer: "उर्वरक",
        pesticide: "कीटनाशक",
        organic: "जैविक"
    },
    mr: {
        upload_tab: "प्रतिमा अपलोड",
        camera_tab: "प्रतिमा कॅप्चर",
        upload_title: "पानाची प्रतिमा अपलोड करा",
        upload_btn: "अपलोड व अंदाज",
        camera_title: "पानाची प्रतिमा कॅप्चर करा",
        capture_btn: "कॅप्चर व अंदाज",
        weather_title: "हवामान",
        weather_loading: "हवामान घेत आहे...",
        prediction_title: "अंदाज निकाल",
        status: "स्थिती:",
        confidence: "विश्वास:",
        fertilizer: "खत",
        pesticide: "कीटकनाशक",
        organic: "सेंद्रिय"
    }
};

document.getElementById("language-select").addEventListener("change", function () {
    const lang = this.value;
    document.querySelectorAll("[data-translate]").forEach(el => {
        const key = el.dataset.translate;
        if (translations[lang] && translations[lang][key]) {
            el.innerText = translations[lang][key];
        }
    });
});

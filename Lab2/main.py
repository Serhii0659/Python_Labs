import sys
from googletrans import Translator, LANGUAGES


def TransLate(text: str, lang: str) -> str:
    translator = Translator()
    try:
        target_lang = lang.lower()
        if target_lang not in LANGUAGES:
            for code, name in LANGUAGES.items():
                if name.lower() == target_lang:
                    target_lang = code
                    break
        result = translator.translate(text, dest=target_lang)
        return result.text
    except Exception as e:
        return f"Error: {str(e)}"


def LangDetect(txt: str) -> str:
    translator = Translator()
    try:
        det = translator.detect(txt)
        return f"Detected(lang={det.lang}, confidence={det.confidence})"
    except Exception as e:
        return f"Error: {str(e)}"


def CodeLang(lang: str) -> str:
    lang = lang.lower()
    if lang in LANGUAGES:
        return LANGUAGES[lang]
    for code, name in LANGUAGES.items():
        if name.lower() == lang:
            return code
    return "Error: Language not found"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        txt = sys.argv[1]
    else:
        txt = "Доброго дня. Як справи?"

    lang = "en"

    print(txt)
    print(LangDetect(txt))
    print(TransLate(txt, lang))
    print(CodeLang("En"))
    print(CodeLang("English"))

from translator_pack import mod_deep


def main():
    print("--- Демонстрація mod_deep (deep_translator + langdetect) ---")
    print(mod_deep.TransLate("Привіт світ", "uk", "it"))
    print(mod_deep.LangDetect("Buongiorno"))
    print(mod_deep.CodeLang("Italian"))
    print(mod_deep.LanguageList("screen", "Доброго ранку"))


if __name__ == "__main__":
    main()

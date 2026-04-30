from translator_pack import mod_gtrans3

def main():
    print("--- Демонстрація mod_gtrans3 (Синхронний, для Docker) ---")
    print(mod_gtrans3.TransLate("Привіт світ", "uk", "it"))
    print(mod_gtrans3.LangDetect("Buongiorno"))
    print(mod_gtrans3.CodeLang("Italian"))
    print(mod_gtrans3.LanguageList("screen", "Доброго ранку"))

if __name__ == "__main__":
    main()
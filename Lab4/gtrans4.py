import asyncio
from translator_pack import mod_gtrans4


async def main():
    print("--- Демонстрація mod_gtrans4 (Асинхронний) ---")
    print(await mod_gtrans4.TransLate("Привіт світ", "uk", "it"))
    print(await mod_gtrans4.LangDetect("Buongiorno"))
    print(await mod_gtrans4.CodeLang("Italian"))
    print(await mod_gtrans4.LanguageList("screen", "Доброго ранку"))


if __name__ == "__main__":
    asyncio.run(main())

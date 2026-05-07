from colorama import Fore, Style, init


def main() -> None:
    init(autoreset=True)

    arr = [3, 2, -7, -9, 1, 0, -2, 1, -2, 1, 2, -6, -7, -9, 0, 6, 1, 8, 4, 4, -1, 1, 12, 13]
    a = 5

    print(f"Масив {Fore.BLUE}{len(arr)}{Style.RESET_ALL} елементів:")

    formatted_elements = [f"{Fore.RED}{val}{Style.RESET_ALL}" for val in arr]
    print(" ".join(formatted_elements))

    print(f"Введіть ціле число а: {Fore.BLUE}{a}{Style.RESET_ALL}")

    neg_count = 0
    pos_count = 0
    positives = []
    negatives = []

    for num in arr:
        if num < 0:
            negatives.append(num)
            if abs(num) > a:
                neg_count += 1
        elif num > 0:
            positives.append(num)
            if num > a:
                pos_count += 1

    max_pos = max(positives) if positives else 0
    min_neg = min(negatives) if negatives else 0
    abs_min_neg = abs(min_neg)

    print(
        f"Кількість від'ємних елементів по модулю більших ніж {Fore.BLUE}{a}{Style.RESET_ALL}: {Fore.RED}{neg_count}{Style.RESET_ALL}"
    )
    print(
        f"Кількість додатних елементів більших ніж {Fore.BLUE}{a}{Style.RESET_ALL}: {Fore.RED}{pos_count}{Style.RESET_ALL}"
    )
    print(f"Найбільший додатний: {Fore.RED}{max_pos}{Style.RESET_ALL}")
    print(f"Найбільший по модулю від'ємний: {Fore.RED}{abs_min_neg}{Style.RESET_ALL}")

    if max_pos > abs_min_neg:
        print("Найбільший додатний елемент БІЛЬШЕ ніж найбільший по модулю від'ємний")
    elif max_pos < abs_min_neg:
        print("Найбільший додатний елемент МЕНШЕ ніж найбільший по модулю від'ємний")
    else:
        print("Найбільший додатний елемент ДОРІВНЮЄ найбільшому по модулю від'ємному")


if __name__ == "__main__":
    main()

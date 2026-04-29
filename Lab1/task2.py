def find_subarrays_with_sum(
    numbers: list[int], target: int
) -> tuple[list[list[int]], int]:
    found_subarrays: list[list[int]] = []
    max_length: int = 0

    n = len(numbers)
    for start in range(n):
        current_sum: int = 0
        for end in range(start, n):
            current_sum += numbers[end]

            if current_sum == target:
                subarray = numbers[start : end + 1]
                found_subarrays.append(subarray)

                if len(subarray) > max_length:
                    max_length = len(subarray)

            if current_sum > target and all(x >= 0 for x in numbers[end:]):
                if 0 not in numbers[end:]:
                    break

    return found_subarrays, max_length


def main() -> None:
    sequence: list[int] = [2, 3, 7, 2, 1, 0, 5, 2, 3, 1, 8, 4, 8]
    a_value: int = 9

    print(f"Послідовність: {', '.join(map(str, sequence))}")
    print(f"Значення a: {a_value}")

    subarrays, max_len = find_subarrays_with_sum(sequence, a_value)

    for sub in subarrays:
        print(", ".join(map(str, sub)))

    print(f"Максимальна кількість елементів: {max_len}")


if __name__ == "__main__":
    main()
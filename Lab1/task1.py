import math
import sys

def find_primes_in_range(bound_a: int, bound_b: int):
    """Генерує прості числа в заданому діапазоні, використовуючи сегментоване решето."""
    lower: int = min(bound_a, bound_b)
    upper: int = max(bound_a, bound_b)
    
    if upper < 2:
        return
    
    start: int = max(2, lower)
    limit = int(math.isqrt(upper))
    primes_to_limit = _get_small_primes(limit)
    
    segment_size = 32768 
    for low in range(start, upper + 1, segment_size):
        high = min(low + segment_size - 1, upper)
        is_prime_segment = [True] * (high - low + 1)
        
        for p in primes_to_limit:
            start_idx = (low + p - 1) // p * p
            start_idx = max(start_idx, p * p)
            
            for j in range(start_idx, high + 1, p):
                is_prime_segment[j - low] = False
        
        for i in range(len(is_prime_segment)):
            if is_prime_segment[i]:
                yield i + low

def _get_small_primes(limit: int) -> list[int]:
    """Генерує всі прості числа до заданого обмеження, використовуючи решето Ератосфена."""
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    for p in range(2, int(limit**0.5) + 1):
        if sieve[p]:
            for i in range(p * p, limit + 1, p):
                sieve[i] = False
    return [p for p in range(2, limit + 1) if sieve[p]]

def get_integer(prompt: str) -> int:
    """Безпечно отримує цілочисельне значення від користувача з обробкою помилок."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Помилка: Необхідно ввести ціле число. Спробуйте ще раз.", file=sys.stderr)

def main() -> None:
    """Точка входу в програму."""
    try:
        bound_a: int = get_integer("Введіть перше число (a): ")
        bound_b: int = get_integer("Введіть друге число (b): ")
        
        primes = list(find_primes_in_range(bound_a, bound_b))
        
        if primes:
            print(f"Прості числа: {', '.join(map(str, primes))}")
        else:
            print("У вказаному діапазоні простих чисел не знайдено.")
        
    except KeyboardInterrupt:
        print("\nВиконання перервано.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
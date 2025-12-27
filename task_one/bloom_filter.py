class BloomFilter:
    """
    A space-efficient probabilistic data structure used to test whether an element is a member of a set.
    """

    def __init__(self, size: int, num_hashes: int):
        if size <= 0 or num_hashes <= 0:
            raise ValueError("size та num_hashes мають бути позитивними числами")

        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _hashes(self, item: str):
        """
        Generate num_hashes hashes for an element.
        """
        for i in range(self.num_hashes):
            yield hash(f"{item}_{i}") % self.size

    def add(self, item: str):
        """
        Adding an element to a filter.
        """
        if not isinstance(item, str) or item == "":
            return  # Incorrect values ​​are ignored

        for index in self._hashes(item):
            self.bit_array[index] = 1

    def contains(self, item: str) -> bool:
        """
        Checking if an element is present in a filter.
        """
        if not isinstance(item, str) or item == "":
            return False

        return all(self.bit_array[index] == 1 for index in self._hashes(item))


def check_password_uniqueness(bloom_filter: BloomFilter, passwords: list[str]) -> dict:
    results = {}
    """
    Checking password uniqueness using Bloom Filter.
    """
    for password in passwords:
        if not isinstance(password, str) or password == "":
            results[password] = "некоректне значення"
            continue

        if bloom_filter.contains(password):
            results[password] = "вже використаний"
        else:
            results[password] = "унікальний"
            bloom_filter.add(password)

    return results


if __name__ == "__main__":
    # Bloom filter initialization.
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Adding existing passwords.
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Checking new passwords.
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Results.
    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")

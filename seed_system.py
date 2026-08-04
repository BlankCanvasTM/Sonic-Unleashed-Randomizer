import hashlib
import secrets
import string


SEED_ALPHABET = string.ascii_uppercase + string.digits
GENERATED_SEED_LENGTH = 12


def normalise_seed(seed: str) -> str:

    normalised = seed.strip()

    if not normalised:
        raise ValueError("Seed cannot be empty.")

    return normalised


def seed_to_integer(seed: str) -> int:

    normalised = normalise_seed(seed)

    digest = hashlib.sha256(
        normalised.encode("utf-8")
    ).digest()

    return int.from_bytes(
        digest,
        byteorder="big",
        signed=False,
    )


def generate_seed_code(
    length: int = GENERATED_SEED_LENGTH,
) -> str:
    """
    Generates a random, shareable seed code.
    """

    if length <= 0:
        raise ValueError(
            "Seed length must be greater than zero."
        )

    return "".join(
        secrets.choice(SEED_ALPHABET)
        for _ in range(length)
    )
import re
from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class ValueObject(ABC):
    """Base class for all Value Objects.
    - Immutable (frozen=True).
    - Value-based equality."""

    pass


@dataclass(frozen=True)
class CUIT(ValueObject):
    """Represents an Argentine CUIT (Clave Única de Identificación Tributaria).
    - Must have 11 digits.
    - The last digit is a verifier calculated according to the official AFIP algorithm.
    - The format may include dashes, but it is normalized to a clean value without dashes.
    """

    value: str

    def __post_init__(self):
        cuit_clean = self.value.replace("-", "").strip()

        if not re.fullmatch(r"\d{11}", cuit_clean):
            raise ValueError(f"Invalid CUIT: {self.value}")

        if not self._validate_digital_verifier(cuit_clean):
            raise ValueError(f"Invalid verifier digit for CUIT: {self.value}")

        # Rewrite value with the clean version
        object.__setattr__(self, "value", cuit_clean)

    @staticmethod
    def _validate_digital_verifier(cuit: str) -> bool:
        # Official AFIP algorithm for validating a CUIT
        coefficients = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
        digits = list(map(int, cuit))
        verifier = digits[-1]
        sum_of_products = sum([c * d for c, d in zip(coefficients, digits[:-1])])
        mod = sum_of_products % 11
        vd = 11 - mod if mod != 0 else 0
        if vd == 11:
            vd = 0
        return vd == verifier

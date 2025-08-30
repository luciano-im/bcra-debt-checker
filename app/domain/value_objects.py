import re
import uuid
from abc import ABC
from dataclasses import dataclass, field


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


@dataclass(frozen=True)
class UserId(ValueObject):
    """Represents a user ID in the system.
    - Must be a non-empty string.
    """

    value: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass(frozen=True)
class CheckNumber(ValueObject):
    """Represents a check number.
    - Must be a string of digits, typically 6 to 8 digits long.
    """

    value: str

    def __post_init__(self):
        if not self.value or len(self.value.strip()) == 0:
            raise ValueError("Check number cannot be empty")

        if not re.fullmatch(r"\d{6,8}", self.value):
            raise ValueError(f"Invalid check number: {self.value}")

        if not self.value.strip().isdigit():
            raise ValueError("Check number must contain only digits")


@dataclass(frozen=True)
class DebtPeriod(ValueObject):
    """Represents a debt period in the format 'YYYYMM'.
    - Must be a valid date format.
    """

    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Debt period cannot be empty")

        if not re.fullmatch(r"\d{4}(0[1-9]|1[0-2])", self.value):
            raise ValueError(f"Invalid debt period format: {self.value}")

        year = int(self.value[:4])
        month = int(self.value[4:])

        if year < 1900:
            raise ValueError("Year in debt period must be 1900 or later.")

        if month < 1 or month > 12:
            raise ValueError("Month in debt period must be between 01 and 12.")

    @property
    def year(self) -> int:
        return int(self.value[:4])

    @property
    def month(self) -> int:
        return int(self.value[4:])


@dataclass(frozen=True)
class EmailAddress(ValueObject):
    """Represents an email address.
    - Must be a valid email format.
    """

    value: str

    def __post_init__(self):
        if not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", self.value):
            raise ValueError(f"Invalid email address: {self.value}")


@dataclass(frozen=True)
class DebtCheckRequestId(ValueObject):
    value: int

    def __post_init__(self):
        if self.value <= 0:
            raise ValueError("DebtCheckRequestId must be a non-negative integer")

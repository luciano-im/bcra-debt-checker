import pytest

from app.domain.value_objects import (
    CUIT,
    CheckNumber,
    DebtCheckRequestId,
    DebtPeriod,
    EmailAddress,
    UserId,
)

# Tests for CUIT


def test_cuit_valido():
    cuit = CUIT("30-51170725-7")
    assert cuit.value == "30511707257"


def test_cuit_invalido_formato():
    with pytest.raises(ValueError):
        CUIT("20-1234567-3")


def test_cuit_invalido_verificador():
    with pytest.raises(ValueError):
        CUIT("20-12345678-0")


# Tests for UserId


def test_userid_default():
    user_id = UserId()
    assert isinstance(user_id.value, str)
    assert len(user_id.value) > 0


def test_userid_custom():
    user_id = UserId("custom-id")
    assert user_id.value == "custom-id"


# Tests for CheckNumber


def test_checknumber_valido():
    check = CheckNumber("123456")
    assert check.value == "123456"


def test_checknumber_invalido_formato():
    with pytest.raises(ValueError):
        CheckNumber("abc123")


def test_checknumber_vacio():
    with pytest.raises(ValueError):
        CheckNumber("")


# Tests for DebtPeriod


def test_debtperiod_valido():
    period = DebtPeriod("202501")
    assert period.year == 2025
    assert period.month == 1


def test_debtperiod_invalido_formato():
    with pytest.raises(ValueError):
        DebtPeriod("202513")


def test_debtperiod_anio_invalido():
    with pytest.raises(ValueError):
        DebtPeriod("189912")


def test_debtperiod_mes_invalido():
    with pytest.raises(ValueError):
        DebtPeriod("202500")


# Tests for EmailAddress


def test_emailaddress_valido():
    email = EmailAddress("usuario@dominio.com")
    assert email.value == "usuario@dominio.com"


def test_emailaddress_invalido_sin_arroba():
    with pytest.raises(ValueError):
        EmailAddress("usuariodominio.com")


def test_emailaddress_invalido_sin_dominio():
    with pytest.raises(ValueError):
        EmailAddress("usuario@dominio")


def test_emailaddress_invalido_vacio():
    with pytest.raises(ValueError):
        EmailAddress("")


# Tests for DebtCheckRequestId


def test_debtcheckrequestid_valido():
    obj = DebtCheckRequestId(10)
    assert obj.value == 10


def test_debtcheckrequestid_cero():
    with pytest.raises(ValueError):
        DebtCheckRequestId(0)


def test_debtcheckrequestid_negativo():
    with pytest.raises(ValueError):
        DebtCheckRequestId(-1)

import pytest
from pydantic import ValidationError

from app.schemas.token import TokenCreate


def test_minimal_valid_token_payload_applies_defaults():
    token = TokenCreate(service_type="Cash deposit")
    assert token.service_type == "Cash deposit"
    assert token.disability is False
    assert token.language_barrier == 0.0
    assert token.vulnerability_score == 0.0


def test_nic_is_trimmed_and_normalized_to_uppercase():
    token = TokenCreate(service_type="Cash", nic=" 123456789v ")
    assert token.nic == "123456789V"


def test_phone_spaces_and_dashes_are_removed():
    token = TokenCreate(service_type="Cash", phone="+94 77-123-4567")
    assert token.phone == "+94771234567"


@pytest.mark.parametrize("nic", ["12345", "123456789Z", "1234567890123"])
def test_invalid_nic_is_rejected(nic):
    with pytest.raises(ValidationError):
        TokenCreate(service_type="Cash", nic=nic)


@pytest.mark.parametrize("phone", ["077ABC1234", "123", "++94771234567"])
def test_invalid_phone_is_rejected(phone):
    with pytest.raises(ValidationError):
        TokenCreate(service_type="Cash", phone=phone)


@pytest.mark.parametrize("age", [-1, 151])
def test_age_outside_allowed_range_is_rejected(age):
    with pytest.raises(ValidationError):
        TokenCreate(service_type="Cash", age=age)


def test_unsupported_language_is_rejected():
    with pytest.raises(ValidationError):
        TokenCreate(service_type="Cash", language="french")


@pytest.mark.parametrize("score", [-0.01, 2.01])
def test_vulnerability_score_outside_allowed_range_is_rejected(score):
    with pytest.raises(ValidationError):
        TokenCreate(service_type="Cash", vulnerability_score=score)


def test_unexpected_fields_are_rejected():
    with pytest.raises(ValidationError):
        TokenCreate(service_type="Cash", unexpected=True)


@pytest.mark.xfail(
    strict=True,
    reason="BUG-001: whitespace-only service_type currently passes min_length without trimming",
)
def test_whitespace_only_service_type_is_rejected():
    with pytest.raises(ValidationError):
        TokenCreate(service_type="   ")

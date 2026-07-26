from dogfood_api import normalize_name


def test_normalize_name_strips_whitespace() -> None:
    assert normalize_name("  Ada  ") == "Ada"


def test_normalize_name_uses_fallback() -> None:
    assert normalize_name("   ") == "anonymous"

from dogfood_api import normalize_name, normalize_names


def test_normalize_name_strips_whitespace() -> None:
    assert normalize_name("  Ada  ") == "Ada"


def test_normalize_name_uses_fallback() -> None:
    assert normalize_name("   ") == "anonymous"


def test_normalize_names_preserves_order_and_input() -> None:
    names = ["  Ada  ", "   ", "Grace"]
    original_names = names.copy()

    assert normalize_names(names) == ["Ada", "anonymous", "Grace"]
    assert names == original_names


def test_normalize_names_handles_empty_input() -> None:
    assert normalize_names([]) == []

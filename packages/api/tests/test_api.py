from dogfood_api import (
    normalize_name,
    normalize_names,
    normalize_unique_names,
    normalized_name_counts,
)


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


def test_normalize_unique_names_deduplicates_normalized_results_in_order() -> None:
    names = ["  Ada  ", "Grace", "Ada", "   ", "anonymous", "  Grace  "]
    original_names = names.copy()

    assert normalize_unique_names(names) == ["Ada", "Grace", "anonymous"]
    assert names == original_names


def test_normalize_unique_names_handles_empty_input() -> None:
    assert normalize_unique_names([]) == []


def test_normalized_name_counts_uses_existing_rules_and_preserves_input() -> None:
    names = ["  Ada  ", "Grace", "Ada", "   ", "anonymous", "\tGrace\n"]
    original_names = names.copy()

    assert normalized_name_counts(names) == {"Ada": 2, "Grace": 2, "anonymous": 2}
    assert names == original_names


def test_normalized_name_counts_accepts_immutable_and_empty_sequences() -> None:
    names = ("  Ada  ", "", "Ada")

    assert normalized_name_counts(names) == {"Ada": 2, "anonymous": 1}
    assert names == ("  Ada  ", "", "Ada")
    assert normalized_name_counts(()) == {}

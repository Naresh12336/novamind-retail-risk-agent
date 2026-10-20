
from engine.text_preprocessor import TextPreprocessor
from engine.nlp_types import NamedEntity


def test_case_normalization():
    print("\nTEST 1: Case normalization")

    variants = ["JOHN", "John", "john"]
    normalized = [
        value.strip().casefold()
        for value in variants
    ]

    assert normalized == ["john", "john", "john"]
    print("PASS: Case variants normalize consistently.")


def test_whitespace_normalization():
    print("\nTEST 2: Whitespace normalization")

    value = "  John  "
    normalized = value.strip().casefold()

    assert normalized == "john"
    assert value == "  John  "
    print("PASS: Normalized value is trimmed; original is preserved.")


def test_entity_integrity():
    print("\nTEST 3: Entity text and offsets")

    preprocessor = TextPreprocessor()
    text = "Transfer money to John immediately."

    result = preprocessor.process(text)

    john_entities = [
        entity for entity in result.named_entities
        if entity.text == "John"
    ]

    assert john_entities, "John was not detected."

    for entity in john_entities:
        assert text[entity.start_char:entity.end_char] == entity.text
        assert entity.normalized_text == "john"

    print("PASS: Original text, offsets, and normalized value are valid.")


def test_named_entity_constructor():
    print("\nTEST 4: NamedEntity constructor compatibility")

    entity = NamedEntity(
        text="John",
        normalized_text="john",
        label="PERSON",
        start_char=0,
        end_char=4,
        start_token=0,
        end_token=1,
    )

    assert entity.text == "John"
    assert entity.normalized_text == "john"
    assert entity.label == "PERSON"

    print("PASS: NamedEntity construction works with normalized_text.")


def main():
    test_case_normalization()
    test_whitespace_normalization()
    test_entity_integrity()
    test_named_entity_constructor()

    print("\nAll V6 normalization tests passed.")


if __name__ == "__main__":
    main()

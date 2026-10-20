
from engine.text_preprocessor import TextPreprocessor


def main():
    preprocessor = TextPreprocessor()

    text = (
        "John reported a suspicious payment. "
        "Contact support@example.com or visit "
        "https://example.com/report."
    )

    result = preprocessor.process(text)

    print("Input:", text)
    print("\nExtracted entities:")

    for entity in result.named_entities:
        print(
            f"{entity.label}: {entity.text!r} | "
            f"Normalized: {entity.normalized_text!r} | "
            f"Offsets: ({entity.start_char}, {entity.end_char})"
        )

        assert (
            text[entity.start_char:entity.end_char] == entity.text
        ), f"Invalid offsets for {entity.text!r}"

    assert any(
        entity.text == "John" and entity.label == "PERSON"
        for entity in result.named_entities
    ), "spaCy NER did not detect John."

    assert any(
        entity.text == "support@example.com"
        and entity.label == "EMAIL"
        for entity in result.named_entities
    ), "Email extraction failed."

    assert any(
        entity.text == "https://example.com/report"
        and entity.label == "URL"
        for entity in result.named_entities
    ), "URL extraction or punctuation handling failed."

    positions = [
        entity.start_char for entity in result.named_entities
    ]

    assert positions == sorted(positions), (
        "Entities are not sorted by character position."
    )

    print("\nAll V6 integration tests passed.")


if __name__ == "__main__":
    main()


from engine.text_preprocessor import TextPreprocessor
from engine.models.preprocessing_config import PREPROCESSING_CONFIG


TEST_CASES = [
    {
        "text": "Transfer money to John immediately.",
        "expected": {"John": "PERSON"},
    },
    {
        "text": "Transfer money from John to Mumbai.",
        "expected": {
            "John": "PERSON",
            "Mumbai": "GPE",
        },
    },
    {
        "text": "John transferred ₹5000 yesterday.",
        "expected": {
            "John": "PERSON",
            "5000": "MONEY",
            "yesterday": "DATE",
        },
    },
    {
        "text": "Send money to Rahul from Chennai.",
        "expected": {
            "Rahul": "PERSON",
            "Chennai": "GPE",
        },
    },
    {
        "text": "Contact Priya about the suspicious transaction.",
        "expected": {"Priya": "PERSON"},
    },
]


def test_named_entity_recognition():
    print("\nTEST 1: Named Entity Recognition")

    preprocessor = TextPreprocessor()

    for case in TEST_CASES:
        text = case["text"]
        result = preprocessor.process(text)

        detected = {
            entity.text: entity.label
            for entity in result.named_entities
        }

        print(f"\nInput: {text}")
        print("Detected:", detected)

        for expected_text, expected_label in case["expected"].items():
            assert detected.get(expected_text) == expected_label, (
                f"Expected {expected_text!r} as {expected_label}; "
                f"got {detected.get(expected_text)!r}"
            )

        print("PASS")

    print("\nAll NER regression cases passed.")


def test_entity_offsets():
    print("\nTEST 2: Entity offset integrity")

    preprocessor = TextPreprocessor()

    for case in TEST_CASES:
        text = case["text"]
        result = preprocessor.process(text)

        for entity in result.named_entities:
            assert text[entity.start_char:entity.end_char] == entity.text, (
                f"Character offset mismatch for {entity.text!r}"
            )

            assert 0 <= entity.start_token < entity.end_token, (
                f"Invalid token offsets for {entity.text!r}"
            )

        print(f"PASS: {text}")

    print("\nAll entity offset checks passed.")



def test_ner_configuration_toggle():
    print("\nTEST 3: NER configuration toggle")

    from dataclasses import replace
    import engine.text_preprocessor as preprocessor_module

    original_config = preprocessor_module.PREPROCESSING_CONFIG

    try:
        preprocessor_module.PREPROCESSING_CONFIG = replace(
            original_config,
            linguistic=replace(
                original_config.linguistic,
                extract_named_entities=False,
            ),
        )

        preprocessor = preprocessor_module.TextPreprocessor()
        result = preprocessor.process(
            "Transfer money to John immediately."
        )

        assert result.named_entities == []
        print("PASS: NER disabled successfully.")

    finally:
        preprocessor_module.PREPROCESSING_CONFIG = original_config

    print("\nNER configuration toggle test passed.")



def main():
    test_named_entity_recognition()
    test_entity_offsets()
    test_ner_configuration_toggle()

    print("\nAll V3 NER tests passed.")


if __name__ == "__main__":
    main()

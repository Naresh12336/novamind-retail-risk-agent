
from engine.pattern_extractor import PatternExtractor


def run_case(extractor, text, expected_emails, expected_urls):
    entities = extractor.extract(text)

    emails = [
        entity for entity in entities
        if entity.label == "EMAIL"
    ]
    urls = [
        entity for entity in entities
        if entity.label == "URL"
    ]

    actual_emails = [entity.text for entity in emails]
    actual_urls = [entity.text for entity in urls]

    print(f"\nInput: {text}")
    print("Emails:", actual_emails)
    print("URLs:", actual_urls)

    assert actual_emails == expected_emails, (
        f"Expected emails {expected_emails}, got {actual_emails}"
    )
    assert actual_urls == expected_urls, (
        f"Expected URLs {expected_urls}, got {actual_urls}"
    )

    for entity in entities:
        assert (
            text[entity.start_char:entity.end_char] == entity.text
        ), f"Offset mismatch for {entity.text!r}"

    print("PASS")


def main():
    extractor = PatternExtractor()

    cases = [
        # Valid candidates
        (
            "Contact support@example.com.",
            ["support@example.com"],
            [],
        ),
        (
            "Email user+case@company.co.in",
            ["user+case@company.co.in"],
            [],
        ),
        (
            "Visit https://example.com/login",
            [],
            ["https://example.com/login"],
        ),
        (
            "Visit www.example.org/help",
            [],
            ["www.example.org/help"],
        ),

        # Multiple candidates
        (
            "Email a@example.com and b@example.org",
            ["a@example.com", "b@example.org"],
            [],
        ),
        (
            "Visit https://example.com and www.example.org",
            [],
            ["https://example.com", "www.example.org"],
        ),

        # Punctuation handling: expected to reveal current limitations
        (
            "Visit https://example.com/path.",
            [],
            ["https://example.com/path"],
        ),
        (
            "Contact support@example.com, please.",
            ["support@example.com"],
            [],
        ),

        # Malformed candidates: expected to reveal current limitations
        (
            "Invalid: support@@example.com",
            [],
            [],
        ),
        (
            "Incomplete URL: https://",
            [],
            [],
        ),
    ]

    for text, expected_emails, expected_urls in cases:
        run_case(
            extractor,
            text,
            expected_emails,
            expected_urls,
        )

    print("\nAll expanded extraction tests passed.")


if __name__ == "__main__":
    main()

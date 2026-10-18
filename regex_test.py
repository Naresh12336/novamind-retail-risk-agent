import re

from engine.models.preprocessing_config import PREPROCESSING_CONFIG


def main() -> None:
    patterns = PREPROCESSING_CONFIG.patterns

    test_text = (
        "Contact support@example.com or user.name+test@company.org. "
        "Visit https://example.com/path or www.example.org"
    )

    emails = re.findall(patterns.email_pattern, test_text)
    urls = re.findall(patterns.url_pattern, test_text)

    print("Input:", test_text)
    print("\nEmails detected:")
    for email in emails:
        print(f"  - {email}")

    print("\nURLs detected:")
    for url in urls:
        print(f"  - {url}")

    print("\nPattern validation:")
    print("Email pattern:", bool(emails))
    print("URL pattern:", bool(urls))

    assert len(emails) == 2, f"Expected 2 emails, found {len(emails)}"
    assert len(urls) == 2, f"Expected 2 URLs, found {len(urls)}"

    print("\nAll regex tests passed.")


if __name__ == "__main__":
    main()
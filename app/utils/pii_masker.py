from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# Set up the analyzer
analyzer = AnalyzerEngine()

# Set up the anonymizer
anonymizer = AnonymizerEngine()

def mask_pii(text: str) -> str:
    """
    Analyzes text to find and mask PII.
    :param text: The original text to be anonymized.
    :return: Text with PII masked.
    """
    print("--- Running PII Scan ---")

    # Analyze the text to find PII entities
    pii_entities = ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "LOCATION"]
    analyzer_results = analyzer.analyze(text=text, language='en', entities=pii_entities)

    # Anonymize the findings
    anonymized_result = anonymizer.anonymize(
        text=text,
        analyzer_results=analyzer_results
    )

    print("PII scan complete. Data has been masked.")
    return anonymized_result.text
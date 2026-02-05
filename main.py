"""
AI Legal Document Classifier - Demo Entry Point

This script demonstrates how to use the legal classifier to categorize
legal documents as Criminal or Civil cases.
"""

from legal_classifier import classify_legal_text


def main():
    """Demonstrate the legal classifier with example documents."""
    print("=" * 60)
    print("AI Legal Document Classifier")
    print("=" * 60)
    print()
    
    # Example legal documents
    examples = [
        {
            "text": "The accused stabbed the victim with a knife and fled the scene. "
                    "An FIR was registered under sections 307 and 324 IPC.",
            "label": "Expected: Criminal"
        },
        {
            "text": "The tenant refused to pay rent for 6 months despite multiple "
                    "notices. The landlord seeks eviction and recovery of dues.",
            "label": "Expected: Civil"
        },
        {
            "text": "The accused robbed the bank at gunpoint and stole Rs. 5 lakhs. "
                    "Charges filed under sections 392 and 397 IPC.",
            "label": "Expected: Criminal"
        },
        {
            "text": "The plaintiff filed suit for recovery of loan amount of Rs. 2 lakhs "
                    "with interest as per the promissory note dated 15th March 2023.",
            "label": "Expected: Civil"
        },
    ]
    
    # Classify each example
    for i, example in enumerate(examples, 1):
        print(f"Example {i}:")
        print(f"Text: {example['text'][:80]}...")
        print(f"{example['label']}")
        print()
        
        result = classify_legal_text(example["text"])
        
        print(f"✓ Classification: {result['type']}")
        print(f"  Confidence: {result['confidence']*100:.1f}%")
        print(f"  Civil Probability: {result['civil_prob']*100:.1f}%")
        print(f"  Criminal Probability: {result['criminal_prob']*100:.1f}%")
        print("-" * 60)
        print()


if __name__ == "__main__":
    main()

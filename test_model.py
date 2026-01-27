"""
test_model.py
Loads the trained civil_criminal_model and tests it with legal documents.
Provides a predict_case_type() function that returns "Criminal" or "Civil".

Handles long legal documents (up to 512 tokens).
"""

import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification


# Model path
MODEL_PATH = "./civil_criminal_model"
MAX_LENGTH = 512


def load_model():
    """Load the trained model and tokenizer."""
    try:
        print("Loading model from:", MODEL_PATH)
        tokenizer = DistilBertTokenizer.from_pretrained(MODEL_PATH)
        model = DistilBertForSequenceClassification.from_pretrained(MODEL_PATH)
        model.eval()  # Set to evaluation mode
        print("✓ Model loaded successfully!")
        return tokenizer, model
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Make sure you have trained the model by running train_classifier.py first.")
        return None, None


def predict_case_type(text: str, tokenizer=None, model=None) -> tuple:
    """
    Predict whether a legal document describes a Criminal or Civil case.
    
    Args:
        text: The legal document text (can be long - FIR, case filing, etc.)
        tokenizer: Optional pre-loaded tokenizer
        model: Optional pre-loaded model
    
    Returns:
        Tuple of (case_type, confidence) e.g., ("Criminal", 0.95)
    """
    # Load model if not provided
    if tokenizer is None or model is None:
        tokenizer, model = load_model()
        if model is None:
            return "Error", 0.0
    
    # Tokenize input (handles long documents)
    inputs = tokenizer(
        text,
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH,
        return_tensors="pt"
    )
    
    # Get prediction
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=-1)
        prediction = torch.argmax(probabilities, dim=-1).item()
        confidence = probabilities[0][prediction].item()
    
    case_type = "Criminal" if prediction == 1 else "Civil"
    return case_type, confidence


def predict_with_details(text: str, tokenizer=None, model=None) -> dict:
    """
    Predict with full details including probabilities.
    
    Returns:
        Dictionary with prediction details
    """
    if tokenizer is None or model is None:
        tokenizer, model = load_model()
        if model is None:
            return {"error": "Model not loaded"}
    
    # Tokenize input
    inputs = tokenizer(
        text,
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH,
        return_tensors="pt"
    )
    
    # Get prediction
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=-1)[0]
    
    civil_prob = probabilities[0].item()
    criminal_prob = probabilities[1].item()
    prediction = "Criminal" if criminal_prob > civil_prob else "Civil"
    
    return {
        "prediction": prediction,
        "confidence": max(civil_prob, criminal_prob),
        "civil_probability": civil_prob,
        "criminal_probability": criminal_prob
    }


def main():
    """Test the model with sample legal documents."""
    print("=" * 70)
    print("Legal Case Type Classifier - Test Script")
    print("Classifies legal documents as CRIMINAL or CIVIL")
    print("=" * 70)
    
    # Load model once
    print("\nInitializing...")
    tokenizer, model = load_model()
    if model is None:
        return
    
    # Test with realistic legal documents
    test_cases = [
        # === CIVIL CASES ===
        {
            "name": "Money Recovery (Civil)",
            "expected": "Civil",
            "text": """CASE INFORMATION - CIVIL SUIT

Court: Saket District Court, New Delhi
Case Number: CIV-2025-1088
Case Type: Civil Case (Recovery of Money)
Filing Date: September 20, 2025

Parties:
Plaintiff: Mr. Raj Sharma
Defendant: Ms. Priya Singh

Case Summary: The plaintiff, Mr. Raj Sharma, has filed a suit for the recovery of ₹50,000 from the defendant, Ms. Priya Singh. The plaintiff alleges that the loan was extended via a written promissory note dated January 15, 2025, with a repayment date of July 15, 2025. The defendant has failed to repay the amount by the stipulated date.

Current Status: Pending - Summons issued to the defendant."""
        },
        
        {
            "name": "Lawyer Notes (Civil)",
            "expected": "Civil",
            "text": """CONFIDENTIAL - ATTORNEY-CLIENT PRIVILEGE

Client Information:
Name: Mr. Raj Sharma
Role: Client (Plaintiff)

Case Strategy Notes:
Primary evidence is the signed promissory note. It's very strong.
The witness, Amit Verma, is reliable and willing to testify.
The email chain shows Priya acknowledging the debt and her failure to pay.
Our primary argument is a straightforward breach of contract. No complex legal theories needed.

Client is firm on recovering the full amount. Not interested in a settlement."""
        },
        
        {
            "name": "Eviction Case (Civil)",
            "expected": "Civil",
            "text": """CIVIL SUIT - EVICTION AND RENT RECOVERY

Plaintiff/Landlord: Suresh Kumar
Defendant/Tenant: Amit Verma
Monthly Rent: ₹25,000
Outstanding Rent: ₹1,50,000 (6 months)

The plaintiff is the owner of the residential premises. The defendant has been a tenant since 2023. The defendant has defaulted on rent payments for the last 6 months.

Relief Sought:
1. Eviction of the defendant from the premises
2. Recovery of outstanding rent
3. Compensation for property damage

This is a civil landlord-tenant dispute under the Rent Control Act."""
        },
        
        {
            "name": "Consumer Complaint (Civil)",
            "expected": "Civil",
            "text": """CONSUMER COMPLAINT

Complainant: Vikram Patel
Opposite Party: Best Electronics Store
Product: Air Conditioner
Amount: ₹75,000

Complaint: The complainant purchased an air conditioner from the opposite party. Within weeks of purchase, the product developed a major defect. Despite multiple complaints, neither repair nor replacement was provided.

This is a consumer dispute under the Consumer Protection Act. The complainant seeks replacement of the defective product and compensation."""
        },
        
        # === CRIMINAL CASES ===
        {
            "name": "Assault FIR (Criminal)",
            "expected": "Criminal",
            "text": """FIR - FIRST INFORMATION REPORT

Police Station: Central Police Station
FIR Number: 245/2025
Sections: 323, 324, 506 IPC (Assault, Causing Hurt, Criminal Intimidation)

Complainant: Deepa Nair
Accused: Sanjay Mehta

Statement: On the evening of Tuesday, at approximately 8 PM, the accused Sanjay Mehta attacked me near my residence. The accused attacked me with a wooden stick causing injuries to my head and arms. He also threatened to kill me if I report to the police. I sustained bleeding injuries and was taken to the hospital.

This is a criminal case of assault and criminal intimidation."""
        },
        
        {
            "name": "Theft Case (Criminal)",
            "expected": "Criminal",
            "text": """FIR - THEFT/ROBBERY

Police Station: City Police Station
FIR Number: 567/2025
Sections: 379, 380 IPC (Theft, Theft in dwelling house)

Complainant: Meera Iyer
Accused: Rahul Khanna (identified)

Incident: On the night of the incident, unknown persons broke into my residence while I was away. Upon returning, I found the lock broken and the house ransacked.

Items Stolen: Gold jewelry worth ₹5,00,000

During investigation, the accused Rahul Khanna was identified based on CCTV footage. This is a criminal case of theft/burglary."""
        },
        
        {
            "name": "Fraud Case (Criminal)",
            "expected": "Criminal",
            "text": """FIR - CRIMINAL FRAUD AND CHEATING

Sections: 420, 406, 468, 471 IPC (Cheating, Criminal Breach of Trust, Forgery)

Complainant: Anita Reddy
Accused: Vikram Patel

Criminal Complaint: The accused Vikram Patel cheated me of ₹10,00,000 through a fake investment scheme promising 50% returns. The accused made false promises and representations to induce me to invest money.

After receiving the money, the accused absconded. Upon investigation, I found that the entire scheme was fraudulent. This is a clear case of criminal fraud and cheating."""
        },
        
        {
            "name": "Murder Investigation (Criminal)",
            "expected": "Criminal",
            "text": """FIR - MURDER CASE

Police Station: Crime Branch
FIR Number: 123/2025
Sections: 302, 201 IPC (Murder, Causing disappearance of evidence)

Deceased: Raj Sharma
Accused: Amit Verma

Case Summary: The body of Raj Sharma was found at the outskirts of the city. Post-mortem report confirms death due to stab wounds and strangulation. The victim was last seen with the accused Amit Verma.

Investigation reveals the accused had ongoing disputes with the deceased. This is a case of premeditated murder. Charge sheet being prepared."""
        },
        
        {
            "name": "Drug Offense (Criminal)",
            "expected": "Criminal",
            "text": """FIR - NDPS ACT VIOLATION

Sections: 21, 22, 29 NDPS Act (Possession, Sale, Conspiracy)

Accused: Manoj Tiwari
Substance: Cocaine
Quantity: 2 kilograms

Case Details: Acting on intelligence input, a raid was conducted at the residence of the accused. During search, 2 kilograms of cocaine was recovered along with packaging material.

The accused was caught red-handed in possession of commercial quantity. This is a serious criminal offense under the NDPS Act."""
        },
        
        {
            "name": "Domestic Violence (Criminal)",
            "expected": "Criminal",
            "text": """FIR - DOMESTIC VIOLENCE

Sections: 498A, 323, 506 IPC (Cruelty, Assault, Criminal Intimidation)

Complainant: Priya Singh
Accused: Rahul Sharma (Husband)

Complaint: The complainant has been subjected to continuous physical and mental torture by husband. The accused regularly beats the complainant, often under influence of alcohol.

Injuries: Multiple bruises, burn marks on arms

The accused demands additional dowry and threatens to kill if family doesn't pay. This is a criminal case of domestic violence and marital cruelty."""
        },
        
        # === EDGE CASES ===
        {
            "name": "Email Evidence (Civil)",
            "expected": "Civil",
            "text": """EMAIL CORRESPONDENCE - EVIDENCE

From: Raj Sharma
To: Priya Singh
Subject: Reminder: Loan Repayment Overdue

Hi Priya,
Hope you're well. I'm following up on the ₹50,000 loan. The due date has passed. Please let me know when I can expect the payment.

Reply from Priya:
I know, I'm sorry. Things have been difficult financially. Can you give me more time?

This constitutes civil matter for recovery of debt. No criminal elements present."""
        },
        
        {
            "name": "Promissory Note (Civil)",
            "expected": "Civil",
            "text": """PROMISSORY NOTE

Date: January 15, 2025
Loan Amount: ₹50,000 (Fifty Thousand Indian Rupees)

FOR VALUE RECEIVED, the undersigned, Ms. Priya Singh (the "Borrower"), promises to pay to the order of Mr. Raj Sharma (the "Lender") the principal sum of ₹50,000.

TERMS: The full amount is to be repaid on or before July 15, 2025.

Signature of Borrower: Priya Singh

Note: The borrower has not repaid despite reminders. This matter is being taken to civil court for recovery."""
        },
    ]
    
    print("\n" + "=" * 70)
    print("TESTING WITH SAMPLE LEGAL DOCUMENTS")
    print("=" * 70)
    
    correct = 0
    total = len(test_cases)
    
    for i, case in enumerate(test_cases, 1):
        result = predict_with_details(case["text"], tokenizer, model)
        prediction = result["prediction"]
        confidence = result["confidence"] * 100
        expected = case["expected"]
        name = case["name"]
        
        is_correct = prediction == expected
        correct += is_correct
        status = "✓" if is_correct else "✗"
        
        print(f"\n[{i}/{total}] {name}")
        print(f"  Expected: {expected}")
        print(f"  Predicted: {prediction} ({confidence:.1f}% confidence) {status}")
        
        if not is_correct:
            print(f"  Civil prob: {result['civil_probability']*100:.1f}%")
            print(f"  Criminal prob: {result['criminal_probability']*100:.1f}%")
    
    print("\n" + "=" * 70)
    print(f"ACCURACY: {correct}/{total} ({correct/total*100:.1f}%)")
    print("=" * 70)
    
    # Interactive mode
    print("\n" + "=" * 70)
    print("INTERACTIVE MODE")
    print("=" * 70)
    print("Paste a legal document to classify.")
    print("When done pasting, type 'done' on a new line and press Enter.")
    print("Type 'quit' to exit.")
    print()
    
    while True:
        lines = []
        empty_count = 0
        print(">>> Paste your document below, then type 'done':")
        
        while True:
            try:
                line = input()
                
                # Check for exit commands
                if line.lower().strip() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    return
                
                # Check for 'done' signal to process input
                if line.lower().strip() == 'done':
                    break
                
                lines.append(line)
                
            except EOFError:
                break
        
        if not lines:
            print("No input received. Please paste a document.\n")
            continue
        
        user_input = "\n".join(lines)
        
        # Show a preview of what was received
        preview = user_input[:100].replace('\n', ' ')
        if len(user_input) > 100:
            preview += "..."
        print(f"\n  Processing: \"{preview}\"")
        print(f"  Total length: {len(user_input)} characters")
        
        result = predict_with_details(user_input, tokenizer, model)
        print(f"\n  ╔════════════════════════════════════════╗")
        print(f"  ║  RESULT: {result['prediction']:^10}                  ║")
        print(f"  ╠════════════════════════════════════════╣")
        print(f"  ║  Confidence: {result['confidence']*100:>5.1f}%                   ║")
        print(f"  ║  Civil probability: {result['civil_probability']*100:>5.1f}%            ║")
        print(f"  ║  Criminal probability: {result['criminal_probability']*100:>5.1f}%         ║")
        print(f"  ╚════════════════════════════════════════╝")
        print()


if __name__ == "__main__":
    main()

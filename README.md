# AI Legal Document Classifier

A machine learning model that classifies legal documents as **Criminal** or **Civil** cases using fine-tuned DistilBERT.

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)
![Transformers](https://img.shields.io/badge/Transformers-4.30+-orange.svg)

## Features

- **Plug-and-Play API** - Simple `classify_legal_text()` function for instant predictions
- **DistilBERT-based** - Fine-tuned transformer model for legal text understanding
- **Long Document Support** - Handles documents up to 512 tokens
- **Synthetic Dataset** - Includes realistic legal document generator (FIRs, case filings, evidence summaries)
- **GPU/CPU Support** - Automatic detection of CUDA, Apple MPS, or CPU

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd "AI Lawyer Model"

# Install dependencies
pip install -r requirements.txt
# OR using uv
uv sync
```

### Usage

```python
from legal_classifier import classify_legal_text

# Classify any legal document
result = classify_legal_text("The accused stabbed the victim with a knife and fled the scene.")
print(result)
# Output: {"type": "Criminal", "confidence": 0.92, "civil_prob": 0.08, "criminal_prob": 0.92}

# Civil case example
result = classify_legal_text("The tenant refused to pay rent for 6 months.")
print(result)
# Output: {"type": "Civil", "confidence": 0.89, "civil_prob": 0.89, "criminal_prob": 0.11}
```

### Quick Test

```bash
python legal_classifier.py
```

## Project Structure

```
AI Lawyer Model/
├── legal_classifier.py      # Main API - plug-and-play classifier
├── train_classifier.py      # Model training script
├── generate_dataset.py      # Synthetic legal dataset generator
├── test_model.py            # Comprehensive model testing
├── legal_stories.csv        # Generated training dataset (600+ documents)
├── civil_criminal_model/    # Trained model weights (~268MB)
│   ├── config.json
│   ├── model.safetensors
│   ├── tokenizer_config.json
│   └── vocab.txt
├── training_output/         # Training checkpoints
├── requirements.txt         # Python dependencies
├── pyproject.toml           # Project configuration (uv)
└── README.md
```

## API Reference

### `classify_legal_text(text: str) -> dict`

Classifies a legal document as Criminal or Civil.

**Parameters:**
- `text` (str): The legal document text (can be any length, will be truncated if needed)

**Returns:**
```python
{
    "type": "Criminal" | "Civil",  # Classification result
    "confidence": float,            # Confidence score (0-1)
    "civil_prob": float,            # Probability of Civil
    "criminal_prob": float          # Probability of Criminal
}
```

## Training Your Own Model

### Step 1: Generate Dataset

```bash
python generate_dataset.py
```

This creates `legal_stories.csv` with ~600 synthetic legal documents including:

**Civil Cases:**
- Money recovery disputes
- Property disputes
- Contract breaches
- Landlord-tenant disputes
- Employment disputes
- Consumer complaints
- Divorce/family matters

**Criminal Cases:**
- Assault/violence
- Theft/robbery
- Fraud/cheating
- Murder/attempt to murder
- Kidnapping
- Drug offenses
- Domestic violence
- Criminal threats/extortion
- Sexual offenses
- Forgery

### Step 2: Train the Model

```bash
python train_classifier.py
```

Training configuration:
- **Base Model:** `distilbert-base-uncased`
- **Max Sequence Length:** 512 tokens
- **Batch Size:** 8
- **Epochs:** 3
- **Learning Rate:** 2e-5
- **Early Stopping:** Patience of 2 epochs

The trained model is saved to `./civil_criminal_model/`.

### Step 3: Test the Model

```bash
python test_model.py
```

This runs comprehensive tests with various legal document types.

## Model Performance

The model is evaluated on a 20% held-out test set with the following metrics:

| Metric | Score |
|--------|-------|
| Accuracy | ~95%+ |
| F1 Score | ~0.95 |
| Precision | ~0.95 |
| Recall | ~0.95 |

*Actual scores may vary based on the generated dataset.*

## Requirements

- Python 3.13+
- PyTorch 2.0+
- Transformers 4.30+
- pandas 2.0+
- scikit-learn 1.3+

See `requirements.txt` for the complete list.

## Hardware Requirements

- **Minimum:** 8GB RAM, CPU (training will be slower)
- **Recommended:** 16GB RAM, NVIDIA GPU with 8GB+ VRAM
- **Model Size:** ~268MB (DistilBERT)

## Environment Variables

Create a `.env` file for optional Groq API integration:

```env
GROQ_API_KEY=your_api_key_here
```

## License

This project is for educational and research purposes.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

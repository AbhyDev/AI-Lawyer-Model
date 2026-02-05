# AI Lawyer Model - Copilot Instructions

## Project Overview
This is a **legal document classification system** that automatically categorizes legal documents as **Criminal** or **Civil** using a fine-tuned DistilBERT model. The system uses synthetic legal data for training and provides a production-ready classifier with high accuracy.

## Core Architecture

### Three Main Components:

1. **Dataset Pipeline** (`generate_dataset.py`)
   - Generates synthetic legal documents (8300+ examples) in `legal_stories.csv`
   - Creates realistic legal case types: money recovery, property disputes, FIRs, harassment, contract breaches, etc.
   - Labels: 0 = Civil, 1 = Criminal
   - **Key insight**: More Civil cases in dataset (improves civil classification accuracy)

2. **Model Training** (`train_classifier.py`)
   - Fine-tunes DistilBERT on the dataset (checkpoint every 30 epochs)
   - Uses `LegalDocumentsDataset` class for tokenization with 512-token limit
   - Trains for 90 epochs with early stopping and validation set (10%)
   - Outputs trained model to `./civil_criminal_model/`
   - **Key metrics**: accuracy, F1, precision, recall

3. **Inference & API** (`legal_classifier.py` + `test_model.py`)
   - `legal_classifier.classify_legal_text(text)` - main entry point
   - Returns dict: `{"type": "Criminal"|"Civil", "confidence": float, "civil_prob": float, "criminal_prob": float}`
   - Lazy-loads model on first use for performance
   - Handles documents up to 512 tokens (auto-truncates longer docs)

## Data Flow
```
legal_stories.csv → train_classifier.py → ./civil_criminal_model/ → legal_classifier.py → classify_legal_text()
```

## Key Files & Patterns

### Model Handling
- **Model path**: Always relative `./civil_criminal_model` (must contain `config.json`, `model.safetensors`, `tokenizer_config.json`, `vocab.txt`)
- **Lazy loading**: `_load_model()` in `legal_classifier.py` prevents repeated initialization
- **Global state**: `_tokenizer` and `_model` cached after first import
- **Device handling**: Uses `torch.no_grad()` for inference efficiency

### Dataset Conventions
- **CSV format**: Simple 2-column layout (`text`, `label`)
- **Text diversity**: Legal documents include case filings, FIRs, lawyer notes, email evidence, property deeds, promissory notes
- **Criminal markers**: Sections like "354, 354A, 509 IPC", "FIR", assault, harassment, theft
- **Civil markers**: Property disputes, contract breaches, money recovery, family settlement, partition

### Configuration
- **MAX_LENGTH = 512**: Hard limit for tokenization (legal docs can be long)
- **MODEL_NAME = "distilbert-base-uncased"**: Chosen for speed and legal language performance
- **Batch size**: 32 (training), adjustable for memory constraints

## Development Workflows

### Training a New Model
```bash
python train_classifier.py
```
- Expects `legal_stories.csv` in project root
- Creates `./civil_criminal_model/` with checkpoints
- Generates `./training_output/checkpoint-{30,60,90}/` for recovery/analysis

### Testing Classification
```bash
python test_model.py
```
- Uses `predict_case_type(text)` function
- Loads model from `./civil_criminal_model/`
- Tests with predefined legal document examples

### Using in Production
```python
from legal_classifier import classify_legal_text
result = classify_legal_text("Your legal text...")
print(result["type"])  # "Criminal" or "Civil"
```

### Generating New Dataset
```bash
python generate_dataset.py
```
- Regenerates `legal_stories.csv` with new synthetic data
- Useful for rebalancing class distribution or adding new case types

## External Integrations

### Dependencies
- **torch**: Deep learning framework
- **transformers**: Hugging Face model library
- **pandas/scikit-learn**: Data handling & metrics

## Project-Specific Conventions

1. **No explicit test suite**: Validation happens in `test_model.py` as manual testing script
2. **Relative paths only**: All model/data paths are relative to project root (Windows/Linux compatible)
3. **Synthetic data priority**: No real legal data; all training data is generated
4. **Binary classification only**: Always outputs "Criminal" or "Civil", never ambiguous
5. **Confidence scores**: Always provided to let downstream systems decide thresholds

## Common Tasks for AI Agents

### Improving Accuracy
- Review `./training_output/checkpoint-{N}/` for metrics
- Regenerate dataset with better criminal case examples (`generate_dataset.py`)
- Adjust `MAX_LENGTH` or batch size in `train_classifier.py`

### Adding New Legal Case Types
- Edit template functions in `generate_dataset.py` (e.g., `generate_civil_property_dispute()`)
- Add criminal case generators for FIR types
- Regenerate dataset, retrain

### Debugging Classification Errors
- Use `test_model.py` to analyze edge cases
- Check token limits (512) - very long docs may be cut off
- Verify model files exist in `./civil_criminal_model/`

### Extending the Pipeline
- Create API wrapper (FastAPI) around `legal_classifier.classify_legal_text()`
- Build UI that displays confidence scores & probabilities

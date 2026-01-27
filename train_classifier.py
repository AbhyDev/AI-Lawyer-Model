"""
train_classifier.py
Fine-tunes DistilBERT on the legal_stories.csv dataset
to classify legal documents as Criminal (1) or Civil (0).

Supports long legal documents (up to 512 tokens).
Saves the trained model and tokenizer to ./civil_criminal_model
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import torch
from transformers import (
    DistilBertTokenizer,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments,
    EarlyStoppingCallback
)
from torch.utils.data import Dataset
import warnings
warnings.filterwarnings('ignore')


class LegalDocumentsDataset(Dataset):
    """Custom Dataset for legal document classification."""
    
    def __init__(self, texts, labels, tokenizer, max_length=512):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=self.max_length,
            return_tensors="pt"
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }


def compute_metrics(pred):
    """Compute metrics for evaluation."""
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    
    precision, recall, f1, _ = precision_recall_fscore_support(
        labels, preds, average='binary'
    )
    acc = accuracy_score(labels, preds)
    
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }


def main():
    # Configuration
    MODEL_NAME = "distilbert-base-uncased"
    OUTPUT_DIR = "./civil_criminal_model"
    MAX_LENGTH = 512  # Increased for longer legal documents
    BATCH_SIZE = 8    # Reduced due to longer sequences
    EPOCHS = 3
    LEARNING_RATE = 2e-5
    
    print("=" * 60)
    print("Legal Document Classifier Training")
    print("(Criminal vs Civil Classification)")
    print("=" * 60)
    
    # Check for GPU/MPS
    if torch.cuda.is_available():
        device = "cuda"
        print(f"Using GPU: {torch.cuda.get_device_name(0)}")
    elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        device = "mps"
        print("Using Apple Silicon (MPS)")
    else:
        device = "cpu"
        print("Using CPU (training will be slower)")
    
    # Load the dataset
    print("\n[1/5] Loading dataset...")
    try:
        df = pd.read_csv("legal_stories.csv")
        print(f"  ✓ Loaded {len(df)} documents")
        print(f"    - Criminal cases: {len(df[df['label'] == 1])}")
        print(f"    - Civil cases: {len(df[df['label'] == 0])}")
        
        # Calculate average document length
        avg_chars = df['text'].str.len().mean()
        avg_words = df['text'].str.split().str.len().mean()
        print(f"    - Avg document length: {avg_chars:.0f} chars, {avg_words:.0f} words")
    except FileNotFoundError:
        print("ERROR: legal_stories.csv not found!")
        print("Please run generate_dataset.py first.")
        return
    
    # Split data
    print("\n[2/5] Splitting data (80% train / 20% test)...")
    train_texts, test_texts, train_labels, test_labels = train_test_split(
        df['text'].values,
        df['label'].values,
        test_size=0.2,
        random_state=42,
        stratify=df['label'].values  # Maintain class balance
    )
    print(f"  ✓ Training set: {len(train_texts)} documents")
    print(f"  ✓ Test set: {len(test_texts)} documents")
    
    # Load tokenizer and model
    print("\n[3/5] Loading DistilBERT model and tokenizer...")
    tokenizer = DistilBertTokenizer.from_pretrained(MODEL_NAME)
    model = DistilBertForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2,
        id2label={0: "Civil", 1: "Criminal"},
        label2id={"Civil": 0, "Criminal": 1}
    )
    print(f"  ✓ Model: {MODEL_NAME}")
    print(f"  ✓ Max sequence length: {MAX_LENGTH} tokens")
    
    # Create datasets
    print("\n[4/5] Tokenizing documents...")
    train_dataset = LegalDocumentsDataset(
        train_texts, train_labels, tokenizer, MAX_LENGTH
    )
    test_dataset = LegalDocumentsDataset(
        test_texts, test_labels, tokenizer, MAX_LENGTH
    )
    print(f"  ✓ Tokenization complete")
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir="./training_output",
        num_train_epochs=EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        per_device_eval_batch_size=BATCH_SIZE,
        warmup_steps=50,
        weight_decay=0.01,
        logging_dir="./logs",
        logging_steps=25,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        push_to_hub=False,
        report_to="none",  # Disable wandb/tensorboard
        learning_rate=LEARNING_RATE,
        # For GPU memory efficiency with long sequences
        gradient_accumulation_steps=2,
        fp16=torch.cuda.is_available(),  # Use mixed precision on GPU
    )
    
    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
    )
    
    # Train
    print("\n[5/5] Training the model...")
    print("-" * 60)
    trainer.train()
    print("-" * 60)
    
    # Evaluate
    print("\nEvaluating on test set...")
    results = trainer.evaluate()
    
    print(f"\n{'='*60}")
    print("FINAL RESULTS")
    print(f"{'='*60}")
    print(f"  Accuracy:  {results['eval_accuracy']:.4f} ({results['eval_accuracy']*100:.1f}%)")
    print(f"  F1 Score:  {results['eval_f1']:.4f}")
    print(f"  Precision: {results['eval_precision']:.4f}")
    print(f"  Recall:    {results['eval_recall']:.4f}")
    
    # Confusion Matrix
    predictions = trainer.predict(test_dataset)
    preds = predictions.predictions.argmax(-1)
    cm = confusion_matrix(test_labels, preds)
    
    print(f"\nConfusion Matrix:")
    print(f"                    Predicted")
    print(f"                 Civil  Criminal")
    print(f"  Actual Civil    {cm[0][0]:4d}     {cm[0][1]:4d}")
    print(f"  Actual Criminal {cm[1][0]:4d}     {cm[1][1]:4d}")
    
    # Calculate additional metrics
    true_negative = cm[0][0]
    false_positive = cm[0][1]
    false_negative = cm[1][0]
    true_positive = cm[1][1]
    
    print(f"\nDetailed Breakdown:")
    print(f"  True Positives (Criminal correctly identified):  {true_positive}")
    print(f"  True Negatives (Civil correctly identified):     {true_negative}")
    print(f"  False Positives (Civil misclassified as Criminal): {false_positive}")
    print(f"  False Negatives (Criminal misclassified as Civil): {false_negative}")
    
    # Save the model
    print(f"\nSaving model to {OUTPUT_DIR}...")
    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    print("  ✓ Model saved successfully!")
    print("  ✓ Tokenizer saved successfully!")
    
    print(f"\n{'='*60}")
    print("Training Complete!")
    print(f"{'='*60}")
    print(f"\nNext step: Run 'python test_model.py' to test the model")


if __name__ == "__main__":
    main()

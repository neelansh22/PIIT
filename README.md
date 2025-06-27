# PIIT - Personal Information Identification Tool. 

**PIIT** is an offline Python tool for detecting and redacting sensitive Personally Identifiable Information (PII) in text. It is designed for use in any data project. Quite useful for a first iteration to be used as a layer on top of sensitive data that must remain within an org's internal data ecosystem.
---

## Features

- **Detects PII:** Finds names, locations, emails, phone numbers, and addresses in text.
- **Multi-language Support:** Uses spaCy language models for English, French, German, Italian, Dutch, Portuguese, Romanian, Spanish, Catalan, and Japanese.
- **Flexible & Modular:** Each detection method is modular, so you can use only what you need.
- **Offline Processing in SDK style:** No data leaves your environment. The utility is designed as an SDK, easily extendable and modular.
- **Redaction:** Can automatically redact detected PII from text.

---

## How It Works

The tool combines:
- **spaCy NER models** for language-specific entity recognition.
- **Regular expressions** for pattern-based detection (e.g., emails, phone numbers).
- **Custom logic** for scoring and flagging PII.

You can process a single text string or a batch of texts. The main workflow is demonstrated in `main.ipynb`.

---

## Quick Start

### 1. Set Up Your Environment

```sh
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Download spaCy Models

Depending on your language needs, download the required spaCy models. For example:

```sh
python -m spacy download en_core_web_lg
python -m spacy download de_core_news_lg
python -m spacy download fr_core_news_lg
# ...and others as needed
```

### 3. Run the Notebook

Open `main.ipynb` in VS Code or Jupyter and run the cells to see PII detection in action.

---

## Example Usage

```python
import utils.pii_sniffer as pii_sniffer

test_string = "John Smith lives at 123 Main St, New York, USA. Email: john.smith@example.com ph 123939402"
sniffer = pii_sniffer.pii_sniffer(test_string)
sniffer.data_processing()
sniffer.address_flag()
sniffer.pii_scorer_call()
sniffer.rpi_caller()
sniffer.extract_phone_numbers()
sniffer.extract_organization_names()
sniffer.detect_pii_flag()

processed_data = sniffer.data
print(processed_data)
```

---

## Contributing

- The code is modular: each script in the `utils` folder can be used independently.
- To add new detection logic, simply create a new module and integrate it into the pipeline.
- Please run `data_processing` before any other function to ensure proper setup.

---

## Notes

- All processing is done locally; no data is sent to external servers.
- The notebook (`main.ipynb`) is fully commented and demonstrates each step.
- For best results, ensure you have the correct spaCy models installed for your target languages.

---

## Contact

For questions or suggestions, please open an issue or contact the maintainer.

# Project Instructions

You have been provided with an anonymized dataset of medical transcriptions organized by specialty, transcriptions.csv.
- Use the OpenAI API to extract "age", "medical_specialty", and a new data field to store the recommended treatment extracted from each transcription.
- Match each recommended treatment with the corresponding International Classification of Diseases (ICD) code, and save your answers in a pandas DataFrame named df_structured.

## 🗂️ Project Structure

```
organizing-medical-transcriptions/
├── src/
│   └── data/
│       └── main.py         # Main script for processing data
├── venv/                   # Virtual environment (excluded from Git)
├── .env                    # Environment variables (not committed)
├── .env.example            # Sample environment file
├── .gitignore              # Git ignore rules
├── requirements.txt        # Python dependencies
```

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/NEOLPAR/organizing-medical-transcriptions-openai.git
cd organizing-medical-transcriptions
```

### 2. Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install dependencies

```bash
pip install -r requirements
```

### 4. Configure environment variables

Copy the example file and provide your OpenAI API key:

```bash
cp .env.example .env
```

Then open `.env` and set your key:

```bash
OPENAI_API_KEY=your-api-key-here
```

## 🚀 Running the Script

Run the main script using:

```bash
python src/main.py
```

## 📝 Notes

* The script relies on the OpenAI API. Ensure your API key is valid and usage limits are sufficient.
* `.env` is excluded from version control to protect sensitive credentials.
* You can modify main.py to adjust how transcription data is loaded, processed, or saved.

## 📄 License

This project is provided for educational purposes. See `LICENSE` for details (if applicable).

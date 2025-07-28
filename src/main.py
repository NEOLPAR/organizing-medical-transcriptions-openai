import os
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from openai import OpenAI
import json

load_dotenv()

# Load the data
BASE_DIR = Path(__file__).resolve().parent
transcriptions_filepath = os.path.join(BASE_DIR, 'data', 'transcriptions.csv')
df = pd.read_csv(transcriptions_filepath)
df.head()

# Initialize the OpenAI client
client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

## Start coding here, use as many cells as you need

def extract_patient_data(text):
    function_definition=[{
        "type": "function",
        "function": {
            "name": "extract_medical_data",
            "description": "Get age, medical_specialty and recommended_treatment",
            "parameters": {
                "type": "object",
                "properties": {
                    "age": {
                        "type": "number",
                        "description": "age of patient"
                    },
                    "recommended_treatment": {
                        "type": "string",
                        "description": "recommended treatment/procedure"
                    }
                },
                "required": ["age", "medical_specialty", "recommended_treatment"]
            }
        }
    }]
    responseExtracting = client.chat.completions.create(
        model="gpt-4.1-mini",
        max_completion_tokens=200,
        messages=[{
            "role": "system",
            "content": "You are a medical data extractor. Return all results strictly in JSON format, with no extra text. Don't make up or assume values. Output example: {age: 20, recommended_treatment: '<Recommended treatments/procedures>'}"
        },
        {
            "role": "user",
            "content": text
        }],
        temperature=0.7,
        response_format={"type":"json_object"},
        tools=function_definition,
        tool_choice={
            "type": "function",
            "function": {"name": "extract_medical_data"}
        }
    )
    return json.loads(responseExtracting.choices[0].message.tool_calls[0].function.arguments)

def extract_icd10(patient_details):
    icd10_function_definition=[{
        "type": "function",
        "function": {
            "name": "extract_icd_10",
            "description": "Get ICD10 from age, treatment/procedure and medical specialty provided.",
            "parameters": {
                "type": "object",
                "properties": {
                    "icd10": {
                        "type": "string",
                        "description": "icd 10"
                    }
                },
                "required": ["icd10"]
            }
        }
    }]
    response_extract_icd_10 = client.chat.completions.create(
        model="gpt-4.1-mini",
        max_completion_tokens=100,
        messages=[{
            "role": "system",
            "content": "You are a medical ICD-10 specialist. Return in JSON format, the ICD-10 code for the age, treatment/procedure and medical specialty provided. Output example: {'icd10': string}"
        },{     # one-shot
          "role": "user",
          "content": json.dumps({
            "age": 34,
            "recommended_treatment": "Uses corticosteroid nasal spray",
            "medical_specialty": "Allergy / Immunology"
          })
        },
        {
          "role": "assistant",
          "content": json.dumps({
            "icd10": "J30.1"
          })
        },{    # prompt
            "role": "user",
            "content": json.dumps(patient_details)
        }],
        temperature=0.7,
        response_format={"type": "json_object"},
        tools=icd10_function_definition,
        tool_choice={   # needed to force the function as gpt-4.1-mini is not as reliable as 4o for function calling, still not good results
            "type": "function",
            "function": {"name": "extract_icd_10"}
        }
    )

    return json.loads(response_extract_icd_10.choices[0].message.tool_calls[0].function.arguments)

results = []
for idx, row in df.iterrows():
    specialty = row["medical_specialty"]
    text = row["transcription"]

    patient_data = extract_patient_data(text)
    patient_data['medical_specialty'] = specialty

    extracted_icd10 = extract_icd10(patient_data)
    patient_data['icd10'] = extracted_icd10['icd10']

    results.append(patient_data)

df_structured = pd.DataFrame(results)
df_structured.head()

processed_filepath = os.path.join(BASE_DIR, 'data', 'processed_data.csv')
df_structured.to_csv(processed_filepath, index=False)  # Save to file
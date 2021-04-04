import requests
import json

def removeAmbiguousSymptom(symptom):
    
    print(symptom)
    if symptom == 'feverish':
        symptom = 'fever'
    elif symptom == 'pain in muscles':
        symptom = 'muscle pain'
    elif symptom == 'cramps in stomach':
        symptom = 'stomach cramps'
    elif symptom == 'pain in back':
        symptom = 'back pain'
    elif symptom == 'pain in stomach':
        symptom = 'stomach pain'
    elif symptom == 'swelling in neck' or symptom == 'neck is swollen':
        symptom = 'neck swelling'
    elif symptom == 'loss in appetite' or symptom == 'appetite loss':
        symptom = 'loss of appetite'
    elif symptom == 'breathlessness' or symptom == 'unable to breathe' or symptom == 'not able to breathe' or symptom == 'difficult to breathe' or symptom == 'breathing issues' or symptom == 'breathing problems':
        symptom = 'difficulty in breathing'
    elif symptom == 'muscle spasms':
        symptom = 'muscle weakness'
    elif symptom == 'less body stability':
        symptom = 'loss of balance'
    elif symptom == 'high heart rate' or symptom == 'high heart beat':
        symptom = 'fast heart rate'
    elif symptom == 'uneasy in the chest':
        symptom = 'chest pain'
    elif symptom == 'pain in face':
        symptom = 'facial pain'
    elif symptom == 'unable to speak properly' or symptom == 'unable to speak well' or symptom == 'unable to speak normally':
        symptom = 'difficulty in speaking'
    elif symptom == 'pain in the eye' or symptom == 'eyes paining':
        symptom = 'eye pain'
    elif symptom == 'pain in my joints' or symptom == 'joints are paining' or symptom == 'not able to move my joints':
        symptom = 'joint pain'
    elif  symptom == 'unable to remember' or symptom == 'forgetting often':
        symptom = 'forgetfulness'
    elif symptom == 'heavy eyes' or symptom == 'swollen eyes' or symptom == 'inflammation of eyes':
        symptom = 'inflammed eyes'
    elif symptom == 'unable to concentrate' or symptom == 'unable to focus' or symptom == 'difficulty in concentration':
        symptom = 'poor concentration'
    elif symptom == 'irritated':
        symptom = 'irritability'
    elif symptom == 'unclear vision' or symptom == 'unable to see':
        symptom = 'distorted vision'
    elif symptom == 'itchiness':
        symptom = 'itching'
    elif symptom == 'red eyes':
        symptom = 'redness in eyes'

    print(symptom)
    return symptom

def create_user(name, email, number, diabetes, blood_pressure, frequent_cold, frequent_cough, migraine):
    request_url = "http://127.0.0.1:5000/register"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
        # "Authorization": f"Bearer {airtable_api_key}",
    }
    print(headers) 
    data = {
        "name" : name,
        "password": "12345678",
        "number" : number,
        "email" : email,
        "diabetes" : diabetes,
        "blood_pressure" : blood_pressure,
        "frequent_cold" : frequent_cold,
        "frequent_cough" : frequent_cough,
        "migraine" : migraine
    }
    print(data)
    
    try:
        print("Sending request")
        response = requests.post(
            request_url, headers=headers, data=json.dumps(data)
        )
        print("Request sent")
        response.raise_for_status()
        print(response.status_code)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    
    return response

def predict(symptoms, email):
    request_url = "http://127.0.0.1:5000/predict"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
        # "Authorization": f"Bearer {airtable_api_key}",
    }
    print(headers) 
    data = {
        "email" : email,
        "symptoms" : symptoms
    }
    print(data)
    
    try:
        print("Sending request")
        response = requests.post(
            request_url, headers=headers, data=json.dumps(data)
        )
        print("Request sent")
        response.raise_for_status()
        print(response.status_code)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    
    return response

def get_diseases(email):
    request_url = "http://127.0.0.1:5000/predict"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
        # "Authorization": f"Bearer {airtable_api_key}",
    }
    print(headers)
    if type(email) == list:
        email = email[0]
    data = {
        "email" : email
    }
    print(data)
    try:
        print("Sending request")
        response = requests.get(
            request_url, headers=headers, data=json.dumps(data)
        )
        print("Request sent")
        response.raise_for_status()
        print(response.status_code)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    
    return response.json()

def stored_prognosed_disease(email, disease):
    request_url = "http://127.0.0.1:5000/prognosis"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
        # "Authorization": f"Bearer {airtable_api_key}",
    }
    print(headers)
    if type(email) == list:
        email = email[0]
    data = {
        "email" : email,
        "disease": disease
    }
    print(data)
    try:
        print("Sending request")
        response = requests.post(
            request_url, headers=headers, data=json.dumps(data)
        )
        print("Request sent")
        response.raise_for_status()
        print(response.status_code)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    finally:
        return response.json()

def get_duration(email):
    request_url = "http://127.0.0.1:5000/prognosis"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
        # "Authorization": f"Bearer {airtable_api_key}",
    }
    print(headers)
    if type(email) == list:
        email = email[0]
    data = {
        "email" : email
    }
    print(data)
    try:
        print("Sending request")
        response = requests.get(
            request_url, headers=headers, data=json.dumps(data)
        )
        print("Request sent")
        response.raise_for_status()
        print(response.status_code)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    
    return response.json()
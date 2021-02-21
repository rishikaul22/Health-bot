# This files contains your custom actions which can be used to run
# custom Python code.

# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
import requests
import json

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormValidationAction
import webbrowser

# from scipy import spatial
# from sentence_transformers import SentenceTransformer
# from backend.nlptest import set_symptom
from backend.unique_symptoms import unique

# print("BEFORE LOADING")
# similarity_model = SentenceTransformer('bert-base-nli-mean-tokens')
# print("AFTER LOADING")

def removeAmbiguousSymptom(symptom):

    print(symptom)

    if symptom == 'pain in muscles':
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

    print(symptom)
    return symptom

class UserForm(Action):
    def name(self):
        return "profile_form"

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

def predict(symptoms):
    request_url = "http://127.0.0.1:5000/predict"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
        # "Authorization": f"Bearer {airtable_api_key}",
    }
    print(headers) 
    data = {
        "email" : "khushi112@gmail.com",
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


class ActionSubmit(Action):
    def name(self):
        return "action_submit"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict"):

        name = tracker.get_slot("name")
        number = tracker.get_slot("number")
        email = tracker.get_slot("email")
        diabetes = tracker.get_slot("diabetes")
        blood_pressure = tracker.get_slot("blood_pressure")
        frequent_cold = tracker.get_slot("frequent_cold")
        frequent_cough = tracker.get_slot("frequent_cough")
        migraine = tracker.get_slot("migraine")

        print(name)
        print(type(name))
        if type(name) == list:
            name = ' '.join(name)
            name = name.title()

        print("Calling function")
        print(name)
        resp = create_user(
            name=name,
            email=email,
            number=number,
            diabetes=diabetes,
            blood_pressure=blood_pressure,
            frequent_cold=frequent_cold,
            frequent_cough=frequent_cough,
            migraine=migraine
        )
        print(resp)
        dispatcher.utter_message(template="utter_form_values",
                                 name=name,
                                 number=number,
                                 email = email,
                                 diabetes = diabetes,
                                 blood_pressure = blood_pressure,
                                 frequent_cold = frequent_cold,
                                 frequent_cough = frequent_cough,
                                 migraine = migraine
                                )

class SymptomsForm(Action):

    def name(self):
        return "symptoms_form"

class SymptomsFormSubmit(Action):

    def name(self):
        return "action_symptoms_form_submit"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict"):
    
        allsymptoms = tracker.get_slot('all_symptoms')
        resp = predict(allsymptoms)
        print(resp.json())
        dispatcher.utter_message(template="utter_symptom_form_values",
                                 symptoms=resp.json())

class ValidateSymptomsForm(FormValidationAction):
    def name(self):
        return "validate_symptoms_form"
    
    def validate_more_symptoms(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ):
        symps = tracker.get_slot('all_symptoms')
        print(symps)

        if symps == None:
            index = 0
            symps = list()
        else:
            index = len(symps)

        val = {
            "symptom": tracker.get_slot('symptoms'),
            "duration": tracker.get_slot('duration'),
            #"severity": tracker.get_slot("severity")
        }

        symps.append(val)

        if slot_value == "yes":
            return {
                "symptoms": None,
                "more_symptoms": None,
                "duration": None,
                #"severity": None,
                "all_symptoms": symps
            }
        else:
            print("IN NO")
            return {"more_symptoms": slot_value, "all_symptoms": symps}

    def validate_symptoms(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ):
        symptom = tracker.get_slot('symptoms')
        print(symptom)
        if type(symptom) == list:
            all_symps = set(symptom)
            symptom = list(all_symps)
            print(symptom)

            if symptom[0] not in unique:
                print("IN HERE")
                print(symptom[0])
                symptom = removeAmbiguousSymptom(symptom[0])
                print(symptom)
            else:
                print("IN THIS")
                symptom = symptom[0]
        
        else:
            if symptom not in unique:
                print("IN HERE")
                symptom = removeAmbiguousSymptom(symptom)

        return {"symptoms" : symptom}

    def validate_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ):
        duration = tracker.get_slot('duration')
        days = 0

        temp = ''
        if type(duration) == list:
            duration = set(duration)
            if len(duration) == 1:
                duration = duration.pop()
            else:
                duration = list(duration)
                if duration[0] == "weeks" or duration[0] == "week" or duration[0] == "days" or duration[0] == "day":
                    temp = duration[1]+ duration[0]
                else:
                    temp = duration[0]+ duration[1]
                duration = temp
        
        if "weeks" in duration:
            index = duration.find("weeks")
            duration = duration[0:index].strip(" .,")
            duration = int(duration)
            days = 7 * duration
        elif "week" in duration:
            days = 7
        elif "days" in duration:
            index = duration.find("days")
            duration = duration[0:index].strip(" .,")
            days = int(duration)
        else:
            days = 1

        return {"duration": days}
    
class Login(Action):
    def name(self):
        return "action_login"
    
    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict"):
        
        email_id = "khushi@gmail.com"
        if tracker.get_slot('email') == email_id:
            print("IN LOGIN SUCCESS")
            SlotSet('loggedin', True)
            dispatcher.utter_message(template="utter_login_success")
        else:
            print("IN LOGIN FAILURE")
            dispatcher.utter_message(template="utter_wrong_email")
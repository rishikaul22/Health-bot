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

class UserForm(Action):
    def name(self):
        return "profile_form"

    # def run(
    #     self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    # ):
    #     required_slots = ["name", "number", ]

    #     for slot_name in required_slots:
    #         if tracker.slots.get(slot_name) is None:
    #             # The slot is not filled yet. Request the user to fill this slot next.
    #             return [SlotSet("requested_slot", slot_name)]

    #     # All slots are filled.
    #     return [SlotSet("requested_slot", None)]

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


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
from backend.prediction import get_info, get_preventive_measures, get_home_remedies, get_diet, get_symptoms
from backend.unique_symptoms import unique
import datetime
from rasa_sdk.events import ReminderScheduled
from rasa_sdk import Action

from actions.helper import removeAmbiguousSymptom, create_user, predict, get_diseases, stored_prognosed_disease, get_duration

class ActionSetReminder(Action):
    """Schedules a reminder, supplied with the last message's entities."""

    def name(self) -> Text:
        return "action_set_reminder"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # dispatcher.utter_message("I will remind you in 10 seconds.")

        date = datetime.datetime.now() + datetime.timedelta(hours=1)
        entities = tracker.latest_message.get("entities")

        reminder = ReminderScheduled(
            "water_reminder",
            trigger_date_time=date,
            entities=entities,
            name="water_reminder",
            kill_on_user_message=False,
        )
        print("Reminder scheduled.")
        return [reminder]

class ActionBookingReminder(Action):
    def name(self):
        return "action_water_reminder"

    def run(self, dispatcher, tracker, domain):
        print("Reminder called.")
        dispatcher.utter_message("Please have a glass of water.")
        date = datetime.datetime.now() + datetime.timedelta(hours=2)
        entities = tracker.latest_message.get("entities")
        return [ReminderScheduled(
                "water_reminder",
                trigger_date_time=date,
                entities=entities,
                name="water_reminder",
                kill_on_user_message=False,
            )]

class UserForm(Action):
    def name(self):
        return "profile_form"

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
        
        if type(name) == str:
            name = name.split(" ")
        print(type(name))
        if type(name) == list:
            if len(name) == 1:
                name = name[0]
            if len(name) == 2 : 
                name1 = name[0].split(" ")
                if len(name1) == 2:
                    name = name[0]
                else:
                    if name[0] == name[1]:
                        name = name[0]
                    else:
                        name = name[0] + " " + name[1]
                name = name.title()
            else:
                name1 = name[0].split(" ")
                if len(name1) == 2:
                    name = name[0]
                elif len(name[1].split(" ")) == 2:
                    name = name[1]
                else:
                    if name[0] == name[1]:
                        name = name[0]
                    else:
                        name = name[0] +" " + name[1]

        if type(number) == list:
            number = number[0]

        if type(email) == list:
            email = email[0]

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
        dispatcher.utter_message(text= "Yay you're now logged in! You may ask any queries that you have or start expressing any problems that you might be facing")
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

class ActionAccurateDiseaseReminder(Action):
    def name(self):
        return "action_acc_disease_reminder"

    def run(self, dispatcher, tracker, domain):
        print("disease reminder called.")
        diseases = get_diseases(tracker.get_slot('email'))
        print(diseases['prognosis'])
        buts = list()
        for d in diseases['prognosis']:
            d = d.lower()
            btn = {
                "payload": '/prognosis_disease{"disease":"'+d+'"}',
                 "title": d
            }
            buts.append(btn)
        dispatcher.utter_message(text = "Which disease are you actually suffering from after diagnosis ?", buttons = buts
        # [
        #         {"payload": '/take_disease{"disease": "fever"}', "title": "Fever"},
        #         {"payload": '/take_disease{"disease": "cough"}', "title": "Cough"},
        #     ]
        )

class SymptomsForm(Action):

    def name(self):
        return "symptoms_form"

class SymptomsFormSubmit(Action):

    def name(self):
        return "action_symptoms_form_submit"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict"):
    
        allsymptoms = tracker.get_slot('all_symptoms')
        email = tracker.get_slot('email')
        if type(email) == list:
            email = email[0]
        resp = predict(allsymptoms, email)
        
        print(resp.json()['flag'])
        text = ""
        if resp.json()['flag'] == 1:
            print(resp.json()['dis'])
            text = "Here is your disease prognosis info : {}\nDo you want to clear out your symptoms ?".format(resp.json()['dis'])
        else:
            temp = resp.json().copy()
            del temp['flag']
            text = "Here is your disease prognosis info : {}\nDo you want to clear out your symptoms ?".format(temp)
            
        dispatcher.utter_message(text = text)
        date = datetime.datetime.now() + datetime.timedelta(seconds=15)
        entities = tracker.latest_message.get("entities")

        if resp.json()['flag'] == 0:
            return [
                SlotSet('symptoms', None),
                SlotSet('more_symptoms', None),
                SlotSet('duration', None)
            ]
        else:
            reminder = ReminderScheduled(
                "acc_disease",
                trigger_date_time=date,
                entities=entities,
                name="acc_disease_reminder",
                kill_on_user_message=False,
            )
            print("disease reminder scheduled.")
            return [
                reminder,
                SlotSet('symptoms', None),
                SlotSet('more_symptoms', None),
                SlotSet('duration', None)
            ]

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
        }

        symps.append(val)

        if slot_value == "yes":
            return {
                "symptoms": None,
                "more_symptoms": None,
                "duration": None,
                "all_symptoms": symps
            }
        else:
            print("IN NO")
            return {"more_symptoms": "yes", "all_symptoms": symps}

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

        print("RESETING SLOTS")
        return {
            "symptoms" : symptom,
            "more_symptoms": None,
            "duration": None,
        }

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

class ActionResetSymptoms(Action):
    
    def name(self):
        return "action_reset_symptoms"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict"):
        intent = tracker.latest_message['intent'].get('name')
        print(intent)
        if intent == 'affirm':
            print("IN AFFIRM")
            dispatcher.utter_message(text = 'Symptoms Cleared.\nIf you have any other symptoms or want information about some disease, feel free to text.')
            return [
                SlotSet('all_symptoms', None)
            ]
        else:
            print("IN DENY")
            dispatcher.utter_message(text = 'Okay.\nIf you have any other symptoms or want information about some disease, feel free to text.')
            return []

class Login(Action):
    def name(self):
        return "action_login"
    
    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict"):
        
        email_id = "priyav.mehta@spit.ac.in"
        email = tracker.get_slot('email')
        if type(email) == list:
            email = email[0]
        request_url = "http://127.0.0.1:5000/login"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        data = {
            "email" : email,
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
            res = response.json()
            if "success" in res['msg'].lower():
                print("IN LOGIN SUCCESS")
                dispatcher.utter_message(template="utter_login_success")
                return [
                    SlotSet('loggedin', True),
                    SlotSet('name', res['user']['name']),
                    SlotSet('diabetes', res['user']['diabetes']),
                    SlotSet('blood_pressure', res['user']['blood_pressure']),
                    SlotSet('migraine', res['user']['migraine']),
                    SlotSet('frequent_cold', res['user']['frequent_cold']),
                    SlotSet('frequent_cough', res['user']['frequent_cough']),
                    SlotSet('number', res['user']['number']),
                ]
            else:
                print("IN LOGIN FAILURE")
                dispatcher.utter_message(template="utter_wrong_email")
                return [
                    SlotSet('loggedin', False),
                ]
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        dispatcher.utter_message(template="utter_wrong_email")
        return [SlotSet('loggedin', False)]

class ActionDiseaseInfoReminder(Action):
    def name(self):
        return "action_disease_info_reminder"

    def run(self, dispatcher, tracker, domain):
        
        duration = get_duration(tracker.get_slot('email'))
        print(duration)
        print(type(duration))
        if duration['duration'] != 0:
            disease = duration['disease']
            info = ""

            if duration['duration'] % 3 == 0:
                info = get_diet(disease)

            elif duration['duration'] % 3 == 1:
                info = get_home_remedies(disease)

            else:
                info = get_preventive_measures(disease)

            print(info)

            date = datetime.datetime.now() + datetime.timedelta(seconds=10)
            entities = tracker.latest_message.get("entities")
            dispatcher.utter_message(text = info)
            return [ReminderScheduled(
                "disease_info_reminder",
                trigger_date_time=date,
                entities=entities,
                name="disease_info_reminder_daily",
                kill_on_user_message=False,
            )]
        else:
            return []

class PrognosisDiseaseInfo(Action):
    def name(self):
        return "action_prog_disease_info"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict"):
        disease = tracker.get_slot('disease')
        email = tracker.get_slot('email')
        if type(email) == list:
            email = email[0]
        msg = stored_prognosed_disease(email, disease)
        print(msg)
        info = get_info(disease)
        print(info)

        date = datetime.datetime.now() + datetime.timedelta(seconds=10)
        entities = tracker.latest_message.get("entities")

        reminder = ReminderScheduled(
            "disease_info_reminder",
            trigger_date_time=date,
            entities=entities,
            name="disease_info_reminder_daily",
            kill_on_user_message=False,
        )
        
        dispatcher.utter_message(template = "utter_disease_info",desc = info)
        return [reminder]

class Information(Action):
    def name(self):
        return "action_info"

    def run(self, dispatcher, tracker: Tracker, domain: "DomainDict"):
        disease = tracker.get_slot('disease')
        intent = tracker.latest_message['intent'].get('name')
        print(intent)
        info = ""
        if intent == 'take_home_remedies':
            info = get_home_remedies(disease)
        elif intent == 'take_diet':
            info = get_diet(disease)
        elif intent == 'take_prevention':
            info = get_preventive_measures(disease)
        elif intent == 'take_disease_symptoms':
            info = get_symptoms(disease)
        else:
            info = get_info(disease)

        print(info)
        dispatcher.utter_message(text = info)
        
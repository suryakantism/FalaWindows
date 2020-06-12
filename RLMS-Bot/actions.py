from typing import Dict, Text, Any, List, Union, Optional

from rasa_sdk import Tracker, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction
from rasa_sdk.events import SlotSet

import requests
from requests.exceptions import RequestException, Timeout, URLRequired, TooManyRedirects, HTTPError, ConnectionError, FileModeWarning, ConnectTimeout, ReadTimeout
import re
try:         
    import extra.config as config
except ImportError:
    import config

class FAQFixForm(FormAction):
    def name(self):
        return "faq_fix_form"

    @staticmethod
    def required_slots(
        tracker: Tracker) -> List[Text]: return ["faq_userinput_question", "faq_intended_section", "faq_intended_question"]

    def slot_mappings(self):
        return {
            "faq_userinput_question": [self.from_text()],
            "faq_intended_section": [self.from_text()],
            "faq_intended_question": [self.from_text()]
        }

    ## Overwrite class base method
    def request_next_slot(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],):
        for slot in self.required_slots(tracker):
            if self._should_request_slot(tracker, slot):
                if slot == "faq_intended_question":
                    # Fetch buttons list here
                    #buttons_list = [{"title": "Button 1", "payload": "Some value"}, {"title": "Button 2", "payload": "Some value"}]
                    intended_section = tracker.get_slot("faq_intended_section")

                    url = f'{config.UTILITY_SERVER_URL}/tfidf/raw/{intended_section}'
                    buttons_data = requests.get(url).json()['data']

                    buttons_list = []
                    for data in buttons_data:
                        buttons_list.append({"title": data, "payload": data})    

                    dispatcher.utter_message(text="Please select the intended question.", buttons=buttons_list, **tracker.slots)
                    return [SlotSet("requested_slot", slot)]
                
                else:
                    dispatcher.utter_message(template=f"utter_ask_{slot}", **tracker.slots)
                    return [SlotSet("requested_slot", slot)]
                

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        user_data = tracker.get_slot("faq_userinput_question")
        intended_section = tracker.get_slot("faq_intended_section")
        intended_question = tracker.get_slot("faq_intended_question")

        url = f'{config.UTILITY_SERVER_URL}/tfidf/update'
        data = {"user_data": user_data, "section": intended_section, "question": intended_question}
        response = requests.post(url, json=data).json()
        print(f"[TFIDF UPDATE REQUEST] Utility server responded with: {response}")
        return []


class OTDPaymentForm(FormAction):
    def name(self):
        return "otd_payment_form"

    @staticmethod
    def required_slots(
        tracker: Tracker) -> List[Text]: return ["customer_bank_name", "customer_account_number", "customer_mobile_number"]

    def slot_mappings(self):
        return {
            "customer_bank_name": [self.from_text()],
            "customer_account_number": [self.from_text()],
            "customer_mobile_number": [self.from_text()]
        }


    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        b = tracker.get_slot("customer_bank_name")
        a = tracker.get_slot("customer_account_number")
        m = tracker.get_slot("customer_mobile_number")

        dispatcher.utter_message(f"Alright, I've set up a payment gateway URL for you to finalize your payment. Please follow this link. Your details are: \nBank Name: {b}\nAcount Number: {a}\n Mobile Number:{m}")
        return []


class SRPPaymentForm(FormAction):
    def name(self):
        return "srp_payment_form"

    @staticmethod
    def required_slots(
        tracker: Tracker) -> List[Text]: return ["customer_bank_name", "customer_account_number", "customer_mobile_number", "ssn_digits", "cycle_date"]

    def slot_mappings(self):
        return {
            "customer_bank_name": [self.from_text()],
            "customer_account_number": [self.from_text()],
            "customer_mobile_number": [self.from_text()],
            "ssn_digits": [self.from_text()], 
            "cycle_date": [self.from_text()]
        }


    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:

        b = tracker.get_slot("customer_bank_name")
        a = tracker.get_slot("customer_account_number")
        m = tracker.get_slot("customer_mobile_number")
        s = tracker.get_slot("ssn_digits")
        c = tracker.get_slot("cycle_date")

        dispatcher.utter_message(f"Alright, I've set up a payment gateway URL for you to finalize your payment. Please follow this link. Your details are:\nBank Name: {b}\nAcount Number: {a}\nMobile Number:{m}\nLast 4 SSN Digits: {s}\nCycle Date: {c}")
        return []


class DynamicCannedResponse(Action):
    def name(self) -> Text:
        return "action_get_canned_dynamic_response"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent_name = tracker.latest_message.get('intent')['name']
        metadata = extract_metadata(tracker)

        loan_number = metadata["loan_number"]
        question_id = intent_name

        print(loan_number)
        print(question_id)

        try:
            url = f'{config.UTILITY_SERVER_URL}/canned/dynamic/request'
            data = {"loan_number": loan_number, "question_id": question_id}
            response_data = requests.post(url, json=data).json()

            print(response_data)

            response_lines = response_data["responses"]

            for response in response_lines:
                if "text" in response: 
                    dispatcher.utter_message(response["text"])

                elif "listed_suggestions" in response: 
                    dispatcher.utter_message(json_message={"listed_suggestions": response["listed_suggestions"]})

                elif "tabular_suggestions" in response: 
                    dispatcher.utter_message(json_message={"tabular_suggestions": response["tabular_suggestions"]})

            return []

        except (RequestException, Timeout, URLRequired, TooManyRedirects, HTTPError, ConnectionError, FileModeWarning, ConnectTimeout, ReadTimeout):
            dispatcher.utter_message("There seems to be an issue in our servers. Please let an admin know.")
            return []


class ActionFAQTrigger(Action):
    def name(self) -> Text:
        return "action_trigger_faq"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        message = tracker.latest_message.get('text')
        intent = tracker.latest_message.get('intent')['name']
        section = intent[4:]

        url = f'{config.UTILITY_SERVER_URL}/tfidf/request'
        data = {"user_input": message, "section": section}
        response = requests.post(url, json=data).json()

        dispatcher.utter_message(response['response1'])
        return []


class ActionSetQuestionData(Action):
    def name(self) -> Text:
        return "action_set_question_data"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        value = tracker.latest_message.get('text')
        return[SlotSet("faq_userinput_question", value)]


class ActionGetIsAdmin(Action):
    def name(self) -> Text:
        return "action_get_is_admin"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        metadata = extract_metadata(tracker)
        is_admin = False

        if check_admin(metadata):
            is_admin = True

        return[SlotSet("is_admin", is_admin)]


class ActionGetUserType(Action):
    def name(self) -> Text:
        return "action_get_user_type"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        metadata = extract_metadata(tracker)
        is_logged_in = False

        if check_is_logged_in(metadata):
            is_logged_in = True

        print("Value: ", is_logged_in)

        return[SlotSet("is_logged_in", is_logged_in)]

# Util
# =============================
def extract_metadata(tracker):
    events = tracker.current_state()['events']
    user_events = []
    for e in events:
        if e['event'] == 'user':
            user_events.append(e)

    data = user_events[-1]['metadata']
    return data

def check_admin(metadata):
    return 'is_admin' in metadata

def check_is_logged_in(metadata):
    return 'loan_number' in metadata
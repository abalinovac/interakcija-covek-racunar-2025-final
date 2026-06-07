from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import requests
import unicodedata

def normalize(text: str) -> str:
    return (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("utf-8")
        .lower()
    )

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World from Actions!")
        return []
    
class ActionLatestToys(Action):     #RADI

    def name(self) -> Text:
        return "action_latest_toys"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = 'https://toy.pequla.com/api/toy'
        rsp = requests.get(url)
        toys = rsp.json()

        if len(toys) >= 3:
            bot_response = {
                "type": "toy_list",
                "data": toys[-3:]
            }
            dispatcher.utter_message(text='Here are some toys', attachment=bot_response)
        else:
            dispatcher.utter_message(text='Not enought toys found') 
        return []
    
class ActionSearchToys(Action):     #RADI

    def name(self) -> Text:
        return "action_search_toys"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        criteria = tracker.get_slot("search_criteria")

        print("SEARCH CRITERIA:", criteria)

        url = "https://toy.pequla.com/api/toy"
        rsp = requests.get(url)
        toys = rsp.json()

        filtered_toys = []

        if criteria:
            filtered_toys = [
                toy for toy in toys
                if criteria.lower() in toy["name"].lower()
            ]
        else:
            filtered_toys = toys

        print("NUMBER OF RESULTS:", len(filtered_toys))

        dispatcher.utter_message(
            text=f"Here are the search results for {criteria}",
            attachment={
                "type": "toy_list",
                "data": filtered_toys
            }
        )

        return []
    
class ActionAgeList(Action):          #RADI

    def name(self) -> Text:
        return "action_age_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = 'https://toy.pequla.com/api/age-group'
        rsp = requests.get(url)

        dispatcher.utter_message(
                text='Here are all age groups:',
                attachment={
                "type": "age_list",
                "data": rsp.json()
               }
            )
        return []

class ActionTypeList(Action):           #RADI

    def name(self) -> Text:
        return "action_type_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = 'https://toy.pequla.com/api/type'
        rsp = requests.get(url)

        dispatcher.utter_message(
                text='Here are all types of toys:',
                attachment={
                "type": "type_list",
                "data": rsp.json()
               }
            )
        return []

class ActionExtractToy(Action):

    def name(self) -> Text:
        return "action_extract_toy"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        criteria = tracker.get_slot("order_criteria")

        rsp = requests.get("https://toy.pequla.com/api/toy")
        toys = rsp.json()

        exact_toy = next(
            (
                toy for toy in toys
                if criteria.lower() in toy["name"].lower()
            ),
            None
        )

        if exact_toy:
            dispatcher.utter_message(
                text=f"Selected toy: {exact_toy['name']}",
                attachment={
                    "type": "order_toy",
                    "data": exact_toy
                }
            )

            return [
                SlotSet("toy_permalink", exact_toy["permalink"])
            ]
        
        dispatcher.utter_message(
            text="No toy for that criteria found!"
        )

        return []
    
class ActionListDeliveryMethod(Action):

    def name(self) -> Text:
        return "action_list_delivery_method"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
        dispatcher.utter_message(
                text='Here are all the available delivery methods:',
                attachment={
                "type": "simple_list",
                "data": ['Dostava na kućnu adresu (Kurirska služba)', 'Preuzimanje u prodavnici (Beograd)', 'Preuzimanje u prodavnici (Novi Sad)']
               }
            )
        return [] 
   
class ActionSelectDeliveryMethod(Action):  #izmenjeno sve proveriti da li radi prilikom narudzbine

    def name(self) -> Text:
        return "action_select_deliveryMethod"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        criteria = tracker.get_slot("delivery_criteria")
        delivery = ['Dostava na kućnu adresu (Kurirska služba)', 'Preuzimanje u prodavnici (Beograd)', 'Preuzimanje u prodavnici (Novi Sad)']
        matched = []

        if criteria:
            normalized_criteria = normalize(criteria)

            for deliver in delivery:
                if normalize(deliver) == normalized_criteria:
                    matched.append(deliver)

        if len(matched) > 0:
            exact_delivery = matched[0]
            dispatcher.utter_message(text='Selected delivery method: '+ exact_delivery)
            return [SlotSet('delivery_id',exact_delivery)]
        
        dispatcher.utter_message(text='No delivery method for that criteria found!') 
        return []
    
class ActionSelectDelivery(Action):

    def name(self) -> Text:
        return "action_select_delivery"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        criteria = tracker.get_slot("delivery_criteria")
        delivery = ['Kurirska služba', 'Preuzimanje u prodavnici (Beograd)', 'Preuzimanje u prodavnici (Novi Sad)']
        matched = []

        if criteria:
            normalized_criteria = normalize(criteria)

            for deliver in delivery:
                if normalize(deliver) == normalized_criteria:
                    matched.append(deliver)

        if len(matched) > 0:
            exact_delivery = matched[0]
            dispatcher.utter_message(text='Selected delivery method: '+ exact_delivery)
            return [SlotSet('deliveryMethod',exact_delivery)]
        
        dispatcher.utter_message(text='No delivery method for that criteria found!') 
        return []
    
class ActionListOrder(Action):

    def name(self) -> Text:
        return "action_list_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        order_list= [
            'Toy: ' +  tracker.get_slot("toy_permalink"),
            'Delivery method: ' +  tracker.get_slot("deliveryMethod"),  #videti za delivery
            'Price: ' +  tracker.get_slot("price_id"),
            'Quantity: ' +  tracker.get_slot("quantity"),
        ]

        dispatcher.utter_message(
                text='This is your current order:',
                attachment={
                "type": "simple_list",
                "data": order_list
               }
            )
        return []

class ActionPlaceOrder(Action):

    def name(self) -> Text:
        return "action_place_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        order_details= {
            'Toy: ' +  tracker.get_slot("toy_permalink"),
            'Delivery method: ' +  tracker.get_slot("deliveryMethod"),  #videti za delivery
            'Price: ' +  tracker.get_slot("price_id"),
            'Quantity: ' +  tracker.get_slot("quantity"),
        }
               
        dispatcher.utter_message(
                text='Your order has been placed:',
                attachment={
                "type": "create_order",
                "data": order_details
               }
            )
        return []
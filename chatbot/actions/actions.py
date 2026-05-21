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
    
class ActionLatestToys(Action):

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
    
class ActionSearchToys(Action):

    def name(self) -> Text:
        return "action_search_toys"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        criteria=tracker.get_slot("search_criteria")

        url = 'https://toy.pequla.com/api/toy?search=' + criteria
        rsp = requests.get(url)
        toys = rsp.json()

        dispatcher.utter_message(
                text='Here are the search results for ' + criteria,
                attachment={
                "type": "toy_list",
                "data": toys
               }
            )
        return []
    
class ActionAgeList(Action):

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

class ActionTypeList(Action):

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
    
class ActionDirectorList(Action):

    def name(self) -> Text:
        return "action_director_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = 'https://movie.pequla.com/api/director'
        rsp = requests.get(url)

        dispatcher.utter_message(
                text='Here are all the available directors:',
                attachment={
                "type": "director_list",
                "data": rsp.json()
               }
            )
        return []

class ActionExtractToy(Action):

    def name(self) -> Text:
        return "action_extract_toy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        criteria=tracker.get_slot("order_criteria")

        url = 'https://toy.pequla.com/api/toy?search=' + criteria
        rsp = requests.get(url)
        toys = rsp.json()

        if len(toys) > 0:
            exact_toy = toys[0]
            dispatcher.utter_message(text='Selected toy: '+ exact_toy['title'])
            return [SlotSet('toy_permalink',exact_toy['shortUrl'])]
        
        dispatcher.utter_message(text='No toy for that criteria found!') 
        return []
    
class ActionListCinema(Action):

    def name(self) -> Text:
        return "action_list_cinema"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
        dispatcher.utter_message(
                text='Here are all the available cinemas:',
                attachment={
                "type": "simple_list",
                "data": ['Ušće', 'Rakovica', 'Rajićeva', 'Ada']
               }
            )
        return []
    
class ActionListPrice(Action):

    def name(self) -> Text:
        return "action_list_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
        dispatcher.utter_message(
                text='Here are all prices:',
                attachment={
                "type": "simple_list",
                "data": ['Velika', 'Mala', 'Privatna']
               }
            )
        return []
    
class ActionListTime(Action):

    def name(self) -> Text:
        return "action_list_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       
        dispatcher.utter_message(
                text='Here are all the available timetables:',
                attachment={
                "type": "simple_list",
                "data": ['Utorak 22h', 'Sreda 21h', 'Petak 20h', 'Petak 22h']
               }
            )
        return []
   
class ActionSelectCinema(Action):

    def name(self) -> Text:
        return "action_select_cinema"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        criteria = tracker.get_slot("cinema_criteria")
        cinemas = ['Ušće', 'Rakovica', 'Rajićeva', 'Ada']
        matched = []

        if criteria:
            normalized_criteria = normalize(criteria)

            for cinema in cinemas:
                if normalize(cinema) == normalized_criteria:
                    matched.append(cinema)

        if len(matched) > 0:
            exact_cinema = matched[0]
            dispatcher.utter_message(text='Selected cinema: '+ exact_cinema)
            return [SlotSet('cinema_id',exact_cinema)]
        
        dispatcher.utter_message(text='No cinema for that criteria found!') 
        return []
    
class ActionSelectPrice(Action):

    def name(self) -> Text:
        return "action_select_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        criteria = tracker.get_slot("price_criteria")
        prices = ['Velika', 'Mala', 'Privatna']
        matched = []

        if criteria:
            normalized_criteria = normalize(criteria)

            for price in prices:
                if normalize(price) == normalized_criteria:
                    matched.append(price)

        if len(matched) > 0:
            exact_price = matched[0]
            dispatcher.utter_message(text='Selected price: '+ exact_price)
            return [SlotSet('price_id',exact_price)]
        
        dispatcher.utter_message(text='No prices for that criteria found!') 
        return []
    
class ActionSelectTime(Action):

    def name(self) -> Text:
        return "action_select_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        criteria = tracker.get_slot("time_criteria")
        times = ['Utorak 22h', 'Sreda 21h', 'Petak 20h', 'Petak 22h']
        matched = []

        if criteria:
            normalized_criteria = normalize(criteria)

            for time in times:
                if normalize(time) == normalized_criteria:
                    matched.append(time)

        if len(matched) > 0:
            exact_time = matched[0]
            dispatcher.utter_message(text='Selected time: '+ exact_time)
            return [SlotSet('time_id',exact_time)]
        
        dispatcher.utter_message(text='No time for that criteria found!') 
        return []
    
class ActionSelectCount(Action):

    def name(self) -> Text:
        return "action_select_time"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        criteria = tracker.get_slot("count_criteria")
        dispatcher.utter_message(text='Selected count: '+ criteria)
        return [SlotSet('ticket_count',criteria)]
    
class ActionListOrder(Action):

    def name(self) -> Text:
        return "action_list_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        order_list= [
            'Movie: ' +  tracker.get_slot("movie_permalink"),
            'Cienema: ' +  tracker.get_slot("cinema_id"),
            'Price: ' +  tracker.get_slot("price_id"),
            'Time: ' +  tracker.get_slot("time_id"),
            'Count: ' +  tracker.get_slot("ticket_count"),
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
            "movie": tracker.get_slot("movie_permalink"),
            "cinema": tracker.get_slot("cinema_id"),
            "Price":  tracker.get_slot("price_id"),
            "time": tracker.get_slot("time_id"),
            "count": tracker.get_slot("ticket_count")
        }
               
        dispatcher.utter_message(
                text='Your order has been placed:',
                attachment={
                "type": "create_order",
                "data": order_details
               }
            )
        return []
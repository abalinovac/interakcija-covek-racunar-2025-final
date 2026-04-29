from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests


class ActionHelloWorld(Action):

     def name(self) -> Text:
         return "action_hello_world"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message(text="Hello World from Actions!")

         return []

class ActionLatestMovies(Action):

     def name(self) -> Text:
         return "action_latest_movies"

     def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = 'https://movie.pequla.com/api/movie'
        rsp = requests.get(url)
        movies = rsp.json()

        if len(movies) >= 3:
            bot_response = {
                "type": "movie_list",
                "data": movies[-3:]
            }
            dispatcher.utter_message(text='Here are some movies', attachment=bot_response)
        else:
            dispatcher.utter_message(text='Not enought movies found') 
        return []

class ActionSearchMovies(Action):

    def name(self) -> Text:
        return "action_search_movies"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        criteria=tracker.get_slot("search_criteria")

        url = 'https://movie.pequla.com/api/movie?search=' + criteria
        rsp = requests.get(url)
        movies = rsp.json()

        dispatcher.utter_message(
                text='Here are the search results for ' + criteria,
                attachment={
                "type": "movie_list",
                "data": movies
               }
            )
        return []

class ActionGenreList(Action):

    def name(self) -> Text:
        return "action_genre_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = 'https://movie.pequla.com/api/genre'       #poziva api upit žanrovi
        rsp = requests.get(url)

        dispatcher.utter_message(
                text='Here are all the available genres: ',
                attachment={
                "type": "genre_list",
                "data": rsp.json()
               }
            )
        return []
    
class ActionActorList(Action):

    def name(self) -> Text:
        return "action_actor_list"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        url = 'https://movie.pequla.com/api/actor'       
        rsp = requests.get(url)

        dispatcher.utter_message(
                text='Here are all actors ',
                attachment={
                "type": "actor_list",
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
                text='Here are all directors: ',
                attachment={
                "type": "director_list",
                "data": rsp.json()
               }
            )
        return []
    
class ActionOrderMovies(Action):

    def name(self) -> Text:
        return "action_order_movie"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        criteria=tracker.get_slot("order_criteria")

        url = 'https://movie.pequla.com/api/movie?search=' + criteria
        rsp = requests.get(url)
        movies = rsp.json()

        if len(movies) > 0:
            bot_response = {
                "type": "order_movie",
                "data": movies[0]
            }
            dispatcher.utter_message(text='Placing an order...', attachment=bot_response)
        else:
            dispatcher.utter_message(text='No movie for that critetira found!') 
        return []
       

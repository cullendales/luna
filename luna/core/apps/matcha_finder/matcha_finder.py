import sqlite3
import requests
import time
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from dotenv import load_dotenv
import os
from text_and_audio.stt import get_command
from text_and_audio.tts import respond

load_dotenv()
API_KEY = os.getenv("google_places_key")
MAX_CAFES = 50

def check_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt_tab')
    except LookupError:
        try:
            nltk.download('punkt_tab')
        except:
            nltk.download('punkt')

    try:
        nltk.data.find('taggers/averaged_perceptron_tagger_eng')
    except LookupError:
        try:
            nltk.download('averaged_perceptron_tagger_eng')
        except:
            try:
                nltk.data.find('taggers/averaged_perceptron_tagger')
            except LookupError:
                nltk.download('averaged_perceptron_tagger')

    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

check_nltk_data()
stop_words = stopwords.words('english')

class Cafe:
    def __init__(self, place_id, name, address, lon, lat, rating, reviews):
        self.place_id = place_id
        self.name = name
        self.address = address
        self.lon = lon
        self.lat = lat
        self.rating = rating
        self.keywords = []

        if reviews:
            self.extract_keywords(reviews)

    def extract_keywords(self, reviews):
        tokenized = word_tokenize(reviews.lower())
        linking_verbs = {'is', 'are', 'was', 'were', 'seems', 'tastes', 'feels'}
        custom_stop_words = set(stop_words) - linking_verbs
        wordsList = [w for w in tokenized if w not in custom_stop_words and w.isalpha()]
        
        if 'matcha' not in wordsList:
            return

        tagged_reviews = nltk.pos_tag(wordsList)

        for i, (word, tag) in enumerate(tagged_reviews):
            if word == 'matcha':
                #checking word before for adj
                if i > 0 and tagged_reviews[i-1][1] in ["JJ", "JJR", "JJS"]:
                    self.keywords.append(tagged_reviews[i-1][0])   
                #check for linking verb and then adj
                if i < len(tagged_reviews) - 2:
                    next_word, next_tag = tagged_reviews[i+1]
                    if next_word in linking_verbs:
                        if i+2 < len(tagged_reviews) and tagged_reviews[i+2][1] in ["JJ", "JJR", "JJS"]:
                            self.keywords.append(tagged_reviews[i+2][0])
                        elif i+3 < len(tagged_reviews) and tagged_reviews[i+3][1] in ["JJ", "JJR", "JJS"]:
                            self.keywords.append(tagged_reviews[i+3][0])     
                    #check for same pattern above but after 'latte'             
                    elif next_word == 'latte' and i < len(tagged_reviews) - 3:
                        third_word, third_tag = tagged_reviews[i+2]
                        if third_word in linking_verbs:
                            if i+3 < len(tagged_reviews) and tagged_reviews[i+3][1] in ["JJ", "JJR", "JJS"]:
                                self.keywords.append(tagged_reviews[i+3][0])
                            elif i+4 < len(tagged_reviews) and tagged_reviews[i+4][1] in ["JJ", "JJR", "JJS"]:
                                self.keywords.append(tagged_reviews[i+4][0])      
      
class MatchaFinder:
    def __init__(self, api_key):
        self.api_key = api_key
        self.conn = sqlite3.connect('matcha_lattes.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS matcha_lattes(
            ID TEXT PRIMARY KEY,
            NAME TEXT,
            ADDRESS TEXT,
            LON FLOAT,
            LAT FLOAT,
            RATING REAL,
            KEYWORDS TEXT,
            CITY TEXT
        );''')
        self.conn.commit()

    def coordinates(self, city):
        url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {"address": city, "key": self.api_key}

        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data['status'] == 'OK':
            loc = data['results'][0]['geometry']['location']
            return loc['lat'], loc['lng']
        else:
            raise Exception (f"Coordinates could not be retrieved: {data['status']}")
        

    def get_reviews(self, place_id):
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            "key": self.api_key,
            "place_id": place_id,
            "fields": "reviews"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
            
        if data.get("status") == "OK" and "result" in data:
            reviews = data["result"].get("reviews", [])
            review_text = " ".join([review.get("text", "") for review in reviews])
            return review_text if review_text.strip() else None
        else:
            raise Exception (f"Error: {data['status']}")

    def find_cafes(self, lat, lon, city):
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "key": self.api_key,
            "location": f"{lat},{lon}",
            "radius": 10000,
            "type": "cafe",
            "keyword": "matcha latte"           
        }

        cafes = []
        max_cafes = MAX_CAFES

        while len(cafes) < max_cafes:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "OK":
                print("There is an API error: ", data.get("status"))
                if data.get("status") == "ZERO_RESULTS":
                    print("There are unfortunately no cafes serving a matcha latte in your area")
                break

            for result in data.get("results", []):
                reviews = self.get_reviews(result["place_id"])
                cafe = Cafe(
                    place_id = result["place_id"],
                    name = result.get("name", ""),
                    address = result.get("vicinity", ""),
                    rating = result.get("rating", 0),
                    lat = result["geometry"]["location"]["lat"],
                    lon = result["geometry"]["location"]["lng"],
                    reviews = reviews
                )
                cafes.append(cafe)
                self.add_cafe(cafe, city)

                time.sleep(0.1)

            if 'next_page_token' in data and len(cafes) < max_cafes:
                time.sleep(2)
                params['pagetoken'] = data['next_page_token']

                if 'location' in params:
                    del params['location']
                if 'radius' in params:
                    del params['radius']
                if 'type' in params:
                    del params['type']
                if 'keyword' in params:
                    del params['keyword']
            else:
                break

        return cafes
    
    def add_cafe(self, cafe, city):
        keywords_res = ", ".join(cafe.keywords) if cafe.keywords else ""
        self.cursor.execute('''INSERT OR IGNORE INTO matcha_lattes (ID, NAME, ADDRESS, LON, LAT, RATING, KEYWORDS, CITY)
                            VALUES (?,?,?,?,?,?,?,?)''',
                            (cafe.place_id, cafe.name, cafe.address, cafe.lon, cafe.lat, cafe.rating, keywords_res, city.lower()))
        self.conn.commit()

    def load_cached_cafes(self, city):
        self.cursor.execute("SELECT * FROM matcha_lattes WHERE CITY = ?", (city.lower(),))
        rows = self.cursor.fetchall()

        cafes = []
        for row in rows:
            cafe = Cafe(
                place_id=row[0],
                name=row[1],
                address=row[2],
                lon=row[3],
                lat=row[4],
                rating=row[5],
                reviews=None 
            )
            cafe.keywords = row[6].split(", ") if row[6] else []
            cafes.append(cafe)
        return cafes

def find_matcha(cheetah):
    search = MatchaFinder(API_KEY)
    respond("What city would you like to find a matcha latte in?")
    city = get_command(cheetah)
    respond(f"Searching all cafes in {city} for delicious matcha lattes")

    cafes = search.load_cached_cafes(city)  

    if not cafes:
        lat, lon = search.coordinates(city)
        cafes = search.find_cafes(lat, lon, city)
    if len(cafes) > 5:
        for cafe in cafes[:5]:
            respond(f"{cafe.name} which has a {cafe.rating} star rating")
            if cafe.keywords:
                respond(f"People are saying: {', '.join(cafe.keywords)} about their matcha lattes")
    else:
        for cafe in cafes:
            respond(f"{cafe.name} which has a {cafe.rating} star rating")
            if cafe.keywords:
                respond(f"People are saying: {', '.join(cafe.keywords)} about their matcha lattes")

    answer = ""
    rating_filter = "1"
    user_keywords = []
    all_ratings = []
    correct_option = True

    while answer != "quit":

        if correct_option:
            print("Would you like to filter results more?")

        respond("Respond one to filter by adjectives in reviews describing a cafe's Matcha Latte")
        respond("Respond two to filter by rating threshold")
        respond("Respond three to reset all previous filters")
        respond("Respond exit to exit the program")
        answer = get_command(cheetah)

        correct_option = True

        if answer == "one":
            user_keywords = input("Enter keywords to filter by seperated by a space: ").split()
            print()
            cafe_list = []
    
            for cafe in cafes:
                for key in user_keywords:            
                    if key in cafe.keywords and cafe.rating >= float(rating_filter):
                        if cafe.name not in cafe_list:
                            cafe_list.append(cafe.name)
            
            if not cafe_list:
                user_keywords.clear()
                respond("No cafes match search criteria.")
                print()
            else:
                if len(cafes) > 5:
                    for cafe in cafes[:5]:
                        if cafe.name in cafe_list and cafe.rating >= float(rating_filter):
                            respond(f"{cafe.name} which has a {cafe.rating} star rating")
                            if cafe.keywords:
                                respond(f"People are saying: {', '.join(cafe.keywords)} about their matcha lattes")
                else:
                    for cafe in cafes:
                        if cafe.name in cafe_list and cafe.rating >= float(rating_filter):
                            respond(f"{cafe.name} which has a {cafe.rating} star rating")
                            if cafe.keywords:
                                respond(f"People are saying: {', '.join(cafe.keywords)} about their matcha lattes")

                    
        elif answer == "two":
            respond("Say a number from 1 - 5 to only see cafes with that rating or higher")
            rating_filter = get_command(cheetah)
            contains_cafe = False
            all_ratings.append(rating_filter)


            if not user_keywords:  
                if cafes > 5:    
                    for cafe in cafes[:5]:
                        if cafe.rating >= float(rating_filter):
                                respond(f"{cafe.name} which has a {cafe.rating} star rating")
                                if cafe.keywords:
                                    respond(f"People are saying: {', '.join(cafe.keywords)} about their matcha lattes")
                                contains_cafe = True
                else:
                    for cafe in cafes:
                        if cafe.rating >= float(rating_filter):
                                respond(f"{cafe.name} which has a {cafe.rating} star rating")
                                if cafe.keywords:
                                    respond(f"People are saying: {', '.join(cafe.keywords)} about their matcha lattes")
                                contains_cafe = True

            else:
                for cafe in cafes:
                    for key in user_keywords:            
                        if key in cafe.keywords and cafe.rating >= float(rating_filter):
                            if cafe.name not in cafe_list:
                                cafe_list.append(cafe.name)
                                contains_cafe = True
                
                if cafes > 5:    
                    for cafe in cafes[:5]:
                        if cafe.rating >= float(rating_filter):
                                respond(f"{cafe.name} which has a {cafe.rating} star rating")
                                if cafe.keywords:
                                    respond(f"People are saying: {', '.join(cafe.keywords)} about their matcha lattes")
                                contains_cafe = True
                else:
                    for cafe in cafes:
                        if cafe.rating >= float(rating_filter):
                                respond(f"{cafe.name} which has a {cafe.rating} star rating")
                                if cafe.keywords:
                                    respond(f"People are saying: {', '.join(cafe.keywords)} about their matcha lattes")
                                contains_cafe = True

                if not contains_cafe:
                    rating_filter = all_ratings[len(all_ratings) - 2]
                    respond("No cafes match criteria.")

        elif answer == "three":
            user_keywords.clear()
            rating_filter = "1"
                
        elif answer == "quit":
            respond("Exiting program")

        else:
            respond("The answer you gave was not an option. Please say one of the options below:")
            correct_option = False

   








        
     
 
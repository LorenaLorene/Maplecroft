from django.http import HttpResponse
from django.template import loader
import twitter
import csv

# log in to Twitter account #
api = twitter.Api(consumer_key='ErJUtqBVUrc7eaaIgm0OFPHa9',
                  consumer_secret='3OsTaI7jrIosvyFRbili0syJotqxpepcGHTmANc7iO2GOwHNK5',
                  access_token_key='1043086627877400576-D3O22zPfvxrwcKTVCFbSiXkszfK4WZ',
                  access_token_secret='OigsrI6xcfQ3F3JBkg9PeMbH9n4BLJf48nw8Axx54HlyQ')

# getting Maplecroft tweets #
statuses = api.GetUserTimeline(screen_name='MaplecroftRisk')

# opening csv file and getting a list #
with open('interview_test/countries.csv') as csv_file:
    data = list(csv.reader(csv_file))

# creating an object to contain country name and related tweets #
class Item:
    # constructor with country name and list of tweets #
    def __init__(self, name):
        self.country_name = name
        self.tweets = []

    # function to add tweets to list #
    def add_tweet(self, tweet):
        self.tweets.append(tweet)

# function which checks if country name exists in tweet text and returns object/class with country name with a related tweets #
def get_tweets_by_country_name(country_name):
    i = Item(country_name)
    for status in statuses:
        if country_name in status.text:
            i.add_tweet(status)

    return i

def index(request):
    template = loader.get_template('index.html') # uploads template #

    my_list_with_countries_and_tweets = [] # shows empty list #

    # for each country in CSV file
    for country in data:
        my_list_with_countries_and_tweets.append(get_tweets_by_country_name(country[0])) # add Item

    context = {'my_list_with_countries_and_tweets': my_list_with_countries_and_tweets}

    return HttpResponse(template.render(context, request))

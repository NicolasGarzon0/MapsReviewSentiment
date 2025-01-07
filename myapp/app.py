import os
import schedule
import pandas as pd
import matplotlib.pyplot as plt
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from dotenv import load_dotenv
from serpapi import GoogleSearch
from datetime import datetime

#get API key
load_dotenv()
Apikey = os.getenv("SerpAPI_APIKEY")
if not Apikey:
    raise ValueError("APIKEY Not Found In Environment Variables.")

sentiment = SentimentIntensityAnalyzer()
processed_data = {"Review Date": [], "Review Rate": [], "Review Snippet": [], "Review Sentiment Score": []}
current_date_formatted = datetime.now().strftime("%Y-%m-%d")

#get reviews of a place given its data id
def get_reviews(data_id):
    params = {
    "api_key": Apikey,
    "engine": "google_maps_reviews",
    "data_id": data_id,
    "hl": "en",
    "sort_by": "newestFirst"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results

#get data id of a place  given its name
def get_place_id(Name):
        params = {
        "api_key": Apikey,
        "engine": "google_maps",
        "type": "search",
        "google_domain": "google.com",
        "q": Name,
        "ll": "@40.7455096, -74.0083012,3z",
        "hl": "en",
        "start": "0"
        }

        search = GoogleSearch(params)
        results = search.get_dict()
        try:
            if "place_results" in results and "data_id" in results["place_results"]:
                return results["place_results"]["data_id"]
            elif "places" in results and results["places"] and "data_id" in results["places"][0]: 
                return results["places"][0]["data_id"]
            elif "local_results" in results and results["local_results"] and "data_id" in results["local_results"][0]: 
                return results["local_results"][0]["data_id"]
            else:
                print("Warning: data_id not found in any expected location.")
                return None  

        except (TypeError, IndexError, KeyError) as e:  
            print(f"Error extracting data_id: {e}")
            return None 

#procceses data from the API call
def process_data(data):
    for x in range(0, 8):

        review = data["reviews"][x]
        snippet = review.get('snippet')
        extracted_snippet = review.get('extracted_snippet', {})
        translation = extracted_snippet.get('translated')

        if snippet and translation:
            processed_data["Review Date"].append(review['iso_date_of_last_edit'].split("T")[0])
            processed_data["Review Rate"].append(review['rating'])
            processed_data["Review Snippet"].append(translation)
            processed_data["Review Sentiment Score"].append((sentiment.polarity_scores(translation))['compound'])
        elif snippet and not translation:
            processed_data["Review Date"].append(review['iso_date_of_last_edit'].split("T")[0])
            processed_data["Review Rate"].append(review['rating'])
            processed_data["Review Snippet"].append(snippet)
            processed_data["Review Sentiment Score"].append((sentiment.polarity_scores(snippet))['compound'])

#create dataframe with proccessed data and save it as CVS
def get_processed_dataframe():
    dataframe = pd.DataFrame(processed_data).drop_duplicates().sort_values(by="Review Date",ascending=True).reset_index(drop=True)
    dataframe.to_csv(f'Processed Dataframe {current_date_formatted}.csv')
    return dataframe

#create plot of the dataframe and save it as PNG
def get_plot_dataframe():
    df = get_processed_dataframe()
    df['Review Date'] = pd.to_datetime(df['Review Date']) 
    df_aggregated = df.groupby('Review Date')['Review Sentiment Score'].mean().reset_index()
    df_aggregated.plot(x='Review Date', y='Review Sentiment Score', kind="line", legend=False)
    plt.xlabel("Reviews Date")  
    plt.ylabel("Reviews Sentiment Score")
    plt.title("Sentiment Score Of Reviews Over Time")  
    plt.savefig(f'Sentiment Score Of Reviews Over Time {current_date_formatted}.png')

#actualize data
def actualize_data():
    data = get_reviews(data_id)
    process_data(data)
    print("Data Updated Successfully")

#download dataframe as csv and plot as png    
def get_formatted_data():
    get_processed_dataframe()
    get_plot_dataframe()
    print("Files Downloaded Successfully")

#main loop
if __name__ == "__main__":
    while True:
        try:
            place_name = input("Enter the name of the place: ")
            data_id = get_place_id(place_name)

            if data_id:
                actualize_data()
                print("Program Running Correctly")
            else:
                print("Error: Place ID not found. Please try again.")
                continue

            schedule.every().day.at("00:00").do(actualize_data)
            schedule.every().sunday.at("00:00").do(get_formatted_data)

            while True:
                schedule.run_pending()
                time.sleep(1)

        except KeyboardInterrupt:
            print("Exiting program.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}. The program will restart.")
            continue

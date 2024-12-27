
# MapsReviewSentiment: Analyzing and Visualizing Google Maps Reviews Sentiment

**MapsReviewSentiment** is a Python-based console application that extracts Google Maps reviews using the SerpAPI API and updates the review dataset daily. Each week, the app generates a CSV file containing the review date, rating, text, and sentiment score, along with a PNG line graph showing sentiment scores over time. Sentiment analysis is performed using the VADER model.



## Example CSV
![MapsReviewSentiment](Images/Image%201.jpg)

## Example Graph
![MapsReviewSentiment](Images/Image%202.jpg)

## Getting An API Key

- **Sign Up for SerpAPI**: Go to [this link](https://serpapi.com/users/sign_up) and sign up.
- **Obtain Your API Key**: After signing up, you'll receive an API key. Copy it to the `.env` file in your project.
## Running The App

1. Clone the `myapp` folder from the repository:
    ```bash
    git clone https://github.com/NicolasGarzon0/MapsReviewSentiment.git
    ```

2. Navigate into the `myapp` directory:
    ```bash
    cd MapsReviewSentiment/myapp
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Open the `.env` file in the `myapp` directory and add your API key:
    ```bash
    SerpAPI_APIKEY = your_api_key
    ```

5. Run the application:
    ```bash
    python app.py
    ```

6. Insert in the console the name of the place you want to get the reviews from.
## Technologies Used


Python, Pandas, Matplotlib, SerpAPI API, VADER Sentiment Analysis Model



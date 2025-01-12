import tweepy
import streamlit as st

# Configuración de la API de Twitter
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAFv9xwEAAAAAjmtuMw4oMe94EABKhDjyWVEV9q0%3DrWD6zncYiEKagBcIq2ZEEuNZ3I3t39xkjDe2fNorsiAI4khqc8"
API_KEY = "QC5f8TGVqpssEtiMAjdhOFvYR"
API_SECRET = "LUYCyRyNQR7yetxBvdBuCCZVVhOyOvfyUWgRudiWK0VxpGwELV"
ACCESS_TOKEN = "1876690727628902400-2ys0MXSryXfhK4OqkD3ptWvGQL3LXO"
ACCESS_TOKEN_SECRET = "ilqbHvcI0cd3njKvqML1L9ec71ueOGWXg36bGM7pUiebK"

try:
    client = tweepy.Client(
        bearer_token=BEARER_TOKEN,
        consumer_key=API_KEY,
        consumer_secret=API_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET
    )
except tweepy.errors.Unauthorized:
    st.error("Error de autenticación en Twitter. Verifica tus credenciales.")
    client = None 


def publish_on_twitter_v2(texto):
    try:
        if len(texto) > 280:
            texto = texto[:277] + "..." 

        response = client.create_tweet(text=texto)
        tweet_id = response.data["id"]
        return f"¡Publicado en X con éxito! [Ver Tweet](https://twitter.com/user/status/{tweet_id})"
    except Exception as e:
        return f"Error al publicar en Twitter: {str(e)}"
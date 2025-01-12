import os
from dotenv import load_dotenv
import tweepy
import streamlit as st

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

API_KEY  = str(os.getenv("TWITTER_API_KEY") or "") 
API_SECRET = str(os.getenv("TWITTER_API_SECRET") or "")
ACCESS_TOKEN = str(os.getenv("TWITTER_ACCESS_TOKEN") or "")
ACCESS_TOKEN_SECRET = str(os.getenv("TWITTER_ACCESS_TOKEN_SECRET") or "")
BEARER_TOKEN = str(os.getenv("TWITTER_BEARER_TOKEN") or "")

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
    client = None # Para evitar errores posteriores


def publish_on_twitter_v2(texto):
    try:
        if len(texto) > 280:
            texto = texto[:277] + "..." 

        response = client.create_tweet(text=texto)
        tweet_id = response.data["id"]
        return f"¡Publicado en X con éxito! [Ver Tweet](https://twitter.com/user/status/{tweet_id})"
    except Exception as e:
        return f"Error al publicar en Twitter: {str(e)}"
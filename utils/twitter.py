import os
from dotenv import load_dotenv
import tweepy
import streamlit as st

# Carga las variables del archivo .env
load_dotenv()

# Accede a las variables de entorno
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", None)  # Token opcional

try:
  if TWITTER_BEARER_TOKEN:
    client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
  else:
    client = tweepy.Client(
        consumer_key=TWITTER_API_KEY,
        consumer_secret=TWITTER_API_SECRET,
        access_token=TWITTER_ACCESS_TOKEN,
        access_token_secret=TWITTER_ACCESS_TOKEN_SECRET
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
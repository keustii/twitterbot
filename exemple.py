import requests
from requests_oauthlib import OAuth1
import os
import tweepy
import time

# Configuration des clés et tokens
bearer_token = ''
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''
# Authentification OAuth1
auth = OAuth1(consumer_key, consumer_secret, access_token, access_token_secret)

# Authentification OAuth1


# Configuration du client Tweepy avec authentification complète
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

def poste_photo(text, chemin_photo):
    url_upload = "https://upload.twitter.com/1.1/media/upload.json"
    try:
        with open(chemin_photo, 'rb') as file:
            files = {'media': file}
            response = requests.post(url_upload, auth=auth, files=files)
        if response.status_code == 200:
            media_id = response.json()['media_id_string']
            tweet = client.create_tweet(text=text, media_ids=[media_id])
            print("Tweet avec photo posté avec succès!")
        else:
            print("Échec du téléchargement du média:", response.status_code, response.text)
    except Exception as e:
        print("Erreur lors de la publication de la photo:", e)


# Fonction pour poster une vidéo
def poste_video(texte, chemin_video):
    url_init = "https://upload.twitter.com/1.1/media/upload.json"
    params_init = {
        'command': 'INIT',
        'total_bytes': str(os.path.getsize(chemin_video)),
        'media_type': 'video/mp4',
        'media_category': 'tweet_video'
    }
    response_init = requests.post(url_init, auth=auth, data=params_init)

    if response_init.status_code == 202:
        media_id = response_init.json().get('media_id_string')
        print("Initialisation réussie, media_id:", media_id)

        url_append = "https://upload.twitter.com/1.1/media/upload.json"
        with open(chemin_video, 'rb') as f:
            segment_id = 0
            while True:
                chunk = f.read(4 * 1024 * 1024)  # Lecture de 4 Mo à la fois
                if not chunk:
                    break
                params_append = {
                    'command': 'APPEND',
                    'media_id': media_id,
                    'segment_index': segment_id
                }
                files = {'media': chunk}
                response_append = requests.post(url_append, auth=auth, data=params_append, files=files)
                if response_append.status_code == 204:
                    print("Segment", segment_id, "ajouté avec succès")
                else:
                    print("Erreur lors de l'ajout du segment", segment_id, ":", response_append.status_code,
                          response_append.text)
                    exit()  # Arrête le script si l'ajout échoue
                segment_id += 1

        url_finalize = "https://upload.twitter.com/1.1/media/upload.json"
        params_finalize = {
            'command': 'FINALIZE',
            'media_id': media_id
        }
        response_finalize = requests.post(url_finalize, auth=auth, data=params_finalize)

        if response_finalize.status_code == 200:
            print("Finalisation réussie, media_id:", media_id)
            processing_info = response_finalize.json().get('processing_info', {})
            while processing_info.get('state') not in ['succeeded', 'failed']:
                print(f"Média en cours de traitement, état: {processing_info['state']} avec {processing_info.get('progress_percent', 0)}% complété")
                check_after_secs = processing_info.get('check_after_secs', 5)
                print(f"Vérification après {check_after_secs} secondes...")
                time.sleep(check_after_secs)
                url_status = f"https://upload.twitter.com/1.1/media/upload.json?command=STATUS&media_id={media_id}"
                response_status = requests.get(url_status, auth=auth)
                processing_info = response_status.json().get('processing_info', {})
                print(response_status.text)
            if processing_info.get('state') == 'succeeded':
                print("Traitement du média terminé, état:", processing_info['state'])
                try:
                    tweet = client.create_tweet(text=texte, media_ids=[media_id])
                    print("Tweet posté avec succès!")
                except tweepy.TweepyException as e:
                    print("Erreur lors de la publication du tweet :", e)
            else:
                print("Le traitement du média a échoué :", processing_info)
        else:
            print("Échec de la finalisation:", response_finalize.status_code, response_finalize.text)

    else:
        print("Échec de l'initialisation:", response_init.status_code, response_init.text)



# Exemple d'utilisation
poste_photo("Bonjour Twitter avec photo!", "image.jpg")
time.sleep(5)
poste_video("Bonjour Twitter avec vidéo!", "video.mp4")
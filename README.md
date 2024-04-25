# Twitter Poster 🐦📸🎥

## Description
Ce script Python vous permet de télécharger et de poster des photos et des vidéos sur Twitter en utilisant l'API Twitter.

## Configuration 🔑
Avant d'utiliser ce script, assurez-vous d'avoir les clés et les tokens nécessaires de l'API Twitter. Vous pouvez obtenir ces clés en créant une application Twitter sur le [site des développeurs Twitter](https://developer.twitter.com/en/apps).

## Installation 💻
1. Cloner ce dépôt sur votre machine locale :
    ```
    git clone https://github.com/votre_utilisateur/twitter-poster.git
    ```
2. Installer les dépendances en utilisant pip :
    ```
    pip install -r requirements.txt
    ```

## Utilisation 🚀
1. Assurez-vous d'avoir les clés et les tokens de votre application Twitter.
2. Importez le module `TwitterPoster` dans votre script Python.
3. Créez un objet `TwitterPoster` en passant vos clés et tokens en paramètres.
4. Utilisez les méthodes `poste_photo` et `poste_video` pour télécharger et poster des photos et des vidéos sur Twitter.

Exemple d'utilisation :
```python
from TwitterPoster import TwitterPoster

# Créez un objet TwitterPoster avec vos clés et tokens
poster = TwitterPoster(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

# Postez une photo sur Twitter
poster.poste_photo("Ceci est une photo !", "chemin/vers/ma/photo.jpg")

# Postez une vidéo sur Twitter
poster.poste_video("Ceci est une vidéo !", "chemin/vers/ma/vidéo.mp4")

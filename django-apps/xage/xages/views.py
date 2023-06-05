from django.shortcuts import render
from PIL import Image
import numpy as np
import tensorflow as tf

from .models import Utilisateur

def get_sexe_label(prediction):
    if prediction == 0:
        return "féminin"
    else:
        return "masculin"

def index(request):
    content = {'a': 'hello'}
    return render(request, 'prediction.html', content)


# Chemin vers le fichier .h5 du modèle entraîné
chemin_modele = 'modele.h5'

# Charger le modèle à partir du fichier .h5modele = tf.keras.models.load_model(chemin_modele)

def prediction(request):
    content = {'a': 'hello'}
    return render(request, 'index.html', content)

def prediction0(request):
    if request.method == 'POST':
        if 'photo' not in request.FILES:
            return render(request, 'prediction.html')

        # Récupérer la photo téléchargée par l'utilisateur
        photo = request.FILES['photo']

        # Prétraiter la photo si nécessaire (redimensionnement, normalisation, etc.)
        img = Image.open(photo)
        img = img.resize((224, 224))  # Redimensionner l'image à la taille attendue par le modèle
        img = np.array(img)  # Convertir l'image en tableau NumPy
        img = img / 255.0  # Normaliser les valeurs des pixels entre 0 et 1
        img = np.expand_dims(img, axis=0)  # Ajouter une dimension pour représenter le batch

        # Effectuer la prédiction de l'âge et du sexe en utilisant le modèle
        # Assumons que `modele` est chargé et prêt à effectuer des prédictions
        resultat_prediction = modele.predict(img)

        # Supposons que le résultat de la prédiction est un dictionnaire
        age = resultat_prediction['age']
        sexe = get_sexe_label(resultat_prediction['sexe'])

        # Enregistrer les informations dans la base de données
        utilisateur = Utilisateur(photo=photo, age=age, sexe=sexe)
        utilisateur.save()

        # Renvoyer les résultats de la prédiction à l'interface utilisateur
        return render(request, 'result.html', {'age': age, 'sexe': sexe})
    else:
        return render(request, 'prediction.html')

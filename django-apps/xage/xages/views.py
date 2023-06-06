from django.shortcuts import render
from PIL import Image
import numpy as np
import pickle

from .models import Utilisateur

def get_sexe_label(prediction):
    if prediction == 0:
        return "féminin"
    else:
        return "masculin"

def index(request):
    content = {'a': 'hello'}
    return render(request, 'prediction.html', content)

def prediction(request):
    content = {'a': 'hello'}
    return render(request, 'index.html', content)

def prediction0(request):
    if request.method == 'POST':
        if 'photo' not in request.FILES:
            return render(request, 'prediction.html')

        # Load the saved Random Forest model
        with open('model.pkl', 'rb') as file:
            model = pickle.load(file)

        # Récupérer la photo téléchargée par l'utilisateur
        photo = request.FILES['photo']

        # Prétraiter la photo si nécessaire (redimensionnement, normalisation, etc.)
        img = Image.open(photo)
        img = img.resize((224, 224))  # Redimensionner l'image à la taille attendue par le modèle
        img = np.array(img)  # Convertir l'image en tableau NumPy
        img = img / 255.0  # Normaliser les valeurs des pixels entre 0 et 1
        img = np.expand_dims(img, axis=0)  # Ajouter une dimension pour représenter le batch

        # Effectuer la prédiction en utilisant le modèle
        resultat_prediction = model.predict(img)

        # Supposons que le résultat de la prédiction est un entier pour le sexe (0 ou 1)
        sexe = get_sexe_label(resultat_prediction)

        # Enregistrer les informations dans la base de données
        utilisateur = Utilisateur(photo=photo, sexe=sexe)
        utilisateur.save()

        # Renvoyer les résultats de la prédiction à l'interface utilisateur
        return render(request, 'result.html', {'sexe': sexe})
    else:
        return render(request, 'prediction.html')

from django.shortcuts import render
from PIL import Image
import numpy as np
import joblib
import os

from .models import Utilisateur

def get_sexe_label(prediction):
    if prediction == 1:
        return "féminin"
    else:
        return "masculin"

def index(request):
    content = {'a': 'hello'}
    return render(request, 'prediction.html', content)

def prediction(request):
    if request.method == 'POST':
        if 'photo' not in request.FILES:
            return render(request, 'prediction.html')

        # Obtenez le chemin absolu du fichier model.pkl dans le même dossier que views.py
        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'model.pkl')

        # Chargez le modèle MultiOutputClassifier à partir du fichier model.pkl
        model = joblib.load(model_path)

        # Récupérer la photo téléchargée par l'utilisateur
        photo = request.FILES['photo']

        # Prétraiter la photo si nécessaire (redimensionnement, normalisation, etc.)
        img = Image.open(photo)
        img = img.resize((224, 224))  # Redimensionner l'image à la taille attendue par le modèle
        img = np.array(img)  # Convertir l'image en tableau NumPy
        img = img / 255.0  # Normaliser les valeurs des pixels entre 0 et 1
        img = img.flatten()  # Aplatir l'image en un vecteur 1D
        img = np.expand_dims(img, axis=0)  # Ajouter une dimension pour représenter le batch

        # Effectuer la prédiction en utilisant le modèle
        resultat_prediction = model.predict(img)

        # Supposons que le résultat de la prédiction est un tableau [[age, sexe]]
        age = resultat_prediction[0][0]
        sexe = get_sexe_label(resultat_prediction[0][1])

        # Enregistrer les informations dans la base de données
        #utilisateur = Utilisateur(photo=photo, age=age, sexe=sexe)
        #utilisateur.save()

        # Renvoyer les résultats de la prédiction à l'interface utilisateur
        return render(request, 'prediction.html', {'age': age, 'sexe': sexe})
    else:
        return render(request, 'prediction.html')
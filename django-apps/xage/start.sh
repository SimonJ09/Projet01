#!/bin/bash

pip install --upgrade typing-extensions

# Activation de l'environnement virtuel (si applicable)
source django-apps/env/bin/activate

# Lancement de Gunicorn avec votre application Django
gunicorn xage.wsgi:application --bind 0.0.0.0:$PORT --workers 4

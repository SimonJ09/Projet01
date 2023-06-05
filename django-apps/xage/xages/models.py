from django.db import models

class Utilisateur(models.Model):
    photo = models.ImageField(upload_to='photos')
    age = models.IntegerField()
    sexe = models.CharField(max_length=10)

    def __str__(self):
        return f"Utilisateur {self.id}"

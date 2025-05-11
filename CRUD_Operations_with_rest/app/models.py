from django.db import models

# Create your models here.
class Database(models.Model):
    Name=models.CharField(max_length=5000)
    Gender=models.CharField(choices={"M": "M", "F" :"F"}, max_length=5)
    Mobile=models.IntegerField()
    Address=models.CharField(max_length=500000)


    def __str__(self):
        return f"{self.Name}, {self.Gender}, {self.Mobile}, {self.Address}"
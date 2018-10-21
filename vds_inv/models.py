from django.db import models
import json


# {mustbe (дожно быть штук), count (количество штук), arrive(заказно у поставщика штуки)}
class Spare(models.Model):
    name = models.CharField(max_length=400)
    mustbe = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    arrive = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Alternative(models.Model):
    name = models.CharField(max_length=400)
    alternatives = models.CharField(max_length=1000)

    def __str__(self):
        return self.name

    def set_alternatives(self, alt):
        self.alternatives = json.dumps(alt)

    def get_alternatives(self):
        return json.loads(self.alternatives)
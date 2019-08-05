from django.db import models

class File(models.Model):
    title = models.FileField(upload_to="model")
    illumination = models.FloatField(default=1)
    h = models.FloatField(default=-10)
    h2o = models.FloatField(default=-10)
    pi = models.FloatField(default=-10)
    nh4 = models.FloatField(default=-10)
    no3 = models.FloatField(default=-10)
    so4 = models.FloatField(default=-10)
    o2 = models.FloatField(default=-10)
    ac = models.FloatField(default=0)
    hash_str = models.TextField(null=True)
    filetxt = models.TextField(null=True)

    objects = models.Manager()


    def __str__(self):
        return self.hash_str

class Cycle(models.Model):
    title = models.FileField(upload_to="cycle")
    hash_str = models.TextField(null=True)

    objects = models.Manager()

    def __str__(self):
        return self.hash_str

class Reactions(models.Model):
    cycle = models.TextField(null=True)
    value = models.TextField(null=True)
    objects = models.Manager()

    def __str__(self):
        return self.cycle


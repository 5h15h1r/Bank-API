from django.db import models


class Banks(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=49)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'banks'


class Branch(models.Model):
    ifsc = models.CharField(max_length=11, primary_key=True, db_index=True)
    bank = models.ForeignKey(Banks, on_delete=models.CASCADE)
    branch = models.CharField(max_length=74, db_index=True)
    address = models.CharField(max_length=195)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=26)

    def __str__(self):
        return self.branch

    class Meta:
        db_table = 'branches'

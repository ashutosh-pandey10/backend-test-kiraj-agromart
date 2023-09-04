from django.db import models

class Candle(models.Model):
    id = models.AutoField(primary_key=True)
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()


class ConvertedCandle(models.Model):
    candle = models.OneToOneField(Candle, on_delete=models.CASCADE, primary_key=True)
    timeframe = models.PositiveIntegerField()


from django.db import models
from django.contrib.auth.models import User


class BMPImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    image = models.ImageField()
    text = models.TextField(default='')
    res_image = models.ImageField(null=True, blank=True)
    build_type = models.CharField(max_length=50, choices=[
        ('type1', 'Type 1'),
        ('type2', 'Type 2'),
        ('type3', 'Type 3')
    ], default='type1')
    color_combination = models.CharField(max_length=50, choices=[
        ('combination1', 'Combination 1'),
        ('combination2', 'Combination 2'),
        ('combination3', 'Combination 3')
    ], default='combination1')

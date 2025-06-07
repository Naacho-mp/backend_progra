from django.db import models
from django_resized import ResizedImageField

class Categoria(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f'{self.id} - {self.nombre}'

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(default="Sin descripción")
    precio = models.IntegerField()
    stock = models.IntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    imagen = ResizedImageField(size=[500, 300], upload_to='mostrar_productos/', null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.nombre}'
from django.contrib import admin
from .models import Animal, Categoria, EstadoProducto

# Registrando los modelos de Animal y Categoria para que sean
# administrados.

admin.site.register(Animal)
admin.site.register(Categoria)
admin.site.register(EstadoProducto)

from django import forms
from .models import Producto


class ProductoForm(forms.ModelForm):
    """
    Formulario para facilitar la creación y edición de productos.
    """

    class Meta: 
        #Espeficiar a que modelo está asociado el formulario
        model = Producto

        fields = [
            'ref_categoria',
            'ref_estado',
            'nombre',
            'descripcion',
            'caracteristicas',
            'precio',
            'imagen'
        ]

        labels = {
            'ref_categoria':'Categoria',
            'ref_estado':'Estado',
            'nombre':'Nombre',
            'descripcion':'Descripción',
            'caracteristicas':'Caracteristicas',
            'precio':'Precio',
            'imagen':'Imagen'
        }

        widgets = {
            'ref_categoria':forms.Select(attrs={'class':'form-control'}),
            'ref_estado':forms.Select(attrs={'class':'form-control'}),
            'nombre':forms.TextInput(attrs={'class':'form-control'}),
            'descripcion':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'caracteristicas':forms.Textarea(attrs={'class':'form-control','rows':3}),
            'precio':forms.NumberInput(attrs={'class':'form-control'}),
            'imagen':forms.FileInput(attrs={'class':'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].error_messages = {'required': 'custom required message'}

        # if you want to do it to all of them
        for field in self.fields.values():
            field.error_messages = {'required':'El campo {fieldname} es obligatorio'.format(
                fieldname=field.label)}
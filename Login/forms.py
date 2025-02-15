from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from Cloraciones.models import Trabajador


class formularioRegistro(UserCreationForm):
    email = forms.EmailField(label = "", widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Dirección de correo electrónico'}))
    
    class Meta:
        model = User
        fields = ('username', 'email','password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(formularioRegistro, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Nombre de Usuario'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Obligatorio. 150 caracteres o menos. Sólo letras, dígitos y @/./+/-/_.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Su contraseña no puede ser demasiado parecida a tus otros datos personales.</li><li>Su contraseña debe contener al menos 8 caracteres.</li><li>Su contraseña no puede ser una contraseña de uso común.</li><li>Su contraseña no puede ser totalmente numérica.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmar Contraseña'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Introduzca la misma contraseña que antes, para la verificación.</small></span>'

        if 'usable_password' in self.fields:
            del self.fields['usable_password']

class TrabajadorForm(forms.ModelForm):
    naci = forms.DateInput

    class Meta:
        model = Trabajador
        fields = ('nom_tra', 'app_tra', 'apm_tra', 'nac_tra', 'rut_tra')
        widgets = {
            'nac_tra': forms.DateInput(format='%Y-%m-%d',attrs = { 'type': 'date', 'class': 'input-group-field', })
        }

    def __init__(self, *args, **kwargs):
        super(TrabajadorForm, self).__init__(*args, **kwargs)

        self.fields['nom_tra'].widget.attrs['class'] = 'form-control'
        self.fields['nom_tra'].label = ''
        self.fields['nom_tra'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Nombre del Trabajador'})

        self.fields['app_tra'].widget.attrs['class'] = 'form-control'
        self.fields['app_tra'].label = ''
        self.fields['app_tra'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Apellido Paterno'})

        self.fields['apm_tra'].widget.attrs['class'] = 'form-control'
        self.fields['apm_tra'].label = ''
        self.fields['apm_tra'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Apellido Materno'})

        self.fields['nac_tra'].widget.attrs['class'] = 'form-control'
        self.fields['nac_tra'].label = 'Fecha de nacimiento'
        # self.fields['nac_tra'].widget = forms.DateField()

        self.fields['rut_tra'].widget.attrs['class'] = 'form-control'
        self.fields['rut_tra'].label = ''
        self.fields['rut_tra'].widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Ingrese su RUT, sin puntos, ni guión'})


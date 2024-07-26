from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from .models import Usuario, Cuenta, Registros,Movimiento,Actividad,Subactividad
from .models import Formapago


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		if username and password:
			self.user = authenticate(username=username,password=password)
			if self.user is None:
				raise forms.ValidationError('Usuario o password incorrectos')
		return self.cleaned_data

	def get_user(self):
		return self.user

class RegistroForm(forms.ModelForm):
	password = forms.CharField(label='Password',widget=forms.PasswordInput)

	class Meta:
		model = Usuario
		fields = ['nombre','apellido','username','password']

	def save(self,commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password'])
		if commit:
			user.save()
		return user

class CuentaForm(forms.ModelForm):
	class Meta:
		model = Cuenta
		fields = ['nombre_cuenta','balance']	

class TransaccionForm(forms.ModelForm):
	"""Instancia de un formulario para registrar las transacciones"""
	class Meta:	
		model = Registros
		fields = [
				'id_cuenta',
				'id_movimiento',
				'id_actividad',
				'id_subactividad',
				'importe',
				'id_formapago',
				'fecha',
				'hora',
				'beneficiario',
				'nota',
				]

		labels = {
			'id_actividad':'Actividad',
			'id_subactividad':'Subactividad',
			'id_movimiento':'Tipo de movimiento',
			'id_formapago':'Forma de pago',
			'id_cuenta':'Cuenta',
		}
		widget = {
			# 'fecha': forms.DateField(required=True,widget=forms.DateInput(format='%Y-%m-%d',
			# 			attrs={'type':'date'}),
			# 			input_formats=['%Y-%m-%d'])
			'fecha': forms.DateInput(format='%Y-%m-%d',attrs={'type':'date'})
		}

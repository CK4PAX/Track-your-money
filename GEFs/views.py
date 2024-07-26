from django.shortcuts import render,redirect
from .models import Cuenta, Registros, Usuario, Formapago
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistroForm, CuentaForm, TransaccionForm

# Create your views here.

# def filtro_cuenta(request):
# 	'''Filtra los registros en base a una cuenta seleccionada'''
# 	cuenta = request.POST
# 	cuenta_seleccionada = cuenta['cuenta']
	


def cuenta_registro(request,id_cuenta):
	'''Renderiza los registros realizados por cada cuenta'''
	registros = Registros.objects.select_related('id_actividad','id_subactividad'
		).filter(id_cuenta=id_cuenta)
	return render(request,'GEFs/registros.html',{'registros':registros})

def eliminar_registro(request,id_registro):
	Registros.objects.get(pk=id_registro).delete()
	return redirect('GEFs:registros')

def eliminar_cuenta(request,id_cuenta):
	Cuenta.objects.get(pk=id_cuenta).delete()
	return redirect('GEFs:cuentas')

@login_required
def modificar_cuenta(request,id_cuenta):
	'''Actualizar el nombre y/o el balance de cada cuenta'''
	cuenta = Cuenta.objects.get(id_cuenta=id_cuenta)
	if request.method != 'POST':
		form = CuentaForm()
	else:
		form = CuentaForm(request.POST)
		if form.is_valid:
			cuenta_modificada = form.save(commit=False)
			cuenta_modificada.id_cuenta = id_cuenta
			cuenta_modificada.id_usuario = request.user 
			cuenta_modificada.save()
			return redirect('GEFs:cuentas')

	context = {
		'form':form,
		'cuenta':cuenta,
	}
	return render(request,'GEFs/mcuenta.html',context)

def nuevo_registro(request):
	'''Inserta registros en una cuenta particular a travez de formulario 
		TransaccionForm'''
	usuario = request.user	
	if request.method != 'POST':
		form = TransaccionForm()
		form.fields['id_cuenta'].choices = [(value.id_cuenta,value.nombre_cuenta) for value in usuario.cuenta_set.all()]
	else:
		form = TransaccionForm(request.POST)
		if form.is_valid:
			transaccion = form.save(commit=False)
			transaccion.id_usuario = usuario
			#Modificamos el balance de la cuenta en base al monto de la transaccion
			if transaccion.id_movimiento.tipo_movimiento in ['Gasto','Transferencia']:
				#Almacenamos la cuenta desde su atributo id_cuenta
				cuenta = transaccion.id_cuenta
				#Si es gasto o transferencia disminuimos el saldo
				cuenta.balance -= transaccion.importe
				cuenta.save()
			else:
				cuenta = transaccion.id_cuenta
				cuenta.balance += transaccion.importe
				cuenta.save()
			transaccion.save()
			return redirect('GEFs:registros')

	return render(request,'GEFs/nuevo_registro.html',{'form':form})			

@login_required
def nueva_cuenta(request,id_usuario):
	'''Ingresa una nueva cuenta para un usuario en particular'''
	usuario = Usuario.objects.get(id_usuario=id_usuario)

	if request.method != 'POST':
		form = CuentaForm()
	else:
		form = CuentaForm(request.POST)
		if form.is_valid:
			cuenta = form.save(commit=False)
			cuenta.id_usuario = usuario
			cuenta.save()
			return redirect('GEFs:cuentas')

	context = {
		'form':form,
		'usuario':usuario,
	}
	return render(request,'GEFs/nueva_cuenta.html',context)

def primera_cuenta(user):
	'''Se crea una cuenta por default "efectivo" para un nuevo usuario'''
	Cuenta.objects.create(nombre_cuenta='Efectivo',balance='0',id_usuario=user)

def user_register(request):
	if request.method == 'POST':
		form = RegistroForm(request.POST)
		if form.is_valid:
			user = form.save()
			login(request,user)
			primera_cuenta(user)
			return redirect('GEFs:cuentas')
	else:		
		form = RegistroForm()

	return render(request,'GEFs/user_register.html',{'form':form})

def mi_login(request):
	if request.method =='POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user = form.get_user()
			if user:
				login(request,user)
				return redirect('GEFs:cuentas')
	else:
		form = LoginForm()
	return render(request,'GEFs/login.html',{'form':form})

def mi_logout(request):
	logout(request)
	return redirect('GEFs:login')

@login_required
def cuentas(request):
	'''Muestra las cuentas que han sido creadas.'''
	cuentas = Cuenta.objects.filter(id_usuario=request.user)
	context = {
		'cuentas':cuentas
	}
	return render(request,'GEFs/cuentas.html',context)

@login_required
def registros(request):
	'''Muestra los registros que han sido creados.'''
	usuario = request.user.id_usuario
	cuentas = Cuenta.objects.filter(id_usuario=usuario)
	registros = Registros.objects.select_related('id_actividad',
			'id_subactividad').filter(id_usuario=usuario)
	context = {
		'registros': registros,
		'cuentas': cuentas,
	}
	return render(request,'GEFs/registros.html',context)

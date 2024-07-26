from django.urls import path
from . import views

app_name = 'GEFs'

urlpatterns = [
	#Pagina de inicio
	#path('usuario/<int:id_usuario>',views.usuario,name='usuario'),

	# path('filtro_cuenta/',views.filtro_cuenta,name='filtro_cuenta'),
	path('cuenta_registro/<int:id_cuenta>',views.cuenta_registro,name='cuenta_registro'),
	path('eliminar_registro/<int:id_registro>',views.eliminar_registro,name='eliminar_registro'),
	path('eliminar_cuenta/<int:id_cuenta>',views.eliminar_cuenta,name='eliminar_cuenta'),
	path('modificar_cuenta/<int:id_cuenta>',views.modificar_cuenta,name='modificar_cuenta'),
	path('nuevo_registro/',views.nuevo_registro,name='nuevo_registro'),
	path('nueva_cuenta/<int:id_usuario>',views.nueva_cuenta,name='nueva_cuenta'),
	path('cuentas/',views.cuentas,name='cuentas'),
	path('registros/',views.registros,name='registros'),
	path('login/',views.mi_login,name='login'),
	path('logout/',views.mi_logout,name='logout'),
	path('user_register/',views.user_register,name='user_register')
]
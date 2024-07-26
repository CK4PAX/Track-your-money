from django.contrib import admin

from .models import Usuario,Cuenta,Movimiento,Actividad,Subactividad,Formapago,Registros

admin.site.register(Usuario)
admin.site.register(Cuenta)
admin.site.register(Movimiento)
admin.site.register(Actividad)
admin.site.register(Subactividad)
admin.site.register(Formapago)
admin.site.register(Registros)

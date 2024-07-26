from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.

class MiUsuarioManager(BaseUserManager):
    def create_user(self,username,password=None,**extra_fields):
        if not username:
            raise ValueError('El usuario debe tener username')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self_db)
        return user

    def create_superuser(self,username,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        return self.create_user(username,password,**extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    password= models.CharField(max_length=128)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=35)

    class Meta:
        db_table = 'usuario'

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = MiUsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        '''Devuelve una representacion del modelo como cadena'''
        return self.username

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

class Cuenta(models.Model):
    id_cuenta = models.AutoField(primary_key=True)
    nombre_cuenta = models.CharField(max_length=15)
    balance = models.FloatField()
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)

    class Meta:
        db_table = 'cuenta'

    def __str__(self):  
        '''Devuelve una representacion del modelo como cadena'''
        return self.nombre_cuenta

class Movimiento(models.Model):
    id_movimiento = models.AutoField(primary_key=True)
    tipo_movimiento = models.CharField(max_length=20)

    class Meta:
        db_table = 'movimiento'

    def __str__(self):
        '''Devuelve una representacion del modelo como cadena'''
        return self.tipo_movimiento

class Actividad(models.Model):
    id_actividad = models.AutoField(primary_key=True)
    tipo_actividad = models.CharField(max_length=50)
    id_movimiento = models.ForeignKey('Movimiento', models.DO_NOTHING, db_column='id_movimiento')

    class Meta:
        db_table = 'actividad'
        verbose_name_plural = 'Actividades'

    def __str__(self):
        '''Devuelve una representacion del modelo como cadena'''
        return self.tipo_actividad

class Subactividad(models.Model):
    id_subactividad = models.AutoField(primary_key=True)
    tipo_subactividad = models.CharField(max_length=50, blank=True, null=True)
    id_actividad = models.ForeignKey(Actividad, models.DO_NOTHING, db_column='id_actividad')

    class Meta:
        db_table = 'subactividad'
        verbose_name_plural ='Subactividades'

    def __str__(self):
        '''Devuelve una representacion del modelo como cadena'''
        return self.tipo_subactividad
        
class Formapago(models.Model):
    id_formapago = models.AutoField(db_column='id_formaPago', primary_key=True)  # Field name made lowercase.
    tipo_pago = models.CharField(max_length=20)

    class Meta:
        db_table = 'formapago'
        verbose_name_plural='Formas de pago'

    def __str__(self):
        '''Devuelve una representacion del modelo como cadena'''
        return self.tipo_pago

class Registros(models.Model):
    id_registro = models.AutoField(primary_key=True)
    importe = models.FloatField()
    fecha = models.DateField()
    hora = models.TimeField()
    beneficiario = models.CharField(max_length=50, blank=True, null=True)
    nota = models.TextField(blank=True, null=True)
    id_movimiento = models.ForeignKey(Movimiento, models.DO_NOTHING, db_column='id_movimiento', blank=True, null=True)
    id_actividad = models.ForeignKey(Actividad, models.DO_NOTHING, db_column='id_actividad', blank=True, null=True)
    id_subactividad = models.ForeignKey('Subactividad', models.DO_NOTHING, db_column='id_subactividad', blank=True, null=True)
    id_formapago = models.ForeignKey(Formapago, models.DO_NOTHING, db_column='id_formaPago', blank=True, null=True)  # Field name made lowercase.
    id_cuenta = models.ForeignKey(Cuenta, db_column='id_cuenta', on_delete=models.CASCADE, blank=True, null=True)
    id_usuario = models.ForeignKey('Usuario', db_column='id_usuario', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'registros'
        verbose_name_plural ='Registros'

from django.contrib import admin
from .models import ConfiguracaoHora, CargoFuncionario, Funcionario, StatusPonto, Frequencia


@admin.register(ConfiguracaoHora)
class ConfiguracaoHoraAdmin(admin.ModelAdmin):
    pass


@admin.register(CargoFuncionario)
class CargoFuncionarioAdmin(admin.ModelAdmin):
    pass


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    pass


@admin.register(StatusPonto)
class StatusPontoAdmin(admin.ModelAdmin):
    pass


@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    pass
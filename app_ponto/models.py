from django.db import models
from django.contrib.auth.models import User
import socket

class ConfiguracaoHora(models.Model):
    descricao_conf_hora = models.CharField('Descrição da configuração da hora', max_length=128)
    conf_hora_entrada_1 = models.TimeField('Hora de entrada 1', blank=True, null=True)
    conf_hora_saida_1 = models.TimeField('Hora de saída 1', blank=True, null=True)
    conf_hora_entrada_2 = models.TimeField('Hora de entrada 2', blank=True, null=True)
    conf_hora_saida_2 = models.TimeField('Hora de saída 2', blank=True, null=True)

    def get_funcionario(self):
        return Funcionario.objects.filter(conf_hora=self)

    def __str__(self):
        return self.descricao_conf_hora


class CargoFuncionario(models.Model):
    descricao_cargo = models.CharField('Descriçaõ do cargo', max_length=128)

    def __str__(self):
        return self.descricao_cargo

class Funcionario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Usuário')
    lider = models.ForeignKey('Funcionario', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Lider')
    cargo = models.ForeignKey(CargoFuncionario, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Cargo do funcionário')
    conf_hora = models.ForeignKey(ConfiguracaoHora, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='COnfiguração da hora')
    nome = models.CharField('Nome do funcionário', max_length=128)

    def get_funcionario(self):
        return Funcionario.objects.filter(lider=self)

    def __str__(self):
        return self.nome

class StatusPonto(models.Model):
    descricao = models.CharField('Descrição', max_length=128)

    def __str__(self):
        return self.descricao


class TipoPonto(models.Model):
    descricao = models.CharField('Descrição', max_length=128)

    def __str__(self):
        return self.descricao


def pegar_ip():
    ip = socket.gethostbyname(socket.gethostname())
    return ip


class Frequencia(models.Model):
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Funcionário')
    hora_ponto = models.TimeField('Hora de entrada 1', blank=True, null=True)
    tipo_ponto = models.ForeignKey(TipoPonto, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Tipo ponto')
    data_resgistro = models.DateField('Data do registro', auto_now_add=True, blank=True, null=True)
    status_ponto = models.ForeignKey(StatusPonto, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Status ponto')
    ip_registro = models.CharField(max_length=20, default=pegar_ip(), editable=False, blank=True, null=True)
    juntificativa = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'Frequencia '+ str(self.funcionario) + ' '+ str(self.data_resgistro)
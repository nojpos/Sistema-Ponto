from django import forms
from .models import Frequencia


class FrequenciaForm(forms.ModelForm):

    class Meta:
        model = Frequencia
        fields = ('funcionario', 'hora_entrada_1', 'hora_saida_1', 'hora_entrada_2', 'hora_saida_2', 'status_ponto', 'juntificativa',)
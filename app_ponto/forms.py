from django import forms
from .models import Frequencia


class FrequenciaForm(forms.ModelForm):

    class Meta:
        model = Frequencia
        fields = ()


class JustificativaForm(forms.ModelForm):

    class Meta:
        model = Frequencia
        fields = ('juntificativa',)
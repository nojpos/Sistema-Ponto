from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Frequencia, Funcionario, ConfiguracaoHora
from .forms import FrequenciaForm


@login_required
def lista_frequencia(request):
    frequencia=Frequencia.objects.all()
    return render(request, 'app_ponto/frequencia.html', {'frequencia': frequencia})

@login_required
def teste_registro_ponto(request):
    user = request.user.id
    print(user)
    data_atual = datetime.now()
    print(data_atual.date())
    hora_atual = datetime.now()
    print(hora_atual.time())


    qtd = Frequencia.objects.filter(funcionario=user, data_resgistro=data_atual.date()).count()


    if qtd == 0:
        return HttpResponse('Quantidade = {}'.format(qtd))

    elif qtd == 1:
        return HttpResponse('Quantidade = {}'.format(qtd))

    elif qtd == 2:
        return HttpResponse('Quantidade = {}'.format(qtd))

    elif qtd == 3:
        return HttpResponse('Quantidade = {}'.format(qtd))


'''
class RegitrarForm(FormView):
    template_name = 'app_ponto/registrar.html'
    form_class = RegistroPontoForm

    def form_valid(self, form):
        hora_atual = datetime.now()
        print(hora_atual.time())
        dados = form.clean()
        s = Frequencia(juntificativa=dados['juntificativa'], )
        s.hora_entrada_2=hora_atual.time()
        s.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('frequencia')


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'app_ponto/name.html', {'form': form})


def funcionario_new(request):
    form = FuncionarioForm()

    if request.method == "POST":
        form = FuncionarioForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('frequencia')

    else:
        form = FuncionarioForm()

    return render(request, 'app_ponto/registro_ponto.html', {'form': form})
'''
@login_required
def registar_ponto(request):
    form = FrequenciaForm()

    user = request.user.id
    print('Usuário', user)

    hora_atual = datetime.now()
    print('Hora atual', hora_atual.time())

    data_atual = datetime.now()
    print('Data atual', data_atual.date())

    qtd = Frequencia.objects.filter(funcionario=user, data_resgistro=data_atual.date()).count()
    print('Quantidade', qtd)

    if request.method == "POST":
        form = FrequenciaForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)

            if qtd == 0:
                post.hora_entrada_1 = hora_atual.time()
                post.save()

            elif qtd == 1:
                post.hora_saida_1 = hora_atual.time()
                post.save()

            elif qtd == 2:
                post.hora_entrada_2 = hora_atual.time()
                post.save()

            elif qtd == 3:
                post.hora_saida_2 = hora_atual.time()
                post.save()

            return redirect('frequencia')

        else:
            form = FrequenciaForm()

    return render(request, 'app_ponto/registro_ponto.html', {'form': form})
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from empresas.models import Vagas
from django.contrib.messages import constants
from django.contrib import messages

# Create your views here.
def nova_vaga(request):
    if request.method  == "POST":
    
        titulo  =  request.POST.get('titulo')
        email = request.POST.get('email')
        tecnologias_domina = request.POST.getlist('tecnologias_domina')
        tecnologias_nao_domina = request.POST.getlist('tecnologias_nao_domina')
        experiencia  = request.POST.get('experiencia')
        data_final = request.POST.get('data_final')
        empresa = request.POST.get('empresa')
        status = request.POST.get('status')

        vagas = Vagas(
            titulo = titulo,
            email = email,
            nivel_experiencia = experiencia,
            data_final = data_final,
            empresa_id = empresa,
            status=status
        )

        vagas.save()
        vagas.tecnologias_etudar.add(*tecnologias_nao_domina)
        vagas.tecnologias_dominadas.add(*tecnologias_domina)
        vagas.save()

        messages.add_message(request, constants.SUCCESS, "Vaga criada com sucesso!")
        return redirect(f'/home/empresa/{empresa}')

    elif request.method == "GET":
        raise Http404

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from empresas.models import Vagas, Empresa
from .models import Tarefa, Emails
from django.contrib.messages import constants
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

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


def vaga(request, id):
    vaga = get_object_or_404(Vagas, id=id)
    tarefa = Tarefa.objects.filter(vaga=vaga).filter(realizada=False)
    email = Emails.objects.filter(vaga=vaga)
    return render(request, 'vaga.html', {'vaga' : vaga, 'tarefas': tarefa, 'emails' : email})

def nova_tarefa(request, id_vaga):

    titulo = request.POST.get('titulo')
    prioridade = request.POST.get('prioridade')
    data =  request.POST.get('data')

    #VALIDAÇÕES
    if len(titulo.strip()) == 0 or len(prioridade.strip()) == 0:
        messages.add_message(request, constants.ERROR,"Por favor preencha todos os campos!")
        return redirect(f'/vagas/vaga/{id_vaga}')

    elif prioridade not in [i[0] for i in Tarefa.choices_prioridade]:
        messages.add_message(request, constants.ERROR,"Escolha apenas entre as opções válidas!")
        return redirect(f'/vagas/vaga/{id_vaga}')

    try:
        tarefa = Tarefa(
                vaga_id = id_vaga,
                titulo = titulo, 
                prioridade = prioridade,
                data = data
        )

        tarefa.save()
        messages.add_message(request, constants.SUCCESS,"Tarefa adicionada com sucesso!")
        return redirect(f'/vagas/vaga/{id_vaga}')

    except RuntimeError:
        messages.add_message(request, constants.WARNING,"Erro interno, por favor tente nomavemnte mais tarde)")
        return redirect(f'/vagas/vaga/{id_vaga}')

def realizar_tarefa(request, id_tarefa):


    tarefa_list = Tarefa.objects.filter(id=id_tarefa).filter(realizada=False)

    if not tarefa_list.exists():
        messages.add_message(request, constants.WARNING,"Tarefa inválida!")
        return redirect(f'/home/empresas/')

    tarefa = tarefa_list.first()
    tarefa.realizada = True
    tarefa.save()
    messages.add_message(request, constants.SUCCESS,"Tarefa realizada com sucesso!")
    return redirect(f'vagas/vaga/{tarefa.vaga.id}')



def envia_email(request, id_vaga):
    vaga = Vagas.objects.get(id=id_vaga)
    assunto = request.POST.get('assunto')
    corpo = request.POST.get('corpo')

    html_cotnent = render_to_string('email/template_email.html', {'corpo' : corpo})
    text_content = strip_tags(html_cotnent)
    email =  EmailMultiAlternatives(assunto, 
                                    text_content, 
                                    settings.EMAIL_HOST_USER,
                                    [vaga.email,]
                                    )
    email.attach_alternative(html_cotnent, "text/html")
    if email.send():
        mail = Emails(
            vaga=vaga,
            assunto=assunto, 
            corpo=corpo, 
            enviado=True
        )
        mail.save()
        messages.add_message(request, constants.SUCCESS,"Email enviado com sucesso!")
        return redirect(f'vagas/vaga/{id_vaga}')
    
    else:
        mail = Emails(
            vaga=vaga,
            assunto=assunto, 
            corpo=corpo, 
            enviado=False
        )
        mail.save()
        messages.add_message(request, constants.ERROR,"Hove um problema ao enviar seu email")
        return redirect(f'vagas/vaga/{id_vaga}')
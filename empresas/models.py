from django.db import models

# Create your models here.


class Tecnologias(models.Model):
    tecnologia = models.CharField(max_length=30)

    def __str__(self):
            return self.tecnologia

class Empresa(models.Model):
    choices_nicho_mercado = (
        ('M', 'Marketing'),
        ('N', 'Nutrição'),
        ('D', 'Design'),
        ('T', 'Tecnologia')
    )
    logo = models.ImageField(upload_to="logo_empresa", null=True)
    nome = models.CharField(max_length=30)
    email = models.EmailField(null=True)
    cidade = models.CharField(max_length=30)
    endereco = models.CharField(max_length=30)
    caracteristicas_empresa = models.TextField()
    nicho_mercado = models.CharField(max_length=4, choices=choices_nicho_mercado)
    tecnologias = models.ManyToManyField(Tecnologias)

    def __str__(self):
        return self.nome

    def qtd_vagas(self):
        return Vagas.objects.filter(empresa__id = self.id).count()


class Vagas(models.Model):
    choices_experiencia = (
        ('J', 'Júnior'),
        ('P', 'Pleno'),
        ('S', 'Sênior')
    )

    choices_status = (
        ('I', 'Interesse'),
        ('C', 'Currículo enviado'),
        ('E', 'Entrevista'),
        ('D', 'Desafio técnico'),
        ('F', 'Finalizado')
    )

    empresa = models.ForeignKey(Empresa, null=True, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=30)
    nivel_experiencia = models.CharField(max_length=2, choices=choices_experiencia)
    data_final =  models.DateField()
    email = models.EmailField(null=True)
    status = models.CharField(max_length=30, choices=choices_status)
    tecnologias_dominadas = models.ManyToManyField(Tecnologias)
    tecnologias_etudar = models.ManyToManyField(Tecnologias, related_name="estudar")

    def progresso(self):
        status_progress = [((i+1) * 20, j[0]) for i, j in enumerate(self.choices_status)]
        status_progress = list(filter(lambda status_progress: status_progress[1] == self.status, status_progress))[0][0]

        return status_progress

    def __str__(self):
         return self.titulo



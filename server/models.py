from django.db import models

class tableEmpilhadeira(models.Model):
    id = models.CharField(max_length=1000, primary_key=True)
    unidade = models.CharField(max_length=1000, null=True, blank=True)
    departamento = models.CharField(max_length=1000, null=True, blank=True)
    secao = models.CharField(max_length=1000, null=True, blank=True)
    patrimonio = models.CharField(max_length=1000, null=True, blank=True)
    descricao = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = 'cadastro_empilhadeira'  # Nome da tabela no banco de dados

# -* coding:utf-8 -*-

from django import forms
from models import *

class FormGrupoMercadoria(forms.ModelForm):
	
	class Meta:
		model = GrupoMercadoria
		fields = ('nome',)

class FormUnidadeMaterial(forms.ModelForm):
	
	class Meta:
		model = UnidadeMaterial
		fields = ('nome',)

class FormCentroCusto(forms.ModelForm):
	
	class Meta:
		model = CentroCusto
		fields = ('nome', 'gerente')

class FormMaterial(forms.ModelForm):
	
	tpMaterial = forms.ChoiceField([('Mercadoria','Mercadoria'), ('Servico', 'Servico')], 
				     initial = ('Mercadoria','Mercadoria'))

	class Meta:
		model = Material
		fields = ('nome', 'fabricante', 'grupoMercadoria', 'unidadeMaterial', 'tpMaterial')

class FormFornecedor(forms.ModelForm):
	razao = forms.CharField(label = 'Razão Social')
	fantasia = forms.CharField(label = 'Nome Fantasia')
	contato = forms.CharField(label = 'Pessoa de Contato')
	tel1 = forms.CharField(min_length = 10, max_length = 10)
	tel2 = forms.CharField(min_length = 10, max_length = 10)
	nrimovel = forms.IntegerField(label = 'Nº')
	complemento = forms.CharField(max_length = 50, required = False)
	uf = forms.ChoiceField([('',''), ('AC','AC'), ('AL','AL'), ('AM','AM'),
				('AP','AP'),('BA','BA'), ('CE','CE'), ('DF','DF'),
				('ES','ES'),('GO','GO'), ('MA','MA'), ('MG','MG'),
				('MS','MS'),('MT','MT'), ('PA','PA'), ('PB','PB'),
				('PI','PI'),('PI','PI'), ('PR','PR'), ('RJ','RJ'),
				('RN','RN'),('RO','RO'), ('RR','RR'), ('RS','RS'),
				('SC','SC'),('SE','SE'),('SP','SP'), ('TO','TO')], 
				initial = ('',''),
				label = 'Estado')
	cep = forms.CharField(min_length = 8, max_length = 8)

	class Meta:
		model = Fornecedor
		fields = ('razao', 'fantasia', 'grupoMercadoria', 'cnpj', 'contato', 'tel1', 'tel2', 'email', 'site', 'logradouro', 'nrimovel', 'complemento', 'bairro', 'cidade', 'uf', 'cep')

class FormRequisicao(forms.ModelForm):
	
	class Meta:
		model = Requisicao
		fields = ('centroCusto', 'diasParaCotacao')

class FormItemRequisicao(forms.ModelForm):
	
	class Meta:
		model = ItemRequisicao
		fields = ('material', 'qtd')

class FormMapaComparativo(forms.ModelForm):
	
	class Meta:
		model = MapaComparativo
		fields = ('cotacaoVencedora', 'obs')














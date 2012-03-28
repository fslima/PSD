# -* coding:utf-8 -*-

from django import forms
from models import *

class FormGrupoMercadoria(forms.ModelForm):
	
	class Meta:
		model = GrupoMercadoria
		fields = ('nomeGrupoMercadoria',)

class FormUnidadeMaterial(forms.ModelForm):
	
	class Meta:
		model = UnidadeMaterial
		fields = ('nomeUnidadeMaterial',)

class FormCentroCusto(forms.ModelForm):
	
	class Meta:
		model = CentroCusto
		fields = ('nomeCentroCusto', 'gerente')

class FormFabricante(forms.ModelForm):
	
	class Meta:
		model = Fabricante
		fields = ('nomeFabricante',)

class FormMaterial(forms.ModelForm):
	
	fabricante = forms.ModelChoiceField(queryset = Fabricante.objects.all(), label = 'Fabricante')
	tpMaterial = forms.ChoiceField([('Mercadoria','Mercadoria'), ('Servico', 'Servico')], 
				     initial = ('Mercadoria','Mercadoria'))

	class Meta:
		model = Material
		fields = ('nomeMaterial', 'fabricante', 'grupoMercadoria', 'unidadeMaterial', 'tpMaterial')

class FormFornecedor(forms.ModelForm):
	razao = forms.CharField(label = 'Razão Social')
	fantasia = forms.CharField(label = 'Nome Fantasia')
	grupoFornecedor = Group.objects.filter(name = 'fornecedor')
	usuario =  forms.ModelChoiceField(queryset = User.objects.filter(groups__in = grupoFornecedor), label = 'Login no Sistema')
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
	status = forms.ChoiceField([('',''), ('Ativo','A'), ('Suspenso','S'), ('Excluido','E'),], 
				initial = ('',''),
				label = 'Situação')
	cep = forms.CharField(min_length = 8, max_length = 8)

	class Meta:
		model = Fornecedor
		fields = ('razao', 'fantasia', 'cnpj', 'usuario', 'tel1', 'tel2', 'email', 'site', 'status', 'logradouro', 'nrimovel', 'complemento', 'bairro', 'cidade', 'uf', 'cep')

class FormGruposFornecedor(forms.ModelForm):

	class Meta:
		model = Fornecedor
		fields = ('grupoMercadoria',)

class FormRequisicao(forms.ModelForm):
	
	class Meta:
		model = Requisicao
		fields = ('centroCusto', 'diasParaCotacao')

class FormItemRequisicao(forms.ModelForm):
	
	class Meta:
		model = ItemRequisicao
		fields = ('material', 'qtd')

class FormCotacao(forms.ModelForm):
	
	class Meta:
		model = Cotacao
		fields = ('vlCotacao', 'obs')

class FormMapaComparativo(forms.ModelForm):
	
	class Meta:
		model = MapaComparativo
		fields = ('obs',)

class FormExibeMapaComparativo(forms.ModelForm):
	dtLiberacao = forms.CharField(label = 'Liberação do Mapa')
	cotacaoVencedora = forms.CharField(label = 'Cotação Vencedora')


	class Meta:
		model = MapaComparativo
		fields = ('dtLiberacao', 'cotacaoVencedora', 'obs')



class FormFiltraMaterial(forms.Form):
	
	nomeMaterial = forms.CharField(required = False)
	fabricante = forms.ModelChoiceField(queryset=Fabricante.objects.all(), required = False, label = 'Fabricante')
	grupoMercadoria = forms.ModelChoiceField(queryset=GrupoMercadoria.objects.all(), required = False, label = 'Grupo de Mercadoria')
	unidadeMaterial = forms.ModelChoiceField(queryset=UnidadeMaterial.objects.all(), required = False, label = 'Unidade de Medida')
	tpMaterial = forms.ChoiceField([('Mercadoria','Mercadoria'), ('Servico', 'Servico')], 
				     initial = ('Mercadoria','Mercadoria'), required = False, label = 'Tipo de Material')

	fields = ('nomeMaterial', 'fabricante', 'grupoMercadoria', 'unidadeMaterial', 'tpMaterial')

class FormFiltraFornecedor(forms.Form):
	razao = forms.CharField(label = 'Razão Social', required = False)
	fantasia = forms.CharField(label = 'Nome Fantasia', required = False)
	cnpj = forms.CharField(min_length = 14, max_length = 14, label = 'CNPJ', required = False)
	grupoFornecedor = Group.objects.filter(name = 'fornecedor')
	usuario =  forms.ModelChoiceField(queryset = User.objects.filter(groups__in = grupoFornecedor), required = False, label = 'Login no Sistema')
	bairro = forms.CharField(label = 'Bairro', required = False)
	cidade = forms.CharField(label = 'Cidade', required = False)
	uf = forms.ChoiceField([('',''), ('AC','AC'), ('AL','AL'), ('AM','AM'),
				('AP','AP'),('BA','BA'), ('CE','CE'), ('DF','DF'),
				('ES','ES'),('GO','GO'), ('MA','MA'), ('MG','MG'),
				('MS','MS'),('MT','MT'), ('PA','PA'), ('PB','PB'),
				('PI','PI'),('PI','PI'), ('PR','PR'), ('RJ','RJ'),
				('RN','RN'),('RO','RO'), ('RR','RR'), ('RS','RS'),
				('SC','SC'),('SE','SE'),('SP','SP'), ('TO','TO')], 
				initial = ('',''),
				label = 'Estado', required = False)

	fields = ('razao', 'fantasia', 'cnpj', 'usuario', 'bairro', 'cidade', 'uf')

class FormFiltraMapaComparativo(forms.Form):
	dtLiberacaoP = forms.DateField(
				label = 'Liberacao a partir de',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
				required = False
			)
	dtLiberacaoA = forms.DateField(
				label = 'Liberacao até',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
				required = False
			)
	fornecedorVencedor = forms.ModelChoiceField(queryset=Fornecedor.objects.all(), required = False, label = 'Forncedor Vencedor')
	
	
	fields = ('dtLiberacaoP', 'dtLiberacaoA', 'fornecedorVencedor')

class FormFiltraRequisicao(forms.Form):
	dtRequisicaoP = forms.DateField(
				label = 'Criação a partir de',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
				required = False
			)
	dtRequisicaoA = forms.DateField(
				label = 'Criação até',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
				required = False
			)
	dtDeferimentoP = forms.DateField(
				label = 'Deferimento a partir de',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
				required = False
			)
	dtDeferimentoA = forms.DateField(
				label = 'Deferimento até',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
				required = False
			)
	itemRequisicao = forms.ModelChoiceField(queryset=Material.objects.all(), required = False, label = 'Item da Requisição')
	status = forms.ChoiceField([('',''), ('Aprovada','Aprovada'), ('Aguardando Aprovação','Aguardando Aprovação'), ('Reprovada','Reprovada')], 
				initial = ('',''),
				label = 'Situação', required = False)
	
	
	fields = ('dtRequisicaoP', 'dtRequisicaoA', 'itemRequisicao', 'dtDeferimentoP', 'dtDeferimentoA')






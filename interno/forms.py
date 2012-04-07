# -* coding:utf-8 -*-

from django import forms
from models import *

class FormGrupoMercadoria(forms.ModelForm):
	nomeGrupoMercadoria = forms.CharField(label = 'Grupo de Mercadoria')
	
	class Meta:
		model = GrupoMercadoria
		fields = ('nomeGrupoMercadoria',)

class FormUnidadeMaterial(forms.ModelForm):
	nomeUnidadeMaterial = forms.CharField(label = 'Unidade de Medida')
	
	class Meta:
		model = UnidadeMaterial
		fields = ('nomeUnidadeMaterial',)

class FormCentroCusto(forms.ModelForm):
	nomeCentroCusto = forms.CharField(label = 'Centro de Custo')
	
	class Meta:
		model = CentroCusto
		fields = ('nomeCentroCusto', 'gerente')

class FormFabricante(forms.ModelForm):
	nomeFabricante = forms.CharField(label = 'Fabricante')
	
	class Meta:
		model = Fabricante
		fields = ('nomeFabricante',)

class FormMaterial(forms.ModelForm):
	nomeMaterial = forms.CharField(label = 'Nome')
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
	status = forms.ChoiceField([('',''), ('A','Ativo'), ('S','Suspenso'), ('E','Excluido'),], 
				initial = ('',''),
				label = 'Situação')
	cep = forms.CharField(min_length = 8, max_length = 8)

	class Meta:
		model = Fornecedor
		fields = ('razao', 'fantasia', 'cnpj', 'usuario', 'tel1', 'tel2', 'email', 'site', 'status', 'logradouro', 'nrimovel', 'complemento', 'bairro', 'cidade', 'uf', 'cep')

class FormGruposFornecedor(forms.ModelForm):
	#forms.CharField(label = 'Fabricante')

	class Meta:
		model = Fornecedor
		fields = ('grupoMercadoria',)

class FormRequisicao(forms.ModelForm):
	centroCusto = forms.ModelChoiceField(queryset=CentroCusto.objects.all(), label = 'Centro de Custo')
	diasParaCotacao = forms.IntegerField(label = 'Nº de dias para cotação')

	class Meta:
		model = Requisicao
		fields = ('centroCusto', 'diasParaCotacao')

class FormItemRequisicao(forms.ModelForm):
	material = forms.ModelChoiceField(queryset=Material.objects.all(), label = 'Material / Serviço')
	qtd = forms.IntegerField(label = 'Quantidade')
	
	class Meta:
		model = ItemRequisicao
		fields = ('material', 'qtd')

class FormCotacao(forms.ModelForm):
	vlCotacao = forms.DecimalField(max_digits = 20, decimal_places = 2, label = 'Valor Unitário')
	
	class Meta:
		model = Cotacao
		fields = ('vlCotacao', 'obs')

class FormMapaComparativo(forms.ModelForm):
	
	class Meta:
		model = MapaComparativo
		fields = ('obs',)

class FormExibeCotacao(forms.ModelForm):
	vlCotacao = forms.DecimalField(max_digits = 20, decimal_places = 2, label = 'Valor Unitário')
	itemRequisicao = forms.CharField(label = 'Item da Cotação')
	dtLimite = forms.CharField(label = 'Data Limite')

	class Meta:
		model = Cotacao
		fields = ('itemRequisicao', 'dtLimite', 'vlCotacao', 'obs')

class FormExibeMapaComparativo(forms.ModelForm):
	dtLiberacao = forms.CharField(label = 'Liberação do Mapa')
	cotacaoVencedora = forms.CharField(label = 'Cotação Vencedora')


	class Meta:
		model = MapaComparativo
		fields = ('dtLiberacao', 'cotacaoVencedora', 'obs')

class FormFiltraCotacao(forms.Form):
	vlCotacaoP = forms.DecimalField(max_digits = 20, decimal_places = 2, required = False, label = 'Valor Unitário a partir de')
	vlCotacaoA = forms.DecimalField(max_digits = 20, decimal_places = 2, required = False, label = 'Valor Unitário ate')
	dtLimiteP = forms.DateField(
				label = 'Data limite a partir de',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
				required = False
			)
	dtLimiteA = forms.DateField(
				label = 'Data limite ate',
				widget = forms.DateInput(format = '%d/%m/%Y'),
				input_formats = ['%d/%m/%Y'],
				required = False
			)
	itemRequisicao = forms.ModelChoiceField(queryset=Material.objects.all(), required = False, label = 'Item da Cotação')
	
	
	fields = ('dtLimiteP', 'dtLimiteA', 'dtLimiteP', 'dtLimiteA', 'itemRequisicao')

class FormFiltraMaterial(forms.Form):
	
	nomeMaterial = forms.CharField(label = 'Nome', required = False)
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
	status = forms.ChoiceField([('',''), ('A','Ativo'), ('S','Suspenso'), ('E','Excluido'),], 
				initial = ('',''),
				label = 'Situação', required = False)

	fields = ('razao', 'fantasia', 'cnpj', 'usuario', 'bairro', 'cidade', 'uf', 'status')

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
	status = forms.ChoiceField([('',' ------- '), ('Aberto','Aberto'), ('Finalizado','Finalizado')], 
				initial = ('',''),
				label = 'Situação', required = False)
	
	
	fields = ('dtLiberacaoP', 'dtLiberacaoA', 'fornecedorVencedor', 'status')

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
	centroCusto = forms.ModelChoiceField(queryset=CentroCusto.objects.all(), required = False, label = 'Centro de Custo')
	itemRequisicao = forms.ModelChoiceField(queryset=Material.objects.all(), required = False, label = 'Item da Requisição')
	status = forms.ChoiceField([('',''), ('Aprovada','Aprovada'), ('Aguardando Aprovação','Aguardando Aprovação'), ('Reprovada','Reprovada')], 
				initial = ('',''),
				label = 'Situação', required = False)
	
	
	fields = ('dtRequisicaoP', 'dtRequisicaoA', 'itemRequisicao', 'dtDeferimentoP', 'dtDeferimentoA', 'centroCusto')






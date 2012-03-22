# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class GrupoMercadoria(models.Model):
	def __unicode__(self):
		return self.nome

	nome = models.CharField(max_length = 50)
	
	def adiciona(self, request, id_objeto):
		self.save()
		return 'validos'

	class Meta:
		db_table = 'grupo_mercadoria'

class UnidadeMaterial(models.Model):
	def __unicode__(self):
		return self.nome

	nome = models.CharField(max_length = 50)
	
	def adiciona(self, request, id_objeto):
		self.save()
		return 'validos'

	class Meta:
		db_table = 'unidade_material'

class Material(models.Model):
	def __unicode__(self):
		return self.nome
	
	nome = models.CharField(max_length = 50)
	fabricante = models.CharField(max_length = 50)
	grupoMercadoria = models.ForeignKey(GrupoMercadoria, related_name = 'gm_material')
	unidadeMaterial = models.ForeignKey(UnidadeMaterial, related_name = 'un_material')
	tpMaterial = models.CharField(max_length = 50)	
	vlUltimaCompra = models.DecimalField(max_digits = 20, decimal_places = 2, null = True)
	dtUltimaCompra = models.DateField(null = True)
	usuario = models.ForeignKey(User)

	def adiciona(self, request, id_objeto):
		self.usuario = request.user
		self.vlUltimaCompra = '0.00'
		self.dtUltimaCompra = datetime.now()
		self.save()
		return 'validos'
	
	class Meta:
		db_table = 'material'

class Fornecedor(models.Model):
	def __unicode__(self):
		return self.fantasia
	
	razao = models.CharField(max_length = 50)
	fantasia = models.CharField(max_length = 50)
	cnpj = models.CharField(max_length = 14)
	grupoMercadoria = models.ManyToManyField(GrupoMercadoria, related_name = 'gm_fornecedor')
	contato = models.CharField(max_length = 50)
	tel1 = models.BigIntegerField(max_length = 10)
	tel2 = models.BigIntegerField(max_length = 10, null = True, blank = True)
	email = models.EmailField(max_length = 50)
	site = models.URLField(null = True)
	logradouro = models.CharField(max_length = 50)
	nrimovel = models.IntegerField()
	complemento = models.CharField(max_length = 50)
	bairro = models.CharField(max_length = 50)
	cidade = models.CharField(max_length = 50)
	uf = models.CharField(max_length = 2)
	cep = models.BigIntegerField(max_length = 8)
	usuario = models.ForeignKey(User)

	def adiciona(self, request, id_objeto):
		self.usuario = request.user
		self.save()
		return 'validos'
	
	class Meta:
		db_table = 'fornecedor'

class CentroCusto(models.Model):
	def __unicode__(self):
		return self.nome

	nome = models.CharField(max_length = 50)
	gerente = models.ForeignKey(User)	

	def adiciona(self, request, id_objeto):
		self.save()
		return 'validos'

	class Meta:
		db_table = 'centro_custo'

class Requisicao(models.Model):
	def __unicode__(self):
		return str(self.id)

	dtRequisicao = models.DateField()
	centroCusto = models.ForeignKey(CentroCusto, related_name = 'cc_requisicao')
	solicitante = models.ForeignKey(User)
	status = models.CharField(max_length = 50)
	dtDeferimento = models.DateField(null = True)
	diasParaCotacao = models.PositiveSmallIntegerField()
		

	def adiciona(self, request, id_objeto):
		self.dtRequisicao = datetime.now()
		self.status = 'Aguardando Aprovação'
		self.solicitante = request.user
		self.save()
		return 'validos'

	def aprova(self):
		if self.status == u'Aguardando Aprovação':
			self.status = 'Aprovada'
			self.dtDeferimento = datetime.now()
			self.save()
			itens = ItemRequisicao.objects.filter(requisicao = self)
			for item in itens:
				Cotacao().adiciona(item)

	class Meta:
		db_table = 'requisicao'

class ItemRequisicao(models.Model):
	def __unicode__(self):
		return self.material.nome

	requisicao = models.ForeignKey(Requisicao, related_name = 'requisicao_do_item')
	material = models.ForeignKey(Material, related_name = 'material_do_item')
	qtd = models.PositiveSmallIntegerField()
	status = models.CharField(max_length = 50)

	def adiciona(self, request, id_objeto):
		self.requisicao = Requisicao.objects.get(pk = id_objeto)
		self.status = 'Aguardando Cotações'
		self.save()
		return 'validos'

	def alteraStatus(self, status):
		self.status = status
		self.save()

	class Meta:
		db_table = 'item_requisicao'

class Cotacao(models.Model):
	def __unicode__(self):
		return self.fornecedor.fantasia

	itemRequisicao = models.ForeignKey(ItemRequisicao, related_name = 'item_proposta')
	fornecedor = models.ForeignKey(Fornecedor, related_name = 'fornecedor_proposta')
	vlCotacao = models.DecimalField(max_digits = 20, decimal_places = 2, null = True)
	obs = models.TextField(max_length = 100, null = True)

	def adiciona(self, item):
		fornecedores = Fornecedor.objects.filter(grupoMercadoria = item.material.grupoMercadoria)
		for fornecedor in fornecedores:
			cotacao = Cotacao(itemRequisicao = item, fornecedor = fornecedor)
			cotacao.save()
		MapaComparativo().adiciona(item)

	class Meta:
		db_table = 'cotacao'

class MapaComparativo(models.Model):
	def __unicode__(self):
		return str(self.id)

	cotacao = models.ManyToManyField(Cotacao, related_name = 'cotacoes_do_mapa', null = True)
	cotacaoVencedora = models.ForeignKey(Cotacao, related_name = 'cotacao_vencedora', null = True)
	obs = models.TextField(max_length = 100, null = True)

	def adiciona(self, item):
		self.save()
		cotacoes = Cotacao.objects.filter(itemRequisicao = item)
		for cotacao in cotacoes:
			self.cotacao.add(cotacao)
	def finaliza(self):
		self.cotacaoVencedora.itemRequisicao.alteraStatus('Mapa Finalizado')
		self.save()

	class Meta:
		db_table = 'mapa_comparativo'










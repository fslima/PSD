# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class GrupoMercadoria(models.Model):
	def __unicode__(self):
		return self.nome

	nome = models.CharField(max_length = 50)
	
	def validaAtrib(self):
		return 'validos'

	class Meta:
		db_table = 'grupo_mercadoria'

class UnidadeMaterial(models.Model):
	def __unicode__(self):
		return self.nome

	nome = models.CharField(max_length = 50)
	
	def validaAtrib(self):
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

	def validaAtrib(self):
		self.vlUltimaCompra = '0.00'
		self.dtUltimaCompra = datetime.now()
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
	site = models.URLField()
	logradouro = models.CharField(max_length = 50)
	nrimovel = models.IntegerField()
	complemento = models.CharField(max_length = 50)
	bairro = models.CharField(max_length = 50)
	cidade = models.CharField(max_length = 50)
	uf = models.CharField(max_length = 2)
	cep = models.BigIntegerField(max_length = 8)
	usuario = models.ForeignKey(User)

	def validaAtrib(self):
		return 'validos'
	
	class Meta:
		db_table = 'fornecedor'

class CentroCusto(models.Model):
	def __unicode__(self):
		return self.nome

	nome = models.CharField(max_length = 50)
	gerente = models.ForeignKey(User)	

	def validaAtrib(self):
		return 'validos'

	class Meta:
		db_table = 'centro_custo'

class Requisicao(models.Model):
	def __unicode__(self):
		return self.nome

	dtRequisicao = models.DateField()
	centroCusto = models.ForeignKey(CentroCusto, related_name = 'cc_requisicao')
	solicitante = models.ForeignKey(User)
	status = models.CharField(max_length = 10)
	dtDeferimento = models.DateField()
	diasParaCotacao = models.PositiveSmallIntegerField()
		

	def validaAtrib(self):
		return 'validos'

	class Meta:
		db_table = 'requisicao'

class ItemRequisicao(models.Model):
	def __unicode__(self):
		return self.nome

	requisicao = models.ForeignKey(Requisicao, related_name = 'requisicao_do_item')
	material = models.ForeignKey(Material, related_name = 'material_do_item')
	qtd = models.PositiveSmallIntegerField()

	def validaAtrib(self):
		return 'validos'

	class Meta:
		db_table = 'item_requisicao'

class Cotacao(models.Model):
	def __unicode__(self):
		return self.nome

	itemRequisicao = models.ForeignKey(ItemRequisicao, related_name = 'item_proposta')
	fornecedor = models.ForeignKey(Fornecedor, related_name = 'fornecedor_proposta')
	vlCotacao = models.DecimalField(max_digits = 20, decimal_places = 2)
	obs = models.TextField(max_length = 100)

	def validaAtrib(self):
		return 'validos'

	class Meta:
		db_table = 'cotacao'

class MapaComparativo(models.Model):
	def __unicode__(self):
		return self.nome

	cotacao = models.ManyToManyField(Cotacao, related_name = 'cotacoes_do_mapa')
	cotacaoVencedora = models.ForeignKey(Cotacao, related_name = 'cotacao_vencedora')
	obs = models.TextField(max_length = 100)

	def validaAtrib(self):
		return 'validos'

	class Meta:
		db_table = 'mapa_comparativo'










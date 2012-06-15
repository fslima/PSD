# -*- coding:utf-8 -*-

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from interno.models import *
from forms import *
from django.db import connection, transaction

@login_required
def relatorios(request):
	if not request.user.has_perm('interno.aprovar_mapa') and not request.user.has_perm('interno.aprovar_requisicao'):
		erro = 'Área restrita à gerentes'
		return render_to_response("500.html", locals(), context_instance = RequestContext(request))
	return render_to_response('relatorios.html', locals(), context_instance = RequestContext(request))

@login_required
def fornecedor(request, tpObjeto, tpRel):
	if not request.user.has_perm('interno.aprovar_mapa') and not request.user.has_perm('interno.aprovar_requisicao'):
		erro = 'Área restrita à gerentes'
		return render_to_response("500.html", locals(), context_instance = RequestContext(request))
	if str(tpRel) == 'geral':
		data = datetime.now()
		titulo = 'Melhores fornecedores'
		radicalObjeto = 'Fornecedo'
		formpost = FormRelFornecedorGeral(request.POST, request.FILES)
		formget = FormRelFornecedorGeral()
		colunas = ['Razão Social', 'Nome Fantasia', 'Cotações Vencidas']
		if request.method == 'POST':
			form = formpost
			if form.is_valid():
				titulo = 'Melhores fornecedores de '+str(request.POST['dt_liberacaoP'])+' à '+str(request.POST['dt_liberacaoA'])
				infoRel = '* Nesse Relatório são listados apenas Fornecedores que venceram pelo menos uma cotação no período informado'
				cursor = connection.cursor()
				cursor.execute("select f.id, f.razao, f.fantasia, count(*) from cotacao c, fornecedor f where f.id = c.fornecedor_id and c.id in(select cotacao_vencedora_id from mapa m where m.dt_liberacao between %s and %s) group by 1, 2, 3 order by 4 desc", [request.POST['dt_liberacaoP'], request.POST['dt_liberacaoA']])
				query = cursor.fetchall()
				total = len(query)
				return render_to_response('relatorio.html', locals(), context_instance = RequestContext(request))
			else:
				return render_to_response('gerador_relatorio.html', locals(), context_instance = RequestContext(request))	
		else:
			form = FormRelFornecedorGeral()
		return render_to_response('gerador_relatorio.html', locals(), context_instance = RequestContext(request))

	if str(tpRel) == 'grupomercadoria':
		data = datetime.now()
		titulo = 'Melhores fornecedores por grupo de mercadoria'
		radicalObjeto = 'Fornecedo'
		formpost = FormRelFornecedorGrupoMercadoria(request.POST, request.FILES)
		formget = FormRelFornecedorGrupoMercadoria()
		colunas = ['Razão Social', 'Nome Fantasia', 'Cotações Vencidas']
		if request.method == 'POST':
			form = formpost
			if form.is_valid():
				grupo_mercadoria = GrupoMercadoria.objects.get(pk = request.POST['grupo_mercadoria'])
				titulo = 'Melhores fornecedores de '+str(grupo_mercadoria)+' de '+str(request.POST['dt_liberacaoP'])+' à '+str(request.POST['dt_liberacaoA'])
				infoRel = '* Nesse Relatório são listados apenas Fornecedores que venceram pelo menos uma cotação de '+str(grupo_mercadoria)+' no período informado'
				cursor = connection.cursor()
				cursor.execute("select f.id, f.razao, f.fantasia, count(*) from cotacao c, fornecedor f where f.id = c.fornecedor_id and c.id in(select cotacao_vencedora_id from mapa m where m.dt_liberacao between %s and %s) and c.id in (select id from cotacao where item_requisicao_id in(select id from item_requisicao where material_id in(select id from material where grupo_mercadoria_id = %s))) group by 1, 2, 3 order by 4 desc", [request.POST['dt_liberacaoP'], request.POST['dt_liberacaoA'], request.POST['grupo_mercadoria']])
				query = cursor.fetchall()
				total = len(query)
				return render_to_response('relatorio.html', locals(), context_instance = RequestContext(request))
			else:
				return render_to_response('gerador_relatorio.html', locals(), context_instance = RequestContext(request))	
		else:
			form = FormRelFornecedorGrupoMercadoria()
		return render_to_response('gerador_relatorio.html', locals(), context_instance = RequestContext(request))


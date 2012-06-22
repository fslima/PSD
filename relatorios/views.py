# -*- coding:utf-8 -*-

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from interno.models import *
from forms import *
from django.db import connection, transaction
from pyExcelerator import *
from os import system

def gerar_excel(titulo, colunas, registros):
	data = datetime.now()
	wb = Workbook()
	ws1 = wb.add_sheet(titulo)
	colunas.insert(0, 'Código')
	for coluna in colunas:
		ws1.write(0, colunas.index(coluna), coluna)
	nlinha = 1
	ncoluna = 0
	for registro in registros:
		for coluna in registro:
			ws1.write(nlinha, ncoluna, coluna)
			ncoluna += 1
		nlinha += 1
		ncoluna = 0
	nome_arquivo = 'temp/'+str(data)+'.xls'
	wb.save(nome_arquivo)
	response = HttpResponse(open(nome_arquivo, 'r').read(), mimetype = 'application/ms-excel')
	response['Content-Disposition'] = 'attachment; filename='+nome_arquivo
	system('rm "/opt/github/PSD/'+str(nome_arquivo)+'"')
	return response

@login_required
def relatorios(request):
	if not request.user.has_perm('interno.aprovar_mapa') and not request.user.has_perm('interno.aprovar_requisicao'):
		erro = 'Área restrita à gerentes'
		return render_to_response("500.html", locals(), context_instance = RequestContext(request))
	return render_to_response('relatorios.html', locals(), context_instance = RequestContext(request))

@login_required
def gerar_relatorio(request, tpObjeto, tpRel):
	if not request.user.has_perm('interno.aprovar_mapa') and not request.user.has_perm('interno.aprovar_requisicao'):
		erro = 'Área restrita à gerentes'
		return render_to_response("500.html", locals(), context_instance = RequestContext(request))
	data = datetime.now()
	if str(tpObjeto) == 'fornecedor':
		radicalObjeto = 'Fornecedo'
		colunas = ['Razão Social', 'Nome Fantasia', 'Cotações Vencidas']
		if str(tpRel) == 'geral':
			titulo = 'Melhores fornecedores'
			formpost = FormRelGeral(request.POST, request.FILES)
			formget = FormRelGeral()
			if request.method == 'POST':
				form = formpost
				if form.is_valid():
					titulo = 'Melhores fornecedores de '+str(request.POST['dt_liberacaoP'])+' à '+str(request.POST['dt_liberacaoA'])
					infoRel = '* Nesse Relatório são listados apenas Fornecedores que venceram pelo menos uma cotação no período informado'
					cursor = connection.cursor()
					cursor.execute("select f.id, f.razao, f.fantasia, count(*) from cotacao c, fornecedor f where f.id = c.fornecedor_id and c.id in(select cotacao_vencedora_id from mapa m where m.dt_liberacao between %s and %s) group by 1, 2, 3 order by 4 desc", [request.POST['dt_liberacaoP'], request.POST['dt_liberacaoA']])
					query = cursor.fetchall()
					total = len(query)
					if request.POST['formato'] == 'Planilha':
						return gerar_excel(titulo, colunas, query)
					return render_to_response('relatorio.html', locals(), context_instance = RequestContext(request))	
				else:
					return render_to_response('gerador_relatorio.html', locals(), context_instance = RequestContext(request))	
			else:
				form = FormRelGeral()
			return render_to_response('gerador_relatorio.html', locals(), context_instance = RequestContext(request))

		if str(tpRel) == 'grupomercadoria':
			titulo = 'Melhores fornecedores por grupo de mercadoria'
			formpost = FormRelGrupoMercadoria(request.POST, request.FILES)
			formget = FormRelGrupoMercadoria()
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
					if request.POST['formato'] == 'Planilha':
						return gerar_excel(titulo, colunas, query)
					return render_to_response('relatorio.html', locals(), context_instance = RequestContext(request))
				else:
					return render_to_response('gerador_relatorio.html', locals(), context_instance = RequestContext(request))	
			else:
				form = FormRelGrupoMercadoria()
			return render_to_response('gerador_relatorio.html', locals(), context_instance = RequestContext(request))

	if str(tpObjeto) == 'material':
		radicalObjeto = 'Materia'
		colunas = ['Material / Serviço', 'Quantidade']
		if str(tpRel) == 'geral':
			titulo = 'Materiais / Serviços Solicitados'
			formpost = FormRelGeral(request.POST, request.FILES)
			formget = FormRelGeral()
			if request.method == 'POST':
				form = formpost
				if form.is_valid():
					titulo = 'Materiais / Serviços solicitados de '+str(request.POST['dt_liberacaoP'])+' à '+str(request.POST['dt_liberacaoA'])
					infoRel = '* Nesse Relatório são listados todos materiais / serviços solicitados no período informado'
					cursor = connection.cursor()
					cursor.execute("select m.id, m.nome_material, sum(i.qtd) from item_requisicao i, material m where m.id = i.material_id and requisicao_id in(select id from requisicao where dt_requisicao between %s and %s) group by 1, 2 order by 3 desc", [request.POST['dt_liberacaoP'], request.POST['dt_liberacaoA']])
					query = cursor.fetchall()
					total = len(query)
					if request.POST['formato'] == 'Planilha':
						return gerar_excel(titulo, colunas, query)
					return render_to_response('relatorio.html', locals(), context_instance = RequestContext(request))
				else:
					return render_to_response('gerador_relatorio.html', locals(), context_instance = RequestContext(request))	
			else:
				form = FormRelGeral()
			return render_to_response('gerador_relatorio.html', locals(), context_instance = RequestContext(request))

		if str(tpRel) == 'grupomercadoria':
			titulo = 'Materiais / Serviços Solicitados por grupo de mercadoria'
			formpost = FormRelGrupoMercadoria(request.POST, request.FILES)
			formget = FormRelGrupoMercadoria()
			if request.method == 'POST':
				form = formpost
				if form.is_valid():
					grupo_mercadoria = GrupoMercadoria.objects.get(pk = request.POST['grupo_mercadoria'])
					titulo = 'Materiais / Serviços de '+str(grupo_mercadoria)+' solicitados de '+str(request.POST['dt_liberacaoP'])+' à '+str(request.POST['dt_liberacaoA'])
					infoRel = '* Nesse Relatório são listados todos materiais / serviços de '+str(grupo_mercadoria)+' solicitados no período informado'
					cursor = connection.cursor()
					cursor.execute("select m.id, m.nome_material, sum(i.qtd) from item_requisicao i, material m where m.id = i.material_id and m.grupo_mercadoria_id = %s and requisicao_id in(select id from requisicao where dt_requisicao between %s and %s) group by 1, 2 order by 3 desc", [request.POST['grupo_mercadoria'], request.POST['dt_liberacaoP'], request.POST['dt_liberacaoA']])
					query = cursor.fetchall()
					total = len(query)
					if request.POST['formato'] == 'Planilha':
						return gerar_excel(titulo, colunas, query)
					return render_to_response('relatorio.html', locals(), context_instance = RequestContext(request))
				else:
					return render_to_response('gerador_relatorio.html', locals(), context_instance = RequestContext(request))	
			else:
				form = FormRelGrupoMercadoria()
			return render_to_response('gerador_relatorio.html', locals(), context_instance = RequestContext(request))


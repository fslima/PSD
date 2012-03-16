from datetime import datetime, date, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from models import *
from django.template import RequestContext
from forms import *

def sair(request):
	logout(request)
	return HttpResponseRedirect("/login")

@login_required
def inicio(request):
	data = datetime.now()
	return render_to_response('inicio.html', locals())

@login_required
def adiciona(request, objeto):
	if str(objeto) == 'grupomercadoria':
		titulo = 'Grupo de Mercadoria'
		formpost = FormGrupoMercadoria(request.POST, request.FILES)
		formget = FormGrupoMercadoria()
	if str(objeto) == 'unidadematerial':
		titulo = 'Unidade de Medida do Material'
		formpost = FormUnidadeMaterial(request.POST, request.FILES)
		formget = FormUnidadeMaterial()	
	if str(objeto) == 'centrocusto':
		titulo = 'Centro de Custo'
		formpost = FormCentroCusto(request.POST, request.FILES, )
		formget = FormCentroCusto()
	if str(objeto) == 'material':
		titulo = 'Material'
		formpost = FormMaterial(request.POST, request.FILES, )
		formget = FormMaterial()
	if str(objeto) == 'fornecedor':
		titulo = 'Fornecedor'
		formpost = FormFornecedor(request.POST, request.FILES, )
		formget = FormFornecedor()
	if request.method == 'POST': 
		form = formpost
		if form.is_valid():
			objeto_form = form.save(commit = False)
			objeto_form.usuario = request.user
			if objeto_form.validaAtrib() != 'validos':
				erro =  objeto_form.validaAtrib()
				return render_to_response("adiciona.html", locals(), context_instance = RequestContext(request))
			objeto_form.save()
			return HttpResponseRedirect("/lista/"+str(objeto))
		else:
			return render_to_response("adiciona.html", locals(), context_instance = RequestContext(request))
	else: 
		form = formget
		return render_to_response("adiciona.html", locals(), context_instance = RequestContext(request))

@login_required
def lista(request, objeto):
	if str(objeto) == 'grupomercadoria':
		titulo = 'Lista de Grupos de Mercadoria'
		lista_vazia = 'Nenhum Grupo de Mercadoria Cadastrado'
		lista = GrupoMercadoria.objects.all().order_by('nome')
	if str(objeto) == 'unidadematerial':
		titulo = 'Lista de Unidades de Medida do Material'
		lista_vazia = 'Nenhuma Unidade de Medida Cadastrada'
		lista = UnidadeMaterial.objects.all().order_by('nome')
	if str(objeto) == 'centrocusto':
		titulo = 'Lista de Centros de Custo'
		lista_vazia = 'Nenhum Centro de Custo Cadastrado'
		lista = CentroCusto.objects.all().order_by('nome')
	if str(objeto) == 'material':
		titulo = 'Lista de Materiais'
		lista_vazia = 'Nenhum Material Cadastrado'
		lista = Material.objects.all().order_by('nome')
	if str(objeto) == 'fornecedor':
		titulo = 'Lista de Fornecedores'
		lista_vazia = 'Nenhum Fornecedor Cadastrado'
		lista = Fornecedor.objects.all().order_by('fantasia')
	return render_to_response('lista.html', locals())

def exibe(request, objeto, id_objeto):
	if str(objeto) == 'grupomercadoria':
		titulo = 'Grupo de Mercadoria'
		objeto = get_object_or_404(GrupoMercadoria, pk = id_objeto)
		form = FormGrupoMercadoria(instance = objeto)
	if str(objeto) == 'unidadematerial':
		titulo = 'Unidade de Medida'
		objeto = get_object_or_404(UnidadeMaterial, pk = id_objeto)
		form = FormUnidadeMaterial(instance = objeto)
	if str(objeto) == 'centrocusto':
		titulo = 'Centro de Custo'
		objeto = get_object_or_404(CentroCusto, pk = id_objeto)
		form = FormCentroCusto(instance = objeto)
	if str(objeto) == 'material':
		titulo = 'Material'
		objeto = get_object_or_404(Material, pk = id_objeto)
		form = FormMaterial(instance = objeto)
	if str(objeto) == 'fornecedor':
		titulo = 'Fornecedor'
		objeto = get_object_or_404(Fornecedor, pk = id_objeto)
		form = FormFornecedor(instance = objeto)
	return render_to_response('exibe.html', locals())

@login_required
def edita(request, objeto, id_objeto):
	if str(objeto) == 'grupomercadoria':
		grupoMercadoria_para_editar = get_object_or_404(GrupoMercadoria, pk = id_objeto)
		formpost = FormGrupoMercadoria(request.POST, request.FILES, instance = grupoMercadoria_para_editar)
		formget = FormGrupoMercadoria(instance = grupoMercadoria_para_editar)
		titulo = 'Grupo de Mercadoria'		
	if str(objeto) == 'unidadematerial':
		titulo = 'Unidade de Medida'
		unidadeMaterial_para_editar = get_object_or_404(UnidadeMaterial, pk = id_objeto)
		formpost = FormUnidadeMaterial(request.POST, request.FILES, instance = unidadeMaterial_para_editar)
		formget = FormUnidadeMaterial(instance = unidadeMaterial_para_editar)	
	if str(objeto) == 'centrocusto':
		titulo = 'Centro de Custo'
		centroCusto_para_editar = get_object_or_404(CentroCusto, pk = id_objeto)
		formpost = FormCentroCusto(request.POST, request.FILES, instance = centroCusto_para_editar)
		formget = FormCentroCusto(instance = centroCusto_para_editar)	
	if str(objeto) == 'material':
		titulo = 'Material'
		material_para_editar = get_object_or_404(Material, pk = id_objeto)
		formpost = FormMaterial(request.POST, request.FILES, instance = material_para_editar)
		formget = FormMaterial(instance = material_para_editar)
	if str(objeto) == 'fornecedor':
		titulo = 'Fornecedor'
		fornecedor_para_editar = get_object_or_404(Fornecedor, pk = id_objeto)
		formpost = FormFornecedor(request.POST, request.FILES, instance = fornecedor_para_editar)
		formget = FormFornecedor(instance = fornecedor_para_editar)
	if request.method == 'POST':
		form = formpost
		if form.is_valid():
			form.save()
			return HttpResponseRedirect("/lista/"+str(objeto))
		else:
			return render_to_response('edita.html', locals(), context_instance = RequestContext(request))	
	else:
		form = formget
	return render_to_response('edita.html', locals(), context_instance = RequestContext(request))

@login_required
def deleta(request, objeto, id_objeto):
	if str(objeto) == 'grupomercadoria':
		objeto_para_deletar = get_object_or_404(GrupoMercadoria, pk = id_objeto)
		form = FormGrupoMercadoria(instance = objeto_para_deletar)
	if str(objeto) == 'centrocusto':
		objeto_para_deletar = get_object_or_404(CentroCusto, pk = id_objeto)
		form = FormCentroCusto(instance = objeto_para_deletar)
	if str(objeto) == 'unidadematerial':
		objeto_para_deletar = get_object_or_404(UnidadeMaterial, pk = id_objeto)
		form = FormUnidadeMaterial(instance = objeto_para_deletar)
	if str(objeto) == 'material':
		objeto_para_deletar = get_object_or_404(Material, pk = id_objeto)
		form = FormMaterial(instance = objeto_para_deletar)
	if str(objeto) == 'fornecedor':
		objeto_para_deletar = get_object_or_404(Fornecedor, pk = id_objeto)
		form = FormFornecedor(instance = objeto_para_deletar)
	if request.method == 'POST':
		objeto_para_deletar.delete()
		return HttpResponseRedirect("/lista/"+str(objeto))
	else:
		return render_to_response('deleta.html', locals(), context_instance = RequestContext(request))














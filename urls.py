# -*- coding:utf-8 -*-

from django.conf.urls.defaults import *
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth.views import *
from django.contrib import admin
from PSD.interno.views import *

admin.autodiscover()

urlpatterns = patterns('',
#	(r'^data/$', data_atual),
#	(r'^data/plus/\d{1,2}/$', horas_depois),
	(r'^admin/', include(admin.site.urls)),
	
	(r'^$', login, { 'template_name': 'login.html' }),
	(r'^sair$', sair),
	(r'^inicio$', inicio),
	
	(r'^cadastro$', cadastro),
	(r'^lista/(?P<tpObjeto>\w+)$', lista),
	(r'^adiciona/(?P<tpObjeto>\w+)/(?P<idObjeto>\d+)/$', adiciona),
	(r'^filtra/(?P<tpObjeto>\w+)', filtra),
	(r'^exibe/(?P<tpObjeto>\w+)/(?P<idObjeto>\d+)/$', exibe),
	(r'^edita/(?P<tpObjeto>\w+)/(?P<idObjeto>\d+)/$', edita),
	(r'^deleta/(?P<tpObjeto>\w+)/(?P<idObjeto>\d+)/$', deleta),
	(r'^finaliza/(?P<tpObjeto>\w+)/(?P<idObjeto>\d+)/$', finaliza),
	(r'^aprova/(?P<tpObjeto>\w+)/(?P<idObjeto>\d+)/$', aprova),
	(r'^reprova/(?P<tpObjeto>\w+)/(?P<idObjeto>\d+)/$', reprova),

#	(r'^servico/oportunidades/abertas$', servico__oportunidades_abertas),
#	(r'^servico/exibir/(?P<tpObjeto>\w+)', servico_exibir),
#	(r'^servico/cadastrar/(?P<tpObjeto>\w+)', servico_cadastrar),
#	(r'^editora/(?P<id_editora>\d+)/$', editora),
#	(r'^adiciona_livro$', adiciona_livro),
#	(r'^livro/(?P<id_editora>\d+)/$', livro),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

	)

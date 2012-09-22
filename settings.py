# -*- coding:utf-8 -*-

# Django settings for ConsultaVip project.
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SITE_ID = 1

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS


#ligação com o banco de dados
DATABASE_ENGINE = 'postgresql_psycopg2'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'srm'             # Or path to database file if using sqlite3.
DATABASE_USER = 'postgres'             # Not used with sqlite3.
DATABASE_PASSWORD = 'postgres'         # Not used with sqlite3.
DATABASE_HOST = '127.0.0.1'             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = '5432'             # Set to empty string for default. Not used with sqlite3.

#configuração da conta de email que dispara os emails automaticos do sistema
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'tccfabiofabiano@gmail.com'
EMAIL_HOST_PASSWORD = 'projetofinal'
EMAIL_USE_TLS = True

TIME_ZONE = 'America/Sao_Paulo' #Definição de fuso-horario

LANGUAGE_CODE = 'pt-br' 	#idioma da aplicação

DATE_FORMAT = 'd/m/Y'		#Definição do formato de data
DATETIME_FORMAT = 'd/m/Y H:i'	#Definição do formato de data e hora

USE_I18N = True			#Sistema de internacionalização ativado

MEDIA_ROOT = 'media/'		#Mapeada pasta dos arquivos de media

MEDIA_URL = 'PSD.media'		#Mapeada pasta dos arquivos de media

ADMIN_MEDIA_PREFIX = '/admin_media/'					#Mapeada pasta dos arquivos de media da area de administracao

SECRET_KEY = 'y0ucl2b@waju8-b033g23vi^ybk6y9m%s51&+ow+u-jl8=_940'	#codigo gerado pelo Django ao criar o projeto

TEMPLATE_LOADERS = ( 							#mapeados templates utilizados na area de administracao
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (							#ativados os middlewares para gerenciamento de autenticação dos usuários
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',	
)

ROOT_URLCONF = 'PSD.urls'			#mapeado arquivo das urls do projeto

TEMPLATE_DIRS = (				#mapeada pasta com os templates criados para o projeto
	'templates/',
)

INSTALLED_APPS = (				#lista de aplicações ativas
	'PSD.interno',
	'PSD.relatorios',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
)
LOGIN_URL = '/'					#mapeada url de login no sistema
LOGIN_REDIRECT_URL = '/inicio'			#mapeada url de redirecionamento após o login

from django import template

register = template.Library()

@register.filter(name='multiplicar')
def multiplicar(valor1, valor2):
	return valor1 * valor2

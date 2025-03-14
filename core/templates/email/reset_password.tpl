{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{name}}
{% endblock %}

{% block html %} 
{{token}}
<a href='http://127.0.0.1:8000/accounts/api-v1/activation/{{token.access}}'>click link to activate</a> 
{% endblock %}
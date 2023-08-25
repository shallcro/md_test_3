{# Display description #}
{% if description %}
{% if depth > 0 %}**Description:**{{ " " }}{% endif %}{{ description }}
{% endif %}
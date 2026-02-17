from django import template

register = template.Library()


@register.simple_tag
def commonSkill(skills, jobskills):
    for jskill in jobskills:
        if(jskill in skills):
            return True
    return False
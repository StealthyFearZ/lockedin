from django import template

register = template.Library()


@register.simple_tag
def commonSkill(skills, jobskills):
    st_skills = {skill.strip().lower() for skill in skills if skill.strip()} #ensures match regardless of case sensitivity and spaces
    targets = [skill.strip().lower() for skill in jobskills if skill.strip()]
    return any(skill in st_skills for skill in targets) # same idea as original without need for for loop. Any method ensures first match of True passes through
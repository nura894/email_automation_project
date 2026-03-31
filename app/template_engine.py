def render_template(template, data):
    for key, value in data.items():
        template = template.replace(f"{{{{{key}}}}}", str(value))
    return template

subject_template = "Hello {{name}}"
body_template = "Hi {{name}}, welcome to {{company}}!" 
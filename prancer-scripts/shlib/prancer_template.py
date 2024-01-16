import json
from jinja2 import Environment,FileSystemLoader

def gen_config_file(fname, template, data):
    path = 'shlib/templates'
    env = Environment(loader=FileSystemLoader(path))
    template = env.get_template(template)
    output_from_parsed_template = template.render(**data)
    if fname:
        with open(fname, 'w') as f:
            f.write(output_from_parsed_template)
    return json.loads(output_from_parsed_template)

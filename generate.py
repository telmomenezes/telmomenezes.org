#!/usr/bin/env python
# coding=utf-8


import os
import sys
from string import Template


def page_paths():
    pages = []
    for (dirpath, dirnames, filenames) in os.walk('pages'):
        for filename in filenames:
            pages.append((dirpath, filename))
    return pages


def read_page_file(path):
    with open(path) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    page_values = {}
    key = None
    value_lines = []
    for line in content:
        if len(line) > 0:
            if line[0] == ':':
                if key:
                    page_values[key] = '\n'.join(value_lines)
                    value_lines = []
                key = line[1:]
            else:
                value_lines.append(line)
    if key:
        page_values[key] = '\n'.join(value_lines)
    return page_values


def generate_page(directory, filename, base_dir, propagate_parameters=None):
    path = '%s/%s' % (directory, filename)

    if propagate_parameters:
        parameters = propagate_parameters.copy()
        parameters.pop('template', None)
    else:
        parameters = {}
    parameters.update(read_page_file(path))
    
    parameters['base_dir'] = base_dir
    
    template = Template(parameters['html'])
    if propagate_parameters and 'html' in propagate_parameters:
        parameters['html'] = propagate_parameters['html']
    page_str = template.substitute(parameters)
    parameters['html'] = page_str

    if 'template' in parameters:
        template_filename = '%s.html' % parameters['template']
        page_str = generate_page('templates', template_filename, base_dir, parameters)

    if not propagate_parameters:
        out_dir = '/'.join(['output'] + directory.split('/')[1:])
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        html_filename = '%s.html' % filename.split('.')[0]
        outpath = '%s/%s' % (out_dir, html_filename)
        with open(outpath, 'w') as text_file:
            text_file.write(page_str)

    return page_str


def generate(base_dir):
    print('base_dir is "%s"' % base_dir)
    for page in page_paths():
        print('processing page: %s/%s' % (page[0], page[1]))
        generate_page(page[0], page[1], base_dir)


if __name__ == '__main__':
    base_dir = ''
    if len(sys.argv) > 1:
        base_dir = sys.argv[1]
    generate(base_dir)
    print('done.')

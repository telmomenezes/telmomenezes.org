#!/usr/bin/env python
# coding=utf-8


import os
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


def generate_page(directory, filename):
    path = '%s/%s' % (directory, filename)
    page_values = read_page_file(path)

    with open('templates/main.html') as f:
        template_lines = f.readlines()
    template_str = '\n'.join(template_lines)
    template = Template(template_str)

    page_str = template.substitute(page_values)

    out_dir = '/'.join(['output'] + directory.split('/')[1:])
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    html_filename = '%s.html' % filename.split('.')[0]
    outpath = '%s/%s' % (out_dir, html_filename)
    with open(outpath, 'w') as text_file:
        text_file.write(page_str)


def generate():
    for page in page_paths():
        print('processing page: %s/%s' % (page[0], page[1]))
        generate_page(page[0], page[1])


if __name__ == '__main__':
    generate()
    print('done.')

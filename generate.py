# coding=utf-8


import os


def header(title):
    return """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="favicon.ico">

    <title>%s -- Telmo Menezes</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.min.css" rel="stylesheet">
  </head>

  <body>
    <nav class="navbar navbar-toggleable-md navbar-light bg-faded rounded mb-3">
      <button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <a href="#" class="navbar-left"><img style="max-height:40px" src="images/man.jpg"></a>
      &nbsp;&nbsp;
      <a class="navbar-brand" href="#">Telmo Menezes</a>

      <div class="collapse navbar-collapse" id="navbarsExampleDefault">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Research</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#">Publications</a>
          </li>
        </ul>
      </div>
    </nav>
    <div class="container">
    """ % title


def footer():
    return """
    </div> <!-- /container -->

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://code.jquery.com/jquery-3.1.1.slim.min.js" integrity="sha384-A7FZj7v+d/sdmMqp/nOQwliLvUsJfDHW+k9Omg/a/EheAdgtzNs3hpfag6Ed950n" crossorigin="anonymous"></script>
    <script>window.jQuery || document.write('<script src="js/jquery.min.js"><\/script>')</script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>
    <script src="js/bootstrap.min.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="js/ie10-viewport-bug-workaround.js"></script>
  </body>
</html>
    """


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
    page_parts = (header(page_values['title']), page_values['content'], footer())
    page_str = '\n'.join(page_parts)

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

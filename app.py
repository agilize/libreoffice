#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
    WSGI APP to convert wkhtmltopdf As a webservice
    :copyright: (c) 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import json
import tempfile
import zipfile
from werkzeug.wsgi import wrap_file
from werkzeug.wrappers import Request, Response
from executor import execute


@Request.application
def application(request):
    """
    To use this application, the user must send a POST request with
    base64 or form encoded encoded HTML content and the wkhtmltopdf Options in
    request data, with keys 'base64_html' and 'options'.
    The application will return a response with the PDF file.
    """
    if request.method != 'POST':
        return Response('alive')

    with tempfile.NamedTemporaryFile(suffix='.docx') as source_file:
        # First check if any files were uploaded
        source_file.write(request.files['file'].read())
        # Load any options that may have been provided in options
        options = json.loads(request.form.get('options', '{}'))

        source_file.flush()

        # Evaluate argument to run with subprocess
        args = ['libreoffice', '--headless', '--convert-to', 'pdf', source_file.name, '--outdir', '/tmp']

        # Add Global Options
        if options:
            for option, value in options.items():
                args.append('--%s' % option)

                if value:
                    if value.isdigit():
                        args.append('%s' % value)
                    else:
                        args.append('"%s"' % value)

        # Add source file name and output file name
        file_name = source_file.name
        # args += [file_name, file_name + ".pdf"]

        cmd = ' '.join(args)

        # Execute the command using executor
        print("Executing > " + cmd)
        execute(cmd)

        pdf_file = open(file_name.replace(".docx", ".pdf"))

        return Response(
            wrap_file(request.environ, pdf_file),
            mimetype='application/pdf',
            direct_passthrough=True,
        )


if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple(
        '127.0.0.1', 5000, application, use_debugger=True, use_reloader=True
    )
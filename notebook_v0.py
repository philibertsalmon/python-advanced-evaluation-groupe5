#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
starter code for your evaluation assignment
"""

# Python Standard Library
import base64
import io
import json
import pprint
from typing_extensions import Concatenate

# Third-Party Libraries
import numpy as np
import PIL.Image  # pillow


def load_ipynb(filename) -> dict:
    r"""
    Load a jupyter notebook .ipynb file (JSON) as a Python dict.

    Usage:

        >>> ipynb = load_ipynb("samples/minimal.ipynb")
        >>> ipynb
        {'cells': [], 'metadata': {}, 'nbformat': 4, 'nbformat_minor': 5}

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> pprint.pprint(ipynb)
        {'cells': [{'cell_type': 'markdown',
                    'id': 'a9541506',
                    'metadata': {},
                    'source': ['Hello world!\n',
                               '============\n',
                               'Print `Hello world!`:']},
                   {'cell_type': 'code',
                    'execution_count': 1,
                    'id': 'b777420a',
                    'metadata': {},
                    'outputs': [{'name': 'stdout',
                                 'output_type': 'stream',
                                 'text': ['Hello world!\n']}],
                    'source': ['print("Hello world!")']},
                   {'cell_type': 'markdown',
                    'id': 'a23ab5ac',
                    'metadata': {},
                    'source': ['Goodbye! 👋']}],
         'metadata': {},
         'nbformat': 4,
         'nbformat_minor': 5}
    """
    # On ouvre le fichier puis on le converit en dict python avec la fonction json.load()->dict
    with open(filename) as f: 
        return json.load(f)


def save_ipynb(ipynb, filename):
    r"""
    Save a jupyter notebook (Python dict) as a .ipynb file (JSON)

    Usage:

        >>> ipynb = load_ipynb("samples/minimal.ipynb")
        >>> ipynb
        {'cells': [], 'metadata': {}, 'nbformat': 4, 'nbformat_minor': 5}
        >>> ipynb["metadata"]["clone"] = True
        >>> save_ipynb(ipynb, "samples/minimal-save-load.ipynb")
        >>> load_ipynb("samples/minimal-save-load.ipynb")
        {'cells': [], 'metadata': {'clone': True}, 'nbformat': 4, 'nbformat_minor': 5}

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> save_ipynb(ipynb, "samples/hello-world-save-load.ipynb")
        >>> ipynb == load_ipynb("samples/hello-world-save-load.ipynb")
        True

    """
    # Mettre 'a' en argument de open() permet de créer un nouveau fichier, dans lequel on écrit le code au format JSON avec la fonction json.dumps().
    with open(filename, 'a') as f:
        f.write(json.dumps(ipynb))


def get_format_version(ipynb):
    r"""
    Return the format version (str) of a jupyter notebook (dict).

    Usage:

        >>> ipynb = load_ipynb("samples/minimal.ipynb")
        >>> get_format_version(ipynb)
        '4.5'

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> get_format_version(ipynb)
        '4.5'
    """
    # La version et la sous-version sont stockées dans le dictionnaire ipynb représentant le notebook. Elles correspondent respectivement aux clefs 'nbformat' et 'nbformat_minor'.
    return f"{ipynb['nbformat']}.{ipynb['nbformat_minor']}"


def get_metadata(ipynb):
    r"""
    Return the global metadata of a notebook.

    Usage:

        >>> ipynb = load_ipynb("samples/metadata.ipynb")
        >>> metadata = get_metadata(ipynb)
        >>> pprint.pprint(metadata)
        {'celltoolbar': 'Edit Metadata',
         'kernelspec': {'display_name': 'Python 3 (ipykernel)',
                        'language': 'python',
                        'name': 'python3'},
         'language_info': {'codemirror_mode': {'name': 'ipython', 'version': 3},
                           'file_extension': '.py',
                           'mimetype': 'text/x-python',
                           'name': 'python',
                           'nbconvert_exporter': 'python',
                           'pygments_lexer': 'ipython3',
                           'version': '3.9.7'}}
    """
    # Les metdata sont stockées dans le dictionnaire représentant le Notebook. Elles correspondent à la clef 'metadata'.
    return ipynb['metadata']


def get_cells(ipynb):
    r"""
    Return the notebook cells.

    Usage:

        >>> ipynb = load_ipynb("samples/minimal.ipynb")
        >>> cells = get_cells(ipynb)
        >>> cells
        []

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> cells = get_cells(ipynb)
        >>> pprint.pprint(cells)
        [{'cell_type': 'markdown',
          'id': 'a9541506',
          'metadata': {},
          'source': ['Hello world!\n', '============\n', 'Print `Hello world!`:']},
         {'cell_type': 'code',
          'execution_count': 1,
          'id': 'b777420a',
          'metadata': {},
          'outputs': [{'name': 'stdout',
                       'output_type': 'stream',
                       'text': ['Hello world!\n']}],
          'source': ['print("Hello world!")']},
         {'cell_type': 'markdown',
          'id': 'a23ab5ac',
          'metadata': {},
          'source': ['Goodbye! 👋']}]
    """
    # Les cellules sont stockées dans le dictionnaire représentant le Notebook. Elles correspondent à la clef 'cells'. La fonction get_cells() renvoie une liste de cellules, donc une list de dict.
    return ipynb['cells']


def to_percent(ipynb):
    r"""
    Convert a ipynb notebook (dict) to a Python code in the percent format (str).

    Usage:

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> print(to_percent(ipynb)) # doctest: +NORMALIZE_WHITESPACE
        # %% [markdown]
        # Hello world!
        # ============
        # Print `Hello world!`:
        # %%
        print("Hello world!")
        # %% [markdown]
        # Goodbye! 👋

        >>> notebook_files = Path(".").glob("samples/*.ipynb")
        >>> for notebook_file in notebook_files:
        ...     ipynb = load_ipynb(notebook_file)
        ...     percent_code = to_percent(ipynb)
        ...     with open(notebook_file.with_suffix(".py"), "w", encoding="utf-8") as output:
        ...         print(percent_code, file=output)
    """
    # En lisant les notebooks donnés en exemple, on comprend les règles d'écritures que l'on reproduit.
    text = ""
    cells = get_cells(ipynb)
    # On bâtit le texte cellule par cellule.
    for cell in cells:
        cell_type = cell['cell_type'] # On cherche le type de la cellule...
        markdown = cell_type == 'markdown' # ... que l'on stocke dans un booléen.
        text += '# %% [markdown]\n' if markdown else '# %%\n' # Chaque cellule possède un début, selon son type.
        for line in cell['source']: # Puis on construit ligne par ligne.
            text += '# ' if markdown else '' # Début de la ligne suivant le type.
            text += line # Ajout de la ligne
        text += '\n\n' # Saut caractéristique de la fin de cellule.
    return text[:-1] # On coupe le dernier saut de la dernière cellule : le code doit se terminer par un unique saut de ligne.


def starboard_html(code):
    return f"""
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Starboard Notebook</title>
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <link rel="icon" href="https://cdn.jsdelivr.net/npm/starboard-notebook@0.15.2/dist/favicon.ico">
        <link href="https://cdn.jsdelivr.net/npm/starboard-notebook@0.15.2/dist/starboard-notebook.css" rel="stylesheet">
    </head>
    <body>
        <script>
            window.initialNotebookContent = {code!r}
            window.starboardArtifactsUrl = `https://cdn.jsdelivr.net/npm/starboard-notebook@0.15.2/dist/`;
        </script>
        <script src="https://cdn.jsdelivr.net/npm/starboard-notebook@0.15.2/dist/starboard-notebook.js"></script>
    </body>
</html>
"""


def to_starboard(ipynb, html=False):
    r"""
    Convert a ipynb notebook (dict) to a Starboard notebook (str)
    or to a Starboard HTML document (str) if html is True.

    Usage:

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> print(to_starboard(ipynb))
        # %% [markdown]
        Hello world!
        ============
        Print `Hello world!`:
        # %% [python]
        print("Hello world!")
        # %% [markdown]
        Goodbye! 👋

        >>> html = to_starboard(ipynb, html=True)
        >>> print(html) # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        <!doctype html>
        <html>
        ...
        </html>

        >>> notebook_files = Path(".").glob("samples/*.ipynb")
        >>> for notebook_file in notebook_files:
        ...     ipynb = load_ipynb(notebook_file)
        ...     starboard_html = to_starboard(ipynb, html=True)
        ...     with open(notebook_file.with_suffix(".html"), "w", encoding="utf-8") as output:
        ...         print(starboard_html, file=output)
    """
    text = ""
    cells = get_cells(ipynb)
    for cell in cells:
        ismarkdown = cell['cell_type'] == 'markdown'
        text += '# %% [markdown]\n' if ismarkdown else '# %% [python]\n'
        for line in cell["source"]:
            text += line
        text += '\n'
    return starboard_html(text[:-1]) if html else text[:-1]

# Outputs
# ------------------------------------------------------------------------------
def clear_outputs(ipynb):
    r"""
    Remove the notebook cell outputs and resets the cells execution counts.

    Usage:

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> pprint.pprint(ipynb)
        {'cells': [{'cell_type': 'markdown',
                    'id': 'a9541506',
                    'metadata': {},
                    'source': ['Hello world!\n',
                               '============\n',
                               'Print `Hello world!`:']},
                   {'cell_type': 'code',
                    'execution_count': 1,
                    'id': 'b777420a',
                    'metadata': {},
                    'outputs': [{'name': 'stdout',
                                 'output_type': 'stream',
                                 'text': ['Hello world!\n']}],
                    'source': ['print("Hello world!")']},
                   {'cell_type': 'markdown',
                    'id': 'a23ab5ac',
                    'metadata': {},
                    'source': ['Goodbye! 👋']}],
         'metadata': {},
         'nbformat': 4,
         'nbformat_minor': 5}
        >>> clear_outputs(ipynb)
        >>> pprint.pprint(ipynb)
        {'cells': [{'cell_type': 'markdown',
                    'id': 'a9541506',
                    'metadata': {},
                    'source': ['Hello world!\n',
                               '============\n',
                               'Print `Hello world!`:']},
                   {'cell_type': 'code',
                    'execution_count': None,
                    'id': 'b777420a',
                    'metadata': {},
                    'outputs': [],
                    'source': ['print("Hello world!")']},
                   {'cell_type': 'markdown',
                    'id': 'a23ab5ac',
                    'metadata': {},
                    'source': ['Goodbye! 👋']}],
         'metadata': {},
         'nbformat': 4,
         'nbformat_minor': 5}
    """
    for cell in ipynb['cells']:
        if cell['cell_type'] == 'code':
            cell['execution_count'] = None
            cell['outputs'] = []


def get_stream(ipynb, stdout=True, stderr=False):
    r"""
    Return the text written to the standard output and/or error stream.

    Usage:

        >>> ipynb = load_ipynb("samples/streams.ipynb")
        >>> print(get_stream(ipynb)) # doctest: +NORMALIZE_WHITESPACE
        👋 Hello world! 🌍
        >>> print(get_stream(ipynb, stdout=False, stderr=True)) # doctest: +NORMALIZE_WHITESPACE
        🔥 This is fine. 🔥 (https://gunshowcomic.com/648)
        >>> print(get_stream(ipynb, stdout=True, stderr=True)) # doctest: +NORMALIZE_WHITESPACE
        👋 Hello world! 🌍
        🔥 This is fine. 🔥 (https://gunshowcomic.com/648)
    """
    text = ""
    for cell in get_cells(ipynb):
        if cell['cell_type'] == 'code':
            for output in cell['outputs']:
                if stdout and output['name'] == 'stdout':
                    text += ''.join(output['text'])
                elif stderr and output['name'] == 'stderr':
                    text += ''.join(output['text'])
    return text
            


def get_exceptions(ipynb):
    r"""
    Return all exceptions raised during cell executions.

    Usage:

        >>> ipynb = load_ipynb("samples/hello-world.ipynb")
        >>> get_exceptions(ipynb)
        []

        >>> ipynb = load_ipynb("samples/errors.ipynb")
        >>> errors = get_exceptions(ipynb)
        >>> all(isinstance(error, Exception) for error in errors)
        True
        >>> for error in errors:
        ...     print(repr(error))
        TypeError("unsupported operand type(s) for +: 'int' and 'str'")
        Warning('🌧️  light rain')
    """
    errors = []
    # On crée une sous-classe de Exception afin de choisir la représentation de error qui nous arrange.
    class MyError(Exception):
        def __init__(self, ename, evalue):
            self.ename = ename
            self.evalue = evalue
        
        def __repr__(self):
            return self.ename + "(" + repr(self.evalue) + ")"

    for cell in get_cells(ipynb):
        if cell['cell_type'] == 'code':
            for output in cell['outputs']:
                if output['output_type'] == 'error':
                    errors.append(MyError(output['ename'],output['evalue']))
    return errors


def get_images(ipynb):
    r"""
    Return the PNG images contained in a notebook cells outputs
    (as a list of NumPy arrays).

    Usage:

        >>> ipynb = load_ipynb("samples/images.ipynb")
        >>> images = get_images(ipynb)
        >>> images # doctest: +ELLIPSIS
        [array([[[ ...]]], dtype=uint8)]
        >>> grace_hopper_image = images[0]
        >>> np.shape(grace_hopper_image)
        (600, 512, 3)
        >>> grace_hopper_image # doctest: +ELLIPSIS
        array([[[ 21,  24,  77],
                [ 27,  30,  85],
                [ 33,  35,  92],
                ...,
                [ 14,  13,  19]]], dtype=uint8)
    """
    pass

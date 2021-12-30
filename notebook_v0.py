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


def load_ipynb(filename: str) -> dict:
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
    # On ouvre le fichier puis on le convertit en dict python avec la fonction json.load()->dict
    with open(filename) as f: 
        return json.load(f)


def save_ipynb(ipynb, filename: str):
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


def get_format_version(ipynb: dict) -> str:
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
    # La version et la sous-version sont stockées dans le dictionnaire `ipynb` représentant le notebook. Elles correspondent respectivement aux clefs 'nbformat' et 'nbformat_minor'.
    return f"{ipynb['nbformat']}.{ipynb['nbformat_minor']}"


def get_metadata(ipynb: dict) -> dict:
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
    # Les metdata sont stockées dans le dictionnaire représentant le notebook. Elles correspondent à la clef 'metadata'.
    return ipynb['metadata']


def get_cells(ipynb: dict) -> list:
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
    # Les cellules sont stockées dans le dictionnaire représentant le notebook. Elles correspondent à la clef `cells`. La fonction `get_cells()` renvoie une liste de cellules, donc une `list` de `dict`.
    return ipynb['cells']


def to_percent(ipynb: dict) -> str:
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
    # En lisant les notebooks donnés en exemple, on comprend les règles d'écriture, que l'on reproduit  ici.
    text = ""
    cells = get_cells(ipynb)
    # On bâtit le texte cellule par cellule. On le stocke dans `text`.
    for cell in cells:
        cell_type = cell['cell_type'] # On cherche le type de la cellule...
        markdown = cell_type == 'markdown' # ... que l'on stocke dans un booléen.
        text += '# %% [markdown]\n' if markdown else '# %%\n' # Chaque cellule possède un début, selon son type.
        for line in cell['source']: # Puis on construit ligne par ligne, l'information étant stockée à la clef `source`.
            text += '# ' if markdown else '' # Début de la ligne suivant le type.
            text += line # Ajout de la ligne.
        text += '\n\n' # Saut de ligne, caractéristique de la fin de cellule.
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


def to_starboard(ipynb: dict, html=False):
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
    # D'après les indications, on comprend sur un exemple la structure du texte à implémenter dans le format demandé.
    # La démarche est sensiblement la même que dans la fonction `to_percent`, à des détails de mise en forme (retour à la ligne, début de cellule, début de ligne...) près. On ne précisera pas dans le détail la démarche, qui reste quasiment identique.
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
def clear_outputs(ipynb: dict):
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
    # On va chercher, dans les `dict` représentant les cellules, les clefs `execution_count` et `output`, que l'on réinitialise.
    for cell in ipynb['cells']:
        if cell['cell_type'] == 'code':
            cell['execution_count'] = None
            cell['outputs'] = []


def get_stream(ipynb: dict, stdout=True, stderr=False) -> str:
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
    # On parcourt les cellules à la recherche des différentes `outputs`.
    text = ""
    for cell in get_cells(ipynb):
        if cell['cell_type'] == 'code': # Les outputs ne sont présentes que dans des cellules de code.
            for output in cell['outputs']:
                if stdout and output['name'] == 'stdout': # Ces deux tests (1) selectionnent le genre d'output voulu.
                    text += ''.join(output['text'])
                elif stderr and output['name'] == 'stderr': # (2)
                    text += ''.join(output['text'])
    return text
            


def get_exceptions(ipynb: dict) -> list:
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
    # On crée une sous-classe de `Exception` afin de pouvoir choisir par la suite la représentation de `error` qui nous arrange.
    class MyError(Exception):
        def __init__(self, ename, evalue):
            self.ename = ename
            self.evalue = evalue
        
        def __repr__(self):
            return self.ename + "(" + repr(self.evalue) + ")" # On implémente ici la représentation exigée par l'énoncé.

    # Parcourons désormais les cellules à la recherche des erreurs.
    for cell in get_cells(ipynb):
        if cell['cell_type'] == 'code': # Les erreurs ne concernent que les cellules de code.
            for output in cell['outputs']:
                if output['output_type'] == 'error': # Les erreurs sont un type d'output.
                    errors.append(MyError(output['ename'], output['evalue'])) # Notre programme doit renvoyer une `list` de `Exception`. Passer par la sous-classse `MyError` permet de choisir la représentation.
    return errors


def get_images(ipynb: dict) -> list:
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
    # La donnée des images est stockées dans la cellule qui affiche l'image, dans "outputs" puis "data" puis "image/png". Elle est encodée en hexadécimal. Il s'agit donc de récupérer cette `string` d'hexadécimal et de la convertir. On se sert du module base64.
    images = []
    for cell in get_cells(ipynb):
        if cell["cell_type"] == "code" :
            for output in cell["outputs"]:
                if "image/png" in output["data"]:
                    # On a trouvé un image.
                    imagestr = output["data"]["image/png"] # On la sauvegarde au format héxadécimal.
                    image_PIL = PIL.Image.open(io.BytesIO(base64.b64decode(imagestr))) # Puis on crée l'image, avec le module PIL, en prenant soin de décoder l'hexadécimal (par le module base64).
                    image_array = np.array(image_PIL, dtype=np.uint8) # On convertit notre PIL en array numpy.
                    images.append(image_array) # Finalement on ajoute notre array à la liste.
    return images

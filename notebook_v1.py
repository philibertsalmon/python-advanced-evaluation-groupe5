#!/usr/bin/env python
# -*- coding: utf-8 -*-

import notebook_v0 as n0
import json

"""
an object-oriented version of the notebook toolbox
"""

class Cell:
    r"""A Cell i a Jupyter notebook.

    Args :
        ipynb (dict): a dictionary representing the cell in a Jupyter Notebook.
    
    Attributes:
        id (int): the cell's id.
        source (list): the cell's source code, as a list of str.
    """
    # On suit les exigences de la docstring.
    def __init__(self, ipynb: dict):
        self.id = ipynb["id"]
        self.source = ipynb["source"]
        

class CodeCell(Cell): 
    r"""A Cell of Python code in a Jupyter notebook.

    Args:
        ipynb (dict): a dictionary representing the cell in a Jupyter Notebook.

    Attributes:
        id (int): the cell's id.
        source (list): the cell's source code, as a list of str.
        execution_count (int): number of times the cell has been executed.

    Usage:

        >>> code_cell = CodeCell({
        ...     "cell_type": "code",
        ...     "execution_count": 1,
        ...     "id": "b777420a",
        ...     'source': ['print("Hello world!")']
        ... })
        >>> code_cell.id
        'b777420a'
        >>> code_cell.execution_count
        1
        >>> code_cell.source
        ['print("Hello world!")']
    """

    # `CodeCell` (et identiquement `MarkdownCell` ci-dessous) est developpée comme une sous classe de `Cell`.
    def __init__(self, ipynb: dict):
        super().__init__(ipynb) # On initinialise grâce à la super-classe.
        self.execution_count = ipynb['execution_count'] # Reste à rajouter la spécificité d'une cellule de code.

class MarkdownCell(Cell):
    r"""A Cell of Markdown markup in a Jupyter notebook.

    Args:
        ipynb (dict): a dictionary representing the cell in a Jupyter Notebook.

    Attributes:
        id (int): the cell's id.
        source (list): the cell's source code, as a list of str.

    Usage:

        >>> markdown_cell = MarkdownCell({
        ...    "cell_type": "markdown",
        ...    "id": "a9541506",
        ...    "source": [
        ...        "Hello world!\n",
        ...        "============\n",
        ...        "Print `Hello world!`:"
        ...    ]
        ... })
        >>> markdown_cell.id
        'a9541506'
        >>> markdown_cell.source
        ['Hello world!\n', '============\n', 'Print `Hello world!`:']
    """

    # Idem que pour `CodeCell`.
    def __init__(self, ipynb: dict):
        super().__init__(ipynb)

class Notebook:
    r"""A Jupyter Notebook.

    Args:
        ipynb (dict): a dictionary representing a Jupyter Notebook.

    Attributes:
        version (str): the version of the notebook format.
        cells (list): a list of cells (either CodeCell or MarkdownCell).

    Usage:

        - checking the verion number:

            >>> ipynb = toolbox.load_ipynb("samples/minimal.ipynb")
            >>> nb = Notebook(ipynb)
            >>> nb.version
            '4.5'

        - checking the type of the notebook parts:

            >>> ipynb = toolbox.load_ipynb("samples/hello-world.ipynb")
            >>> nb = Notebook(ipynb)
            >>> isinstance(nb.cells, list)
            True
            >>> isinstance(nb.cells[0], Cell)
            True
    """
    def __init__(self, ipynb: dict):
        self.version = n0.get_format_version(ipynb) # On récupère la version à partir du `dict`, grâce à la fonction développée dans le notebook v0.
        self.cells = [MarkdownCell(cell) if cell['cell_type'] == 'markdown' else CodeCell(cell) for cell in n0.get_cells(ipynb)]
        # Il s'agit ici de créer une `list` de `Cell`.

    @staticmethod
    def from_file(filename):
        r"""Loads a notebook from an .ipynb file.

        Usage:

            >>> nb = Notebook.from_file("samples/minimal.ipynb")
            >>> nb.version
            '4.5'
        """
        # On s'appuie sur une fonction développée dans le notebook v0, qui renvoie le dictionnaire ipynb d'un notebook, à partir du nom du fichier.
        return Notebook(n0.load_ipynb(filename))

    def __iter__(self):
        r"""Iterate the cells of the notebook.

        Usage:

            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> for cell in nb:
            ...     print(cell.id)
            a9541506
            b777420a
            a23ab5ac
        """
        # On itère les cellules.
        return iter(self.cells)

class PyPercentSerializer:
    r"""Prints a given Notebook in py-percent format.

    Args:
        notebook (Notebook): the notebook to print.

    Usage:
            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> ppp = PyPercentSerializer(nb)
            >>> print(ppp.to_py_percent()) # doctest: +NORMALIZE_WHITESPACE
            # %% [markdown]
            # Hello world!
            # ============
            # Print `Hello world!`:
            <BLANKLINE>
            # %%
            print("Hello world!")
            <BLANKLINE>
            # %% [markdown]
            # Goodbye! 👋
    """
    def __init__(self, notebook: Notebook):
        self.notebook = notebook

    def to_py_percent(self) -> str:
        r"""Converts the notebook to a string in py-percent format.
        """
        # L'idée de cette fonction est la même que celle du notebook v0. La différence réside dans le fait qu'on ne va pas chercher les informations au même endroit.
        text = ""
        for cell in self.notebook:
            if isinstance(cell, MarkdownCell): # Le type de cellule (code ou markdown) n'est plus dans le dictionnaire `ipynb`, mais est contenu dans le `type` de la cellule.
                text += "# %% [markdown]\n# "
                text += '# '.join(cell.source) # Le contenu de la cellule n'est plus non plus dans le dictionnaire, mais en argument de la `cell:Cell`.
                text += "\n\n"
            if isinstance(cell, CodeCell):
                text += "# %%\n"
                text += ''.join(cell.source) 
                text += "\n\n"
        return text[:-2] # On supprime les deux derniers sauts de ligne pour satisfaire la convention.

    def to_file(self, filename):
        r"""Serializes the notebook to a file

        Args:
            filename (str): the name of the file to write to.

        Usage:

                >>> nb = Notebook.from_file("samples/hello-world.ipynb")
                >>> s = PyPercentSerializer(nb)
                >>> s.to_file("samples/hello-world-serialized-py-percent.py")
        """
        # Il s'agit de l'écriture classique d'un fichier.
        with open(filename, 'a') as f:
            f.write(self.to_py_percent())

class Serializer:
    r"""Serializes a Jupyter Notebook to a file.

    Args:
        notebook (Notebook): the notebook to print.

    Usage:

        >>> nb = Notebook.from_file("samples/hello-world.ipynb")
        >>> s = Serializer(nb)
        >>> pprint.pprint(s.serialize())  # doctest: +NORMALIZE_WHITESPACE
            {'cells': [{'cell_type': 'markdown',
                'id': 'a9541506',
                'medatada': {},
                'source': ['Hello world!\n',
                           '============\n',
                           'Print `Hello world!`:']},
               {'cell_type': 'code',
                'execution_count': 1,
                'id': 'b777420a',
                'medatada': {},
                'outputs': [],
                'source': ['print("Hello world!")']},
               {'cell_type': 'markdown',
                'id': 'a23ab5ac',
                'medatada': {},
                'source': ['Goodbye! 👋']}],
            'metadata': {},
            'nbformat': 4,
            'nbformat_minor': 5}
        >>> s.to_file("samples/hello-world-serialized.ipynb")
    """

    def __init__(self, notebook: Notebook):
        self.notebook = notebook

    def serialize(self) -> dict:
        r"""Serializes the notebook to a JSON object

        Returns:
            dict: a dictionary representing the notebook.
        """
        # Créons un squelette de JSON vide.
        ipynb = {
            'cells': [],
            'metadata' : {},
            'nbformat' : None,
            'nbformat_minor' : None}
        # Remplissons la clef `cells` en parcourant les `Cells` du `Notebook`.
        for cell in self.notebook:
            cell_notebook = {} # Cellule vide à ajouter.
            cell_notebook['cell_type'] = 'code' if isinstance(cell, CodeCell) else 'markdown' # On récupère le type de la cellule.
            if isinstance(cell, CodeCell):
                cell_notebook['execution_count'] = cell.execution_count # On rajoute la spécificité des cellules de code.
            cell_notebook['id'] = cell.id # Puis l'indice, stocké comme argument de la `Cell`.
            cell_notebook['metadata'] = {} # On ajoute des metadata vides.
            cell_notebook['source'] = cell.source # On récupère la source, stockée en argument.
            ipynb['cells'].append(cell_notebook) # Puis on ajoute la cellule à la liste de cellules.
        # Reste à récupérer les versions.
        version = self.notebook.version.split('.')
        ipynb['nbformat'] = int(version[0])
        ipynb['nbformat_minor'] = int(version[1])
        return ipynb

    def to_file(self, filename):
        r"""Serializes the notebook to a file

        Args:
            filename (str): the name of the file to write to.

        Usage:

                >>> nb = Notebook.from_file("samples/hello-world.ipynb")
                >>> s = Serializer(nb)
                >>> s.to_file("samples/hello-world-serialized.ipynb")
                >>> nb = Notebook.from_file("samples/hello-world-serialized.ipynb")
                >>> for cell in nb:
                ...     print(cell.id)
                a9541506
                b777420a
                a23ab5ac
        """
        with open(filename, 'a') as f:
            f.write(self.serialize)

class Outliner:
    r"""Quickly outlines the strucure of the notebook in a readable format.

    Args:
        notebook (Notebook): the notebook to outline.

    Usage:

            >>> nb = Notebook.from_file("samples/hello-world.ipynb")
            >>> o = Outliner(nb)
            >>> print(o.outline()) # doctest: +NORMALIZE_WHITESPACE
                Jupyter Notebook v4.5
                └─▶ Markdown cell #a9541506
                    ┌  Hello world!
                    │  ============
                    └  Print `Hello world!`:
                └─▶ Code cell #b777420a (1)
                    | print("Hello world!")
                └─▶ Markdown cell #a23ab5ac
                    | Goodbye! 👋
    """
    def __init__(self, notebook: Notebook):
        self.notebook = notebook

    def outline(self) -> str:
        r"""Outlines the notebook in a readable format.

        Returns:
            str: a string representing the outline of the notebook.
        """
        # Comme pour les autres fonctions similaires développées plus haut, on construit pas à pas la chaîne de caractères, en suivant l'exemple.
        text = f"Jupyter Notebook v{self.notebook.version}" # Début
        for cell in self.notebook: # On construit cellule par cellule.
            text += "\n└─▶ " # Début de cellule
            text += f"Markdown cell #{cell.id}\n" if isinstance(cell, MarkdownCell) else f"Code cell #{cell.id} ({cell.execution_count})\n" # Début  de la cellule, selon le type.
            # On doit ajouter les signes |, ┌ et └. Pour cela, il faut discriminer les cellule selon leur longueur.
            if len(cell.source) == 1:
                text += f"    | {cell.source[0]}"
            else :
                text += f"    ┌  {cell.source[0]}"
                for middle_line in cell.source[1:-1]:
                    text += f"    │  {middle_line}"
                text += f"    └  {cell.source[-1]}"
        return text
        
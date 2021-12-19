#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
an object-oriented version of the notebook toolbox
"""

import notebook_v0 as n0

class Cell():
    r"""A Cell in a Jupyter notebbok.

    Args :
    id (str): The unique ID of the cell.
    source (list): The source code of the cell, as a list of str.
    """

    def __init__(self, id, source):
        self.id = id
        self.source = source

# On crée les classes CodeCell et MarkdownCell comme des sous-classes de Cell

class CodeCell(Cell):
    r"""A Cell of Python code in a Jupyter notebook.

    Args:
        id (str): The unique ID of the cell.
        source (list): The source code of the cell, as a list of str.
        execution_count (int): The execution count of the cell.

    Attributes:
        id (str): The unique ID of the cell.
        source (list): The source code of the cell, as a list of str.
        execution_count (int): The execution count of the cell.

    Usage:

        >>> code_cell = CodeCell("b777420a", ['print("Hello world!")'], 1)
        ... })
        >>> code_cell.id
        'b777420a'
        >>> code_cell.execution_count
        1
        >>> code_cell.source
        ['print("Hello world!")']
    """
    def __init__(self, id, source, execution_count):
        super().__init__(id, source) # On intialise avec la super-classe...
        self.execution_count = execution_count #... et on complète par l'info spécifique à une cellule de code.

class MarkdownCell(Cell):
    r"""A Cell of Markdown markup in a Jupyter notebook.

    Args:
        id (str): The unique ID of the cell.
        source (list): The source code of the cell, as a list of str.

    Attributes:
        id (str): The unique ID of the cell.
        source (list): The source code of the cell, as a list of str.

    Usage:

        >>> markdown_cell = MarkdownCell("a9541506", [
        ...     "Hello world!",
        ...     "============",
        ...     "Print `Hello world!`:"
        ... ])
        >>> markdown_cell.id
        'a9541506'
        >>> markdown_cell.source
        ['Hello world!', '============', 'Print `Hello world!`:']
    """
    def __init__(self, id, source):
        super().__init__(id, source) # Idem : on initialise avec la super-classe.

class Notebook:
    r"""A Jupyter Notebook

    Args:
        version (str): The version of the notebook format.
        cells (list): The cells of the notebook (either CodeCell or MarkdownCell).

    Attributes:
        version (str): The version of the notebook format.
        cells (list): The cells of the notebook (either CodeCell or MarkdownCell).

    Usage:

        >>> version = "4.5"
        >>> cells = [
        ...     MarkdownCell("a9541506", [
        ...         "Hello world!",
        ...         "============",
        ...         "Print `Hello world!`:"
        ...     ]),
        ...     CodeCell("b777420a", ['print("Hello world!")'], 1),
        ... ]
        >>> nb = Notebook(version, cells)
        >>> nb.version
        '4.5'
        >>> isinstance(nb.cells, list)
        True
        >>> isinstance(nb.cells[0], MarkdownCell)
        True
        >>> isinstance(nb.cells[1], CodeCell)
        True
    """

    def __init__(self, version: str, cells: list): # cells est une list de Cells
        self.version = version
        self.cells = cells
    
    def __iter__(self):
        r"""Iterate the cells of the notebook.
        """
        return iter(self.cells)

class NotebookLoader:
    r"""Loads a Jupyter Notebook from a file

    Args:
        filename (str): The name of the file to load.

    Usage:
            >>> nbl = NotebookLoader("samples/hello-world.ipynb")
            >>> nb = nbl.load()
            >>> nb.version
            '4.5'
            >>> for cell in nb:
            ...     print(cell.id)
            a9541506
            b777420a
            a23ab5ac
    """
    def __init__(self, filename: str):
        self.filename = filename

    def load(self):
        r"""Loads a Notebook instance from the file.
        """
        # Il faut construire un Notebook. On doit récupérer les deux argument suivants :
        # 1 : la version
        ipynb = n0.load_ipynb(self.filename)
        nb_version = n0.get_format_version(ipynb) #où l'on se ressert de fonctions développées dans le notebook 0.
        # 2 : la list cells des Cells du futur Notebook.
        # On construit donc une à une les Cell en parcourant la liste fournie par la fonction n0.get_cells.
        # Cela revient à convertir les cellules du format dict au format Cell.
        nb_cells = [CodeCell(cell["id"], cell["source"], cell["execution_count"]) if cell["cell_type"] == "code" else MarkdownCell(cell["id"], cell["source"]) for cell in n0.get_cells(ipynb)]
        return Notebook(nb_version, nb_cells)

class Markdownizer:
    r"""Transforms a notebook to a pure markdown notebook.

    Args:
        notebook (Notebook): The notebook to transform.

    Usage:

        >>> nb = NotebookLoader("samples/hello-world.ipynb").load()
        >>> nb2 = Markdownizer(nb).markdownize()
        >>> nb2.version
        '4.5'
        >>> for cell in nb2:
        ...     print(cell.id)
        a9541506
        b777420a
        a23ab5ac
        >>> isinstance(nb2.cells[1], MarkdownCell)
        True
        >>> Serializer(nb2).to_file("samples/hello-world-markdown.ipynb")
    """

    def __init__(self, notebook):
        self.notebook = notebook

    def markdownize(self):
        r"""Transforms the notebook to a pure markdown notebook.
        """
        # On va parcourir les cellules du notebook et changer celles du type CodeCell en MarkdownCell
        new_cells = []
        for cell in self.notebook:
            if isinstance(cell, CodeCell):
                # Il faut encadrer le texte source :
                new_source = ["```python\n"] + cell.source + ["\n```"]
                new_cell = MarkdownCell(cell.id, new_source)
            else:
                # Sinon, on ne change rien
                new_cell = cell
            new_cells.append(new_cell)
        return Notebook(self.notebook.version, new_cells)

class MarkdownLesser:
    r"""Removes markdown cells from a notebook.

    Args:
        notebook (Notebook): The notebook to transform.

    Usage:

            >>> nb = NotebookLoader("samples/hello-world.ipynb").load()
            >>> nb2 = MarkdownLesser(nb).remove_markdown_cells()
            >>> print(Outliner(nb2).outline())
            Jupyter Notebook v4.5
            └─▶ Code cell #b777420a (1)
                | print("Hello world!")
    """
    def __init__(self, notebook):
        self.notebook = notebook

    def remove_markdown_cells(self):
        r"""Removes markdown cells from the notebook.

        Returns:
            Notebook: a Notebook instance with only code cells
        """
        # On procède de la même manière que pour Mardownizer
        new_cells = []
        for cell in self.notebook:
            if not isinstance(cell, MarkdownCell):
                new_cells.append(cell)
        return Notebook(self.notebook.version, new_cells)


class PyPercentLoader:
    r"""Loads a Jupyter Notebook from a py-percent file.

    Args:
        filename (str): The name of the file to load.
        version (str): The version of the notebook format (defaults to '4.5').

    Usage:

            >>> # Step 1 - Load the notebook and save it as a py-percent file
            >>> nb = NotebookLoader("samples/hello-world.ipynb").load()
            >>> PyPercentSerializer(nb).to_file("samples/hello-world-py-percent.py")
            >>> # Step 2 - Load the py-percent file
            >>> nb2 = PyPercentLoader("samples/hello-world-py-percent.py").load()
            >>> nb.version
            '4.5'
            >>> for cell in nb:
            ...     print(cell.id)
            a9541506
            b777420a
            a23ab5ac
    """

    def __init__(self, filename, version="4.5"):
        self.filename = filename
        self.version = version

    def load(self):
        r"""Loads a Notebook instance from the py-percent file.
        """
        pass

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from notebook_v1 import *

class Question9(unittest.TestCase):
    def test_build_code_cell(self):
        code_cell = CodeCell({
             "cell_type": "code",
             "execution_count": 1,
             "id": "b777420a",
             'source': ['print("Hello world!")']
         })
        self.assertEqual('b777420a', code_cell.id)
        self.assertEqual(1, code_cell.execution_count)
        self.assertEqual(
        ['print("Hello world!")']
            , code_cell.source)

    def test_build_markdown_cell(self):
        markdown_cell = MarkdownCell({
             "cell_type": "markdown",
             "id": "a9541506",
            "source": [
                "Hello world!\n",
                "============\n",
                "Print `Hello world!`:"
            ]
         })
        self.assertEqual('a9541506', markdown_cell.id)
        self.assertEqual(
        ['Hello world!\n', '============\n', 'Print `Hello world!`:'],
             markdown_cell.source)

    def test_build_notebook_minimal(self):
        ipynb = n0.load_ipynb("samples/minimal.ipynb")
        nb = Notebook(ipynb)
        self.assertEqual("4.5", nb.version)

    def test_build_notebook_hello_world(self):
        ipynb = n0.load_ipynb("samples/hello-world.ipynb")
        nb = Notebook(ipynb)
        self.assertIsInstance(nb.cells, list)
        self.assertIsInstance(nb.cells[0], Cell)

class Question10(unittest.TestCase):
    def test_from_file(self):
        nb = Notebook.from_file("samples/minimal.ipynb")
        self.assertEqual("4.5", nb.version)

class Question11(unittest.TestCase):
    def test_iter_dunder(self):
        nb = Notebook.from_file("samples/hello-world.ipynb")
        self.assertEqual("a9541506", nb.cells[0].id)
        self.assertEqual("b777420a", nb.cells[1].id)
        self.assertEqual("a23ab5ac", nb.cells[2].id)

class Question12(unittest.TestCase):
    def test_serializer(self):
        nb = Notebook.from_file("samples/hello-world.ipynb")
        s = Serializer(nb)
        self.assertEqual(
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
            , s.serialize())

class Question13(unittest.TestCase):
    def test_py_percent_serializer(self):
            nb = Notebook.from_file("samples/hello-world.ipynb")
            ppp = PyPercentSerializer(nb)
            self.assertEqual(r"""# %% [markdown]
# Hello world!
# ============
# Print `Hello world!`:

# %%
print("Hello world!")

# %% [markdown]
# Goodbye! 👋"""
            , ppp.to_py_percent())

class Question14(unittest.TestCase):
    def test_outliner(self):
            nb = Notebook.from_file("samples/hello-world.ipynb")
            o = Outliner(nb)
            self.assertEqual(
                r"""Jupyter Notebook v4.5
└─▶ Markdown cell #a9541506
    ┌  Hello world!
    │  ============
    └  Print `Hello world!`:
└─▶ Code cell #b777420a (1)
    | print("Hello world!")
└─▶ Markdown cell #a23ab5ac
    | Goodbye! 👋"""
            , o.outline()
            )

if __name__ == "__main__":
    unittest.main()

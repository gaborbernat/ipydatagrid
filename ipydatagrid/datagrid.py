#!/usr/bin/env python
# coding: utf-8

# Copyright (c) QuantStack.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from traitlets import (
    Any, Bool, Dict, Enum, Instance, Int, List, Unicode, default
)
from copy import deepcopy
from ipywidgets import DOMWidget, Widget, widget_serialization

from ._frontend import module_name, module_version
from .cellrenderer import CellRenderer, TextRenderer


class DataGrid(DOMWidget):
    _model_name = Unicode('DataGridModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('DataGridView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    base_row_size = Int(20).tag(sync=True)
    base_column_size = Int(64).tag(sync=True)
    base_row_header_size = Int(64).tag(sync=True)
    base_column_header_size = Int(20).tag(sync=True)

    header_visibility = Enum(default_value='all', values=['all', 'row', 'column', 'none']).tag(sync=True)

    _transforms = List(Dict).tag(sync=True, **widget_serialization)
    _visible_rows = List(Int).tag(sync=True)
    data = Dict().tag(sync=True)

    renderers = Dict(Instance(CellRenderer)).tag(sync=True, **widget_serialization)
    default_renderer = Instance(CellRenderer).tag(sync=True, **widget_serialization)
    selection_mode = Enum(default_value='none', values=['row', 'column', 'cell', 'none']).tag(sync=True)

    def get_cell_value(self, column, row_index):
        """Gets the value for a single cell."""

        return self.data['data'][row_index][column]

    def get_visible_data(self):
        """Returns the dataset of the current View."""

        data = deepcopy(self.data)
        if self._visible_rows:
            data['data'] = [data['data'][i] for i in self._visible_rows]
        return data

    def transform(self, transforms):
        """Apply a list of transformation to this DataGrid."""

        # TODO: Validate this input, or let it fail on view side?
        self._transforms = transforms

    def revert(self):
        """Revert all transformations."""

        self._transforms = []

    @default('default_renderer')
    def _default_renderer(self):
        return TextRenderer()

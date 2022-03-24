# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TableComponent(Component):
    """A TableComponent component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- ascending (number; optional):
    Whether the sort is ascending (1), descending (-1), or none (0).

- column (string; optional):
    The column that is being sorted, if sorting is active.

- columns (list; optional):
    An array of objects: {name: str, id: str} used for display and
    identification of columns in the table for calling setProps.

- data (list; optional):
    The DataFrame of data that is to be displayed in the table.

- location (string; optional):
    Needed because it is passed up to Dash to update the map  after a
    row is clicked in the table.

- page_current (number; optional):
    A value used pretty much only for pagination purposes.

- page_size (number; optional):
    A value used pretty much only for pagination purposes.

- report_number (string; optional):
    Needed because it is passed up to Dash to update the map  after a
    row is clicked in the table.

- total_results (number; optional):
    A value used pretty much only for pagination purposes."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, data=Component.UNDEFINED, columns=Component.UNDEFINED, page_current=Component.UNDEFINED, total_results=Component.UNDEFINED, page_size=Component.UNDEFINED, location=Component.UNDEFINED, report_number=Component.UNDEFINED, column=Component.UNDEFINED, ascending=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'ascending', 'column', 'columns', 'data', 'location', 'page_current', 'page_size', 'report_number', 'total_results']
        self._type = 'TableComponent'
        self._namespace = 'koffie_frontend_challenge'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'ascending', 'column', 'columns', 'data', 'location', 'page_current', 'page_size', 'report_number', 'total_results']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in []:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TableComponent, self).__init__(**args)

# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class TableComponent(Component):
    """A TableComponent component.


Keyword arguments:

- id (string; optional):
    The ID used to identify this component in Dash callbacks.

- ascending (number; optional)

- column (string; optional)

- columns (list; optional)

- data (list; optional)

- label (string; required):
    A label that will be printed when this component is rendered.

- location (string; optional)

- page_current (number; optional)

- page_size (number; optional)

- report_number (string; optional)

- total_results (number; optional)

- value (string; optional):
    The value displayed in the input."""
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, label=Component.REQUIRED, value=Component.UNDEFINED, data=Component.UNDEFINED, columns=Component.UNDEFINED, page_current=Component.UNDEFINED, page_size=Component.UNDEFINED, location=Component.UNDEFINED, total_results=Component.UNDEFINED, report_number=Component.UNDEFINED, column=Component.UNDEFINED, ascending=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'ascending', 'column', 'columns', 'data', 'label', 'location', 'page_current', 'page_size', 'report_number', 'total_results', 'value']
        self._type = 'TableComponent'
        self._namespace = 'koffie_frontend_challenge'
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'ascending', 'column', 'columns', 'data', 'label', 'location', 'page_current', 'page_size', 'report_number', 'total_results', 'value']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs
        args = {k: _locals[k] for k in _explicit_args if k != 'children'}
        for k in ['label']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')
        super(TableComponent, self).__init__(**args)

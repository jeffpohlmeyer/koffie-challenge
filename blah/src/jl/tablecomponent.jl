# AUTO GENERATED FILE - DO NOT EDIT

export tablecomponent

"""
    tablecomponent(;kwargs...)

A TableComponent component.

Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `ascending` (Real; optional)
- `column` (String; optional)
- `columns` (Array; optional)
- `data` (Array; optional)
- `label` (String; required): A label that will be printed when this component is rendered.
- `location` (String; optional)
- `page_current` (Real; optional)
- `page_size` (Real; optional)
- `report_number` (String; optional)
- `total_results` (Real; optional)
- `value` (String; optional): The value displayed in the input.
"""
function tablecomponent(; kwargs...)
        available_props = Symbol[:id, :ascending, :column, :columns, :data, :label, :location, :page_current, :page_size, :report_number, :total_results, :value]
        wild_props = Symbol[]
        return Component("tablecomponent", "TableComponent", "koffie_frontend_challenge", available_props, wild_props; kwargs...)
end


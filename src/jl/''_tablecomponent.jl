# AUTO GENERATED FILE - DO NOT EDIT

export ''_tablecomponent

"""
    ''_tablecomponent(;kwargs...)

A TableComponent component.

Keyword arguments:
- `id` (String; optional): The ID used to identify this component in Dash callbacks.
- `ascending` (Real; optional): Whether the sort is ascending (1), descending (-1), or none (0)
- `column` (String; optional): The column that is being sorted, if sorting is active
- `columns` (Array; optional): An array of objects: {name: str, id: str} used for display and
identification of columns in the table for calling setProps
- `data` (Array; optional): The DataFrame of data that is to be displayed in the table
- `location` (String; optional): Needed because it is passed up to Dash to update the map
after a row is clicked in the table
- `page_current` (Real; optional): A value used pretty much only for pagination purposes
- `page_size` (Real; optional): A value used pretty much only for pagination purposes
- `report_number` (String; optional): Needed because it is passed up to Dash to update the map
after a row is clicked in the table
- `total_results` (Real; optional): A value used pretty much only for pagination purposes
"""
function ''_tablecomponent(; kwargs...)
        available_props = Symbol[:id, :ascending, :column, :columns, :data, :location, :page_current, :page_size, :report_number, :total_results]
        wild_props = Symbol[]
        return Component("''_tablecomponent", "TableComponent", "koffie_frontend_challenge", available_props, wild_props; kwargs...)
end


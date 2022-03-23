# AUTO GENERATED FILE - DO NOT EDIT

#' @export
tableComponent <- function(id=NULL, ascending=NULL, column=NULL, columns=NULL, data=NULL, label=NULL, location=NULL, page_current=NULL, page_size=NULL, report_number=NULL, total_results=NULL, value=NULL) {
    
    props <- list(id=id, ascending=ascending, column=column, columns=columns, data=data, label=label, location=location, page_current=page_current, page_size=page_size, report_number=report_number, total_results=total_results, value=value)
    if (length(props) > 0) {
        props <- props[!vapply(props, is.null, logical(1))]
    }
    component <- list(
        props = props,
        type = 'TableComponent',
        namespace = 'koffie_frontend_challenge',
        propNames = c('id', 'ascending', 'column', 'columns', 'data', 'label', 'location', 'page_current', 'page_size', 'report_number', 'total_results', 'value'),
        package = 'koffieFrontendChallenge'
        )

    structure(component, class = c('dash_component', 'list'))
}

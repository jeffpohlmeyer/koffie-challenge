% Auto-generated: do not edit by hand
\name{''TableComponent}

\alias{''TableComponent}

\title{TableComponent component}

\description{

}

\usage{
''TableComponent(id=NULL, ascending=NULL, column=NULL, columns=NULL,
data=NULL, location=NULL, page_current=NULL, page_size=NULL,
report_number=NULL, total_results=NULL)
}

\arguments{
\item{id}{Character. The ID used to identify this component in Dash callbacks.}

\item{ascending}{Numeric. Whether the sort is ascending (1), descending (-1), or none (0)}

\item{column}{Character. The column that is being sorted, if sorting is active}

\item{columns}{Unnamed list. An array of objects: {name: str, id: str} used for display and
identification of columns in the table for calling setProps}

\item{data}{Unnamed list. The DataFrame of data that is to be displayed in the table}

\item{location}{Character. Needed because it is passed up to Dash to update the map
after a row is clicked in the table}

\item{page_current}{Numeric. A value used pretty much only for pagination purposes}

\item{page_size}{Numeric. A value used pretty much only for pagination purposes}

\item{report_number}{Character. Needed because it is passed up to Dash to update the map
after a row is clicked in the table}

\item{total_results}{Numeric. A value used pretty much only for pagination purposes}
}

\value{named list of JSON elements corresponding to React.js properties and their values}


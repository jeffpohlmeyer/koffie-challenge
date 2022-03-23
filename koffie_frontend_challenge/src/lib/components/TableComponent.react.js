import React, {Component, Fragment } from 'react';
import { Menu, Transition } from '@headlessui/react'
import { ChevronDownIcon } from '@heroicons/react/solid'
import PropTypes from 'prop-types';

export default class TableComponent extends Component {
    render() {
        const {id, setProps, columns, data, page_current, total_results, page_size, ascending, column} = this.props;

        const lowVal = page_current * page_size + 1
        const highVal = lowVal + page_size - 1

        const handleRowClick = (city, state, reportNumber) => {
            setProps({location:`${city}, ${state}`, report_number: reportNumber
        })
        }

        const sortByColumn = (col) => {
            let payload = {column: col, page_current}
            if (col !== column) {
                payload = {...payload, ascending: 1}
            } else {
                payload = {...payload, ascending: ascending === 0 ? 1 : ascending === 1 ? -1 : 0}
            }
            setProps(payload)
        }

        const goToPrevious = () => {
            if (page_current > 0) {
                setProps({page_current: page_current - 1})
            }
        }
        const goToNext = () => {
            if (page_current < Math.ceil(total_results / page_size)) {
                setProps({page_current: page_current + 1})
            }
        }

        let tableBody
            if (!data.length) {
                tableBody=  (
                    <tr className="flex justify-center">
                        <td colSpan={columns.length} className='py-10 text-3xl font-semibold'>That search returned no results!</td>
                    </tr>
                )
            } else {

            tableBody = data.map(item => (
                <tr key={item.REPORT_NUMBER} onClick={() => handleRowClick(item.CITY, item.STATE, item.REPORT_NUMBER)}>
                    {columns.map(column => (
                        <td key={`${item.REPORT_NUMBER}~${column.id}`} className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                            {item[column.id]}
                        </td>
                    ))}
                </tr>
            ))
        }




return (
    <>
    <div id={id}>
        <div className="mt-8 flex flex-col">
        <div className="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
            <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
        <table className="min-w-full table-fixed">
            <thead className="bg-gray-50">
             <tr>
                 {columns.map(column => (
                     <th key={column.id} scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 cursor-pointer" onClick={() => sortByColumn(column.id)}>
                         {column.name}

                     </th>
                 ))}
                  </tr>

            </thead>
            <tbody className="divide-y divide-gray-200 bg-white">
            {tableBody}
                </tbody>

        </table>
    </div>
          </div>
        </div>
        </div>
    </div>
<nav
      className="bg-white py-6 flex items-center justify-between"
      aria-label="Pagination"
    >
      <div className="hidden sm:block">
        <p className="text-sm text-gray-700">
          Showing <span className="font-medium">{lowVal}</span> to <span className="font-medium">{highVal}</span> of{' '}
          <span className="font-medium">{total_results}</span> results
        </p>
      </div>
      <div className="flex-1 flex justify-between sm:justify-end">
        <button
          className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          onClick={goToPrevious}
        >
          Previous
        </button>
        <button
          className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          onClick={goToNext}
        >
          Next
        </button>
      </div>
    </nav>
    </>)
    }
}

TableComponent.defaultProps = {};

TableComponent.propTypes = {
    /**
     * The ID used to identify this component in Dash callbacks.
     */
    id: PropTypes.string,

    /**
     * A label that will be printed when this component is rendered.
     */
    label: PropTypes.string.isRequired,

    /**
     * The value displayed in the input.
     */
    value: PropTypes.string,

    /**
     * Dash-assigned callback that should be called to report property changes
     * to Dash, to make them available for callbacks.
     */
    setProps: PropTypes.func,

    data: PropTypes.array,
    columns:PropTypes.array,
    page_current: PropTypes.number,
    page_size:PropTypes.number,
    location: PropTypes.string,
    total_results: PropTypes.number,
    report_number: PropTypes.string,
    column: PropTypes.string,
    ascending: PropTypes.number,
};

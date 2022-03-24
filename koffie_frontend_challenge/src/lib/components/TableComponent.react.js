import React, { Component } from 'react';
import PropTypes from 'prop-types';

export default class TableComponent extends Component {
  render() {
    const {
      id,
      setProps,
      columns,
      data,
      page_current,
      total_results,
      page_size,
      ascending,
      column,
    } = this.props;

    // Pagination
    const lowVal = page_current * page_size + 1;
    const highVal = lowVal + page_size - 1;

    // If we're not on the first page then go back one
    const goToPrevious = () => {
      if (page_current > 0) {
        setProps({page_current: page_current - 1});
      }
    };

    // If we're not on the last page then go forward one
    const goToNext = () => {
      if (page_current < Math.ceil(total_results / page_size)) {
        setProps({page_current: page_current + 1});
      }
    };

    /**
     * This method creates the `<city>, <state>` string and calls
     * setProps to update the map
     *
     * @param {string} city The city name for updating the map
     * @param {string} state The state name for updating the map
     * @param {string} reportNumber This is simply for display on the map
     */
    const handleRowClick = (city, state, reportNumber) => {
      setProps({
        location: `${city}, ${state}`,
        report_number: reportNumber,
      });
    };

    /**
     * This method checks to see if the column that is attempting to be
     * sorted matches the one that was already sorted. If it matches,
     * then continue along the progression of 0->1->-1->0->1...
     * If not then set ascending to be true because you're on a new column
     *
     * @param {string} col The name of the column to be sorted
     */
    const sortByColumn = (col) => {
      let payload = {column: col, page_current};
      if (col !== column) {
        payload = {...payload, ascending: 1};
      } else {
        payload = {
          ...payload,
          ascending: ascending === 0 ? 1 : ascending === 1 ? -1 : 0,
        };
      }
      setProps(payload);
    };

    /**
     * This simply moves the logic out of the markup. This is to display
     * a message if the data prop is an empty array instead of an empty
     * table.
     */
    let tableBody;
    if (!data.length) {
      tableBody = (
        <tr className="flex justify-center">
          <td colSpan={columns.length} className="py-10 text-3xl font-semibold">
            That search returned no results!
          </td>
        </tr>
      );
    } else {
      tableBody = data.map((item) => (
        <tr
          key={item.REPORT_NUMBER}
          onClick={() =>
            handleRowClick(item.CITY, item.STATE, item.REPORT_NUMBER)
          }
        >
          {columns.map((column) => (
            <td
              key={`${item.REPORT_NUMBER}~${column.id}`}
              className="whitespace-nowrap p-2 text-sm text-gray-500"
            >
              {item[column.id]}
            </td>
          ))}
        </tr>
      ));
    }

    /**
     * The majority of the styling for this table comes from
     * https://tailwindui.com
     */
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
                        {columns.map((column) => (
                          <th
                            key={column.id}
                            scope="col"
                            className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 cursor-pointer"
                            onClick={() => sortByColumn(column.id)}
                          >
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
              Showing <span className="font-medium">{lowVal}</span> to{' '}
              <span className="font-medium">{highVal}</span> of{' '}
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
      </>
    );
  }
}

TableComponent.defaultProps = {};

TableComponent.propTypes = {
  /**
   * The ID used to identify this component in Dash callbacks.
   */
  id: PropTypes.string,

  /**
   * Dash-assigned callback that should be called to report property changes
   * to Dash, to make them available for callbacks.
   */
  setProps: PropTypes.func,

  /**
   * The DataFrame of data that is to be displayed in the table
  */
  data: PropTypes.array,

  /**
   * An array of objects: {name: str, id: str} used for display and
   * identification of columns in the table for calling setProps
  */
  columns: PropTypes.array,

  /**
   * A value used pretty much only for pagination purposes
  */
  page_current: PropTypes.number,

  /**
   * A value used pretty much only for pagination purposes
  */
  total_results: PropTypes.number,

  /**
   * A value used pretty much only for pagination purposes
  */
  page_size: PropTypes.number,

  /**
   * Needed because it is passed up to Dash to update the map
   * after a row is clicked in the table
  */
  location: PropTypes.string,

  /**
   * Needed because it is passed up to Dash to update the map
   * after a row is clicked in the table
  */
  report_number: PropTypes.string,

  /**
   * The column that is being sorted, if sorting is active
  */
  column: PropTypes.string,

  /**
   * Whether the sort is ascending (1), descending (-1), or none (0)
  */
  ascending: PropTypes.number,
};

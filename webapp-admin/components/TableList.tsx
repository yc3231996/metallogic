import React from 'react';
import { Table } from '../lib/api';

type TableListProps = {
  tables: Table[];
  onSelectTable: (table: Table) => void;
  selectedTable: Table;
};

const TableList: React.FC<TableListProps> = ({ tables, onSelectTable, selectedTable }) => {
  return (
    <div className="bg-blue-50 p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4 text-blue-800">Workspace Tables</h2>
      <ul className="space-y-2">
        {tables.map((table) => (
          <li
            key={table}
            className={`cursor-pointer transition-colors duration-150 p-3 rounded-md shadow-sm ${
              selectedTable === table ? 'bg-blue-200' : 'bg-white hover:bg-blue-100'
            }`}
            onClick={() => onSelectTable(table)}
          >
            <span className="font-medium text-gray-800">{table}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TableList;
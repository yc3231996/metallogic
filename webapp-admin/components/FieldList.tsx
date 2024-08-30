import React, { useState, useEffect } from 'react';
import { TableMetadata, Field } from '@/lib/api';

type FieldListProps = {
  fields: Field[];
  tableMetadata: TableMetadata | null;
  onSave: (tableMetadata: TableMetadata) => void;
};

const FieldList: React.FC<FieldListProps> = ({ fields, tableMetadata, onSave }) => {
  const [localTableMetadata, setLocalTableMetadata] = useState<TableMetadata>({
    table_name: '',
    table_description: '',
    fields: []
  });

  useEffect(() => {
    if (tableMetadata) {
      setLocalTableMetadata(tableMetadata);
    } else {
      // when tableMetadata is null, probably because no table is selected
      console.debug('tableMetadata is null in FieldList component');
    }
  }, [tableMetadata]);

  const isFieldInTableMetadata = (name: string) => {
    return localTableMetadata.fields.some(field => field.name === name);
  };

  const getFieldDescription = (name: string) => {
    return localTableMetadata.fields.find(field => field.name === name)?.description || '';
  };

  const handleFieldChange = (field: Field, isChecked: boolean, description: string) => {
    let updatedFields;
    if (isChecked) {
      updatedFields = [
        ...localTableMetadata.fields.filter(f => f.name !== field.name),
        { ...field, description }
      ];
    } else {
      updatedFields = localTableMetadata.fields.filter(f => f.name !== field.name);
    }

    setLocalTableMetadata({
      ...localTableMetadata,
      fields: updatedFields
    });
  };

  const handleTableDescriptionChange = (description: string) => {
    setLocalTableMetadata({
      ...localTableMetadata,
      table_description: description
    });
  };

  const handleSave = () => {
    onSave(localTableMetadata);
  };

  return (
    <div className="bg-green-50 p-6 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-4 text-green-800">Field List</h2>
      <div className="overflow-x-auto">
        <table className="w-full bg-white rounded-lg overflow-hidden">
          <thead className="bg-green-200 text-green-800">
            <tr>
              <th className="py-3 px-4 text-left w-16">Check</th>
              <th className="py-3 px-4 text-left">Column Name</th>
              <th className="py-3 px-4 text-left">Column Type</th>
              <th className="py-3 px-4 text-left">Column Description</th>
            </tr>
          </thead>
          <tbody>
            {fields.map((field) => (
              <tr key={field.name} className="border-b border-green-100">
                <td className="py-3 px-4">
                  <input
                    type="checkbox"
                    checked={isFieldInTableMetadata(field.name)}
                    onChange={(e) => handleFieldChange(field, e.target.checked, getFieldDescription(field.name))}
                    className="form-checkbox h-5 w-5 text-green-600"
                  />
                </td>
                <td className="py-3 px-4 font-medium">{field.name}</td>
                <td className="py-3 px-4">{field.type}</td>
                <td className="py-3 px-4">
                  <input
                    type="text"
                    value={getFieldDescription(field.name)}
                    onChange={(e) => handleFieldChange(field, isFieldInTableMetadata(field.name), e.target.value)}
                    className="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-green-400"
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <input
        type="text"
        value={localTableMetadata.table_description}
        onChange={(e) => handleTableDescriptionChange(e.target.value)}
        className="w-full p-2 mt-4 mb-4 border rounded focus:outline-none focus:ring-2 focus:ring-green-400"
        placeholder="Table Description"
      />
      <button
        className="mt-4 bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded transition-colors duration-150"
        onClick={handleSave}
      >
        SAVE
      </button>
    </div>
  );
};

export default FieldList;
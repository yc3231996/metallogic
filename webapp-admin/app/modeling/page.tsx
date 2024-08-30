'use client';

import React, { useState, useEffect, use } from 'react';
import WorkspaceSelector from '@/components/WorkspaceSelector';
import TableList from '@/components/TableList';
import FieldList from '@/components/FieldList';
import MetricsAndDimensions from '@/components/MetricsAndDimensions';
import { fetchTableMetadata, saveTableMetadata, fetchWorkspaces, fetchWorkspaceMetadata, fetchTables, fetchFields, Workspace, Table, Field, TableMetadata, WorkspaceMetadata } from '@/lib/api';

export default function Home() {
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [selectedWorkspace, setSelectedWorkspace] = useState<string>('');
  const [tables, setTables] = useState<Table[]>([]);
  const [selectedTable, setSelectedTable] = useState<Table>('');
  const [fields, setFields] = useState<Field[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [tableMetadata, setTableMetadata] = useState<TableMetadata | null>(null);
  const [workspaceMetadata, setWorkspaceMetadata] = useState<WorkspaceMetadata>('');

  useEffect(() => {
    const loadWorkspaces = async () => {
      try {
        const fetchedWorkspaces = await fetchWorkspaces();
        setWorkspaces(fetchedWorkspaces);
        if (fetchedWorkspaces.length > 0) {
          setSelectedWorkspace(fetchedWorkspaces[0].id);
        }
      } catch (error) {
        console.error('Error fetching workspaces:', error);
      } finally {
        setLoading(false);
      }
    };
    loadWorkspaces();
  }, []);

  useEffect(() => {
    const loadTables = async () => {
      if (selectedWorkspace) {
        setLoading(true);
        try {
          const fetchedTables = await fetchTables(selectedWorkspace);
          setTables(fetchedTables);
          setSelectedTable('');
          setFields([]);
        } catch (error) {
          console.error('Error fetching tables:', error);
        } finally {
          setLoading(false);
        }
      }
    };
    loadTables();
  }, [selectedWorkspace]);

  useEffect(() => {
    const loadFields = async () => {
      if (selectedWorkspace && selectedTable) {
        setLoading(true);
        try {
          const fetchedFields = await fetchFields(selectedWorkspace, selectedTable);
          setFields(fetchedFields);
        } catch (error) {
          console.error('Error fetching fields:', error);
        } finally {
          setLoading(false);
        }
      }
    };
    loadFields();
  }, [selectedWorkspace, selectedTable]);

  useEffect(() => {
    const loadTableMetadata = async () => {
      if (selectedWorkspace && selectedTable) {
        setLoading(true);
        try {
          const metadata = await fetchTableMetadata(selectedWorkspace, selectedTable);
          if (metadata) {
            setTableMetadata(metadata);
          } else {
            // If backend returns null, create a default TableMetadata object
            setTableMetadata({
              table_name: selectedTable,
              table_description: '',
              fields: []
            });
          }
        } catch (error) {
          console.error('Error fetching table metadata:', error);
        } finally {
          setLoading(false);
        }
      }
    };
    loadTableMetadata();
  }, [selectedWorkspace, selectedTable]);

  const handleSaveMetadata = async (updatedMetadata: TableMetadata) => {
    if (selectedWorkspace && selectedTable && updatedMetadata) {
      setLoading(true);
      try {
        await saveTableMetadata(selectedWorkspace, selectedTable, updatedMetadata);
        setTableMetadata(updatedMetadata);
        // TODO Optionally, show a success message

        loadWorkspaceMetadata();
      } catch (error) {
        console.error('Error saving table metadata:', error);
        // TODO Optionally, show an error message
      } finally {
        setLoading(false);
      }
    }
  };

  const loadWorkspaceMetadata = async () => { 
    if (selectedWorkspace) {
      setLoading(true);
      try {
        const fetchedWorkspaceMetadata = await fetchWorkspaceMetadata(selectedWorkspace);
        setWorkspaceMetadata(fetchedWorkspaceMetadata);
      } catch (error) {
        console.error('Error fetching workspace metadata:', error);
      } finally {
        setLoading(false);
      }
    }
  }
  
  useEffect(() => {
    loadWorkspaceMetadata();
  }, [selectedWorkspace])


  return (
    <main className="flex min-h-screen p-8 bg-gray-100">
      {loading ? (
        <div className="flex items-center justify-center w-full">
          <p className="text-xl font-semibold">加载中...</p>
        </div>
      ) : (
        <>
          <div className="flex-1 mr-6">
            <div className="mb-6">
              <WorkspaceSelector
                workspaces={workspaces}
                selectedWorkspace={selectedWorkspace}
                onSelect={setSelectedWorkspace}
              />
            </div>
            <TableList 
              tables={tables} 
              onSelectTable={setSelectedTable}
              selectedTable={selectedTable}
            />
          </div>
          <div className="flex-[3] mr-6">
            {selectedTable && (<FieldList fields={fields} tableMetadata={tableMetadata} onSave={handleSaveMetadata} />)}
          </div>
          <div className="flex-1">
            <div className=''>
              {selectedWorkspace && <MetricsAndDimensions metrics={workspaceMetadata} />}
            </div>
            {/* <iframe src="http://localhost/chatbot/wvV1rq7sfqlmItBB" className='min-h-[700px] w-full' frameborder="0" allow="microphone"> </iframe> */}
          </div>
        </>
      )}
    </main>
  );
}
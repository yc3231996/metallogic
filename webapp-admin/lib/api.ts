// api.ts
import config from '@/config';

export interface Workspace {
  id: string;
  name: string;
}

export type Table = string;

export interface Field {
  name: string;
  type: string;
  description: string;
}

export interface TableMetadata {
  table_name: string;
  table_description: string;
  fields: Field[];
}

export type WorkspaceMetadata = string;

// export interface FieldMetadata {
//   name: string;
//   type: string;
//   comment: string;
//   selected?: boolean;
// }

const buildApiUrl = (path: string) => `${config.publicApiBaseUrl}${path}`;

export const fetchWorkspaces = async (): Promise<Workspace[]> => {
  const response = await fetch(buildApiUrl('/workspaces'));
  if (!response.ok) {
    throw new Error('Failed to fetch workspaces');
  }
  return response.json();
};

export const fetchTables = async (workspace: string): Promise<Table[]> => {
  const response = await fetch(buildApiUrl(`/${workspace}/tables`));
  if (!response.ok) {
    throw new Error(`Failed to fetch tables for workspace ${workspace}`);
  }
  return response.json();
};

export const fetchFields = async (workspace: string, table: string): Promise<Field[]> => {
  const response = await fetch(buildApiUrl(`/${workspace}/${table}/fields`));
  if (!response.ok) {
    throw new Error(`Failed to fetch fields for table ${table} in workspace ${workspace}`);
  }
  return response.json();
};

export const fetchTableMetadata = async (workspace: string, table: string): Promise<TableMetadata> => {
  const response = await fetch(buildApiUrl(`/${workspace}/${table}/metadata`));
  if (!response.ok) {
    throw new Error(`Failed to fetch metadata for table ${table} in workspace ${workspace}`);
  }
  return response.json();
};

export const saveTableMetadata = async (workspace: string, table: string, metadata: TableMetadata): Promise<void> => {
  const response = await fetch(buildApiUrl(`/${workspace}/${table}/metadata`), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(metadata),
  });
  if (!response.ok) {
    throw new Error(`Failed to save metadata for table ${table} in workspace ${workspace}`);
  }
};

export const fetchWorkspaceMetadata = async (workspace: string): Promise<WorkspaceMetadata> => {
  const response = await fetch(buildApiUrl(`/${workspace}/metadata`));
  if (!response.ok) {
    throw new Error(`Failed to fetch metadata for workspace ${workspace}`);
  }
  return response.json();
}
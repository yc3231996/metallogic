import React from 'react';
import { Workspace } from '../lib/api';

type WorkspaceSelectorProps = {
  workspaces: Workspace[];
  selectedWorkspace: string;
  onSelect: (workspaceId: string) => void;
};

const WorkspaceSelector: React.FC<WorkspaceSelectorProps> = ({ workspaces, selectedWorkspace, onSelect }) => {
  return (
    <div className="mb-4">
      <select
        value={selectedWorkspace}
        onChange={(e) => onSelect(e.target.value)}
        className="w-full p-2 border rounded bg-white focus:outline-none focus:ring-2 focus:ring-blue-400"
      >
        {workspaces.map((workspace) => (
          <option key={workspace.id} value={workspace.id}>
            {workspace.name}
          </option>
        ))}
      </select>
    </div>
  );
};

export default WorkspaceSelector;
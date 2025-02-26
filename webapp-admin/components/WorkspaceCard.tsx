'use client';

import React, { useState } from 'react';
import { Workspace } from '@/lib/api';
import { MoreHorizontal } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog';

interface WorkspaceCardProps {
  workspace: Workspace;
  onDelete: (workspaceId: string) => void;
}

const WorkspaceCard: React.FC<WorkspaceCardProps> = ({ workspace, onDelete }) => {
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);

  return (
    <div className="bg-white rounded-lg shadow-md p-3 flex flex-col h-40">
      <div className="flex-grow">
        <h3 className="text-lg font-semibold text-gray-800">{workspace.name}</h3>
        <span className="text-sm text-gray-500">{workspace.type}</span>
      </div>
      <div className="flex justify-end">
        <DropdownMenu>
          <DropdownMenuTrigger className="p-1 rounded-full hover:bg-gray-100">
            <MoreHorizontal className="h-4 w-4 text-gray-500" />
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuItem onClick={() => setShowDeleteDialog(true)}>
              删除
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      <AlertDialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>确认删除</AlertDialogTitle>
            <AlertDialogDescription>
              您确定要删除 "{workspace.name}" 工作区吗？此操作无法撤销。
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>取消</AlertDialogCancel>
            <AlertDialogAction 
              onClick={() => onDelete(workspace.id)}
              className="bg-red-500 hover:bg-red-600"
            >
              删除
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

export default WorkspaceCard; 
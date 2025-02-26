'use client';

import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Plus } from 'lucide-react';
import { fetchWorkspaces, createWorkspace, deleteWorkspace, Workspace, CreateWorkspaceParams } from '@/lib/api';
import WorkspaceCard from '@/components/WorkspaceCard';
import CreateWorkspaceDialog from '@/components/CreateWorkspaceDialog';
import { useToast } from '@/components/ui/use-toast';

const WorkspaceManagement = () => {
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [loadError, setLoadError] = useState<string | null>(null);
  const { toast } = useToast();
  const isFirstRender = useRef(true);
  const loadingRef = useRef(false);

  // 使用useCallback包装loadWorkspaces函数，避免不必要的重新创建
  const loadWorkspaces = useCallback(async () => {
    // 防止重复加载
    if (loadingRef.current) return;
    
    try {
      loadingRef.current = true;
      setIsLoading(true);
      setLoadError(null);
      
      const data = await fetchWorkspaces();
      console.log('获取到的工作区数据:', data);
      
      // 确保data是数组
      if (Array.isArray(data)) {
        setWorkspaces(data);
      } else {
        console.error('Unexpected data format:', data);
        setWorkspaces([]);
        setLoadError('数据格式错误');
      }
    } catch (error) {
      console.error('Failed to fetch workspaces:', error);
      setLoadError('加载失败');
      toast({
        title: '加载失败',
        description: '无法加载工作区列表，请稍后重试。',
        variant: 'destructive',
      });
      setWorkspaces([]);
    } finally {
      setIsLoading(false);
      loadingRef.current = false;
    }
  }, [toast]);

  // 确保useEffect只在组件挂载时执行一次
  useEffect(() => {
    if (isFirstRender.current) {
      isFirstRender.current = false;
      loadWorkspaces();
    }
  }, [loadWorkspaces]);

  const handleCreateWorkspace = async (data: CreateWorkspaceParams) => {
    try {
      await createWorkspace(data);
      toast({
        title: '创建成功',
        description: `工作区 "${data.workspace}" 已成功创建。`,
      });
      setIsCreateDialogOpen(false);
      // 创建成功后刷新工作区列表
      await loadWorkspaces();
    } catch (error) {
      console.error('Failed to create workspace:', error);
      toast({
        title: '创建失败',
        description: '无法连接数据源，创建工作区失败。请检查连接信息是否正确，然后重试。',
        variant: 'destructive',
      });
    }
  };

  const handleDeleteWorkspace = async (workspaceId: string) => {
    try {
      await deleteWorkspace(workspaceId);
      toast({
        title: '删除成功',
        description: `工作区 "${workspaceId}" 已成功删除。`,
      });
      // 删除成功后刷新工作区列表
      await loadWorkspaces();
    } catch (error) {
      console.error('Failed to delete workspace:', error);
      toast({
        title: '删除失败',
        description: '无法删除工作区，请稍后重试。',
        variant: 'destructive',
      });
    }
  };

  return (
    <div className="container mx-auto py-6">
      <h1 className="text-2xl font-bold mb-6">工作区管理</h1>
      
      {isLoading ? (
        <div className="flex justify-center items-center h-64">
          <p className="text-gray-500">加载中...</p>
        </div>
      ) : loadError ? (
        <div className="flex justify-center items-center h-64">
          <div className="text-center">
            <p className="text-red-500 mb-4">{loadError}</p>
            <button 
              onClick={() => loadWorkspaces()} 
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              重试
            </button>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* 创建工作区卡片 */}
          <div 
            className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-3 flex flex-col items-center justify-center h-40 cursor-pointer hover:bg-gray-100 transition-colors"
            onClick={() => setIsCreateDialogOpen(true)}
          >
            <Plus className="h-10 w-10 text-gray-400 mb-2" />
            <p className="text-gray-500 font-medium">创建新工作区</p>
          </div>
          
          {/* 工作区列表 */}
          {Array.isArray(workspaces) && workspaces.length > 0 ? (
            workspaces.map((workspace) => (
              <WorkspaceCard
                key={workspace.id}
                workspace={workspace}
                onDelete={handleDeleteWorkspace}
              />
            ))
          ) : (
            <div className="col-span-full text-center py-8 text-gray-500">
              暂无工作区，请点击左侧创建新工作区
            </div>
          )}
        </div>
      )}
      
      <CreateWorkspaceDialog
        open={isCreateDialogOpen}
        onOpenChange={setIsCreateDialogOpen}
        onSubmit={handleCreateWorkspace}
      />
    </div>
  );
};

export default WorkspaceManagement;
'use client';

import React, { useState } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter, DialogClose, DialogDescription } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { CreateWorkspaceParams } from '@/lib/api';
import { X } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';

interface CreateWorkspaceDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSubmit: (data: CreateWorkspaceParams) => void;
}

// Workspace名称验证规则
const WORKSPACE_NAME_REGEX = /^[a-z0-9][a-z0-9-]*[a-z0-9]$/;
const MIN_WORKSPACE_NAME_LENGTH = 3;
const MAX_WORKSPACE_NAME_LENGTH = 30;

const CreateWorkspaceDialog: React.FC<CreateWorkspaceDialogProps> = ({
  open,
  onOpenChange,
  onSubmit,
}) => {
  const [dbType, setDbType] = useState<string>('sql');
  const [workspace, setWorkspace] = useState<string>('');
  const [connStr, setConnStr] = useState<string>('');
  const [projectId, setProjectId] = useState<string>('');
  const [credentialsJson, setCredentialsJson] = useState<string>('');
  const [nameError, setNameError] = useState<string>('');

  const validateWorkspaceName = (name: string): boolean => {
    // 检查长度
    if (name.length < MIN_WORKSPACE_NAME_LENGTH) {
      setNameError(`工作区名称至少需要${MIN_WORKSPACE_NAME_LENGTH}个字符`);
      return false;
    }
    
    if (name.length > MAX_WORKSPACE_NAME_LENGTH) {
      setNameError(`工作区名称最多允许${MAX_WORKSPACE_NAME_LENGTH}个字符`);
      return false;
    }
    
    // 检查是否包含连续的连字符
    if (name.includes('--')) {
      setNameError('工作区名称不能包含连续的连字符(-)');
      return false;
    }
    
    // 检查格式
    if (!WORKSPACE_NAME_REGEX.test(name)) {
      setNameError('工作区名称只能包含小写字母(a-z)、数字(0-9)和连字符(-)，且必须以字母或数字开头和结尾');
      return false;
    }
    
    setNameError('');
    return true;
  };

  const handleWorkspaceChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setWorkspace(value);
    if (value) {
      validateWorkspaceName(value);
    } else {
      setNameError('');
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateWorkspaceName(workspace)) {
      return;
    }
    
    const params: CreateWorkspaceParams = {
      workspace,
      db_type: dbType,
    };

    if (dbType === 'sql') {
      params.conn_str = connStr;
    } else if (dbType === 'bigquery') {
      params.project_id = projectId;
      params.credentials_json_str = credentialsJson;
    }

    onSubmit(params);
    resetForm();
  };

  const resetForm = () => {
    setWorkspace('');
    setConnStr('');
    setProjectId('');
    setCredentialsJson('');
    setDbType('sql');
    setNameError('');
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[800px] w-[90vw]">
        <DialogHeader>
          <DialogTitle className="text-xl font-bold">创建新的工作区</DialogTitle>
          <DialogDescription>
            填写以下信息创建一个新的工作区
          </DialogDescription>
        </DialogHeader>
        
        <DialogClose className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none">
          <X className="h-4 w-4" />
          <span className="sr-only">关闭</span>
        </DialogClose>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-4">
            <div>
              <Label htmlFor="workspace">工作区名称</Label>
              <Input
                id="workspace"
                value={workspace}
                onChange={handleWorkspaceChange}
                placeholder="输入工作区名称"
                required
                className={nameError ? "border-red-500" : ""}
              />
              {nameError && (
                <Alert variant="destructive" className="mt-2 py-2">
                  <AlertDescription>{nameError}</AlertDescription>
                </Alert>
              )}
              <p className="text-xs text-gray-500 mt-1">
                工作区名称只能包含小写字母(a-z)、数字(0-9)和连字符(-)，长度在{MIN_WORKSPACE_NAME_LENGTH}-{MAX_WORKSPACE_NAME_LENGTH}个字符之间，且必须以字母或数字开头和结尾。
              </p>
            </div>
            
            <div className="space-y-2">
              <Label>数据库类型</Label>
              <RadioGroup value={dbType} onValueChange={setDbType} className="flex flex-col space-y-1">
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="sql" id="sql" />
                  <Label htmlFor="sql">SQL 数据库</Label>
                </div>
                <div className="flex items-center space-x-2">
                  <RadioGroupItem value="bigquery" id="bigquery" />
                  <Label htmlFor="bigquery">BigQuery</Label>
                </div>
              </RadioGroup>
            </div>
            
            {dbType === 'sql' ? (
              <div>
                <Label htmlFor="connStr">连接字符串</Label>
                <Input
                  id="connStr"
                  value={connStr}
                  onChange={(e) => setConnStr(e.target.value)}
                  placeholder="输入数据库连接字符串"
                  required
                />
              </div>
            ) : (
              <>
                <div>
                  <Label htmlFor="projectId">Project ID</Label>
                  <Input
                    id="projectId"
                    value={projectId}
                    onChange={(e) => setProjectId(e.target.value)}
                    placeholder="输入 BigQuery Project ID"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="credentialsJson">Credentials JSON</Label>
                  <Textarea
                    id="credentialsJson"
                    value={credentialsJson}
                    onChange={(e) => setCredentialsJson(e.target.value)}
                    placeholder="输入 BigQuery Credentials JSON"
                    className="min-h-[200px]"
                    required
                  />
                </div>
              </>
            )}
          </div>
          
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              取消
            </Button>
            <Button type="submit" disabled={!!nameError && workspace.length > 0}>创建</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
};

export default CreateWorkspaceDialog; 
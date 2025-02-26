import { NextResponse } from 'next/server';
import config from '@/config';

export async function GET() {
  try {
    console.log('Fetching workspaces...' + `${config.apiBaseUrl}/workspaces`);
    const response = await fetch(`${config.apiBaseUrl}/workspaces`, {
      cache: 'no-store',
      headers: {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'X-API-Key': config.apiKey,
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch workspaces');
    }
    
    const data = await response.json();
    console.log('Workspaces:', data);
    
    //sample data structure {"workspaces":[{"id":"default","name":"default"}]}
    return NextResponse.json(data.workspaces || [], {
      headers: {
        'Cache-Control': 'no-store, max-age=0',
        'Pragma': 'no-cache'
      }
    });
  } catch (error) {
    console.error('Error fetching workspaces:', error);
    return NextResponse.json({ message: 'Error fetching workspaces' });
  }
}

export async function POST(request: Request) {
  try {
    const body = await request.json();
    console.log('Creating workspace...', body);
    
    const response = await fetch(`${config.apiBaseUrl}/workspaces`, {
      method: 'POST',
      headers: {
        'X-API-Key': config.apiKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      console.error('Error response from API:', errorData);
      return NextResponse.json(errorData, { status: response.status });
    }
    
    const data = await response.json();
    console.log('Workspace created:', data);
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error creating workspace:', error);
    return NextResponse.json({ error: '创建工作区失败' }, { status: 500 });
  }
}

export async function DELETE(request: Request) {
  try {
    // 从查询参数中获取workspace名称
    const url = new URL(request.url);
    const workspaceId = url.searchParams.get('workspace');
    
    if (!workspaceId) {
      return NextResponse.json({ error: '未提供工作区ID' }, { status: 400 });
    }
    
    console.log(`Deleting workspace: ${workspaceId}`);
    
    // 使用查询参数向后端发送请求
    const response = await fetch(`${config.apiBaseUrl}/workspaces?workspace=${workspaceId}`, {
      method: 'DELETE',
      headers: {
        'X-API-Key': config.apiKey,
        'Content-Type': 'application/json'
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: '删除工作区失败' }));
      console.error('Error response from API:', errorData);
      return NextResponse.json(errorData, { status: response.status });
    }
    
    const data = await response.json();
    console.log('Workspace deleted:', data);
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error deleting workspace:', error);
    return NextResponse.json({ error: '删除工作区失败' }, { status: 500 });
  }
}
import { NextResponse } from 'next/server';
import config from '@/config';

export async function GET() {
  try {
    console.log('Fetching workspaces...' + `${config.apiBaseUrl}/workspaces`);
    const response = await fetch(`${config.apiBaseUrl}/workspaces`, {
      cache: 'no-store',
      headers: {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
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
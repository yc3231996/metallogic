import { NextRequest, NextResponse } from 'next/server';
import config from '@/config';

export async function GET(request: NextRequest, { params }: { params: { workspace: string } }) {
    const { workspace } = params;
    try {
      console.log('Fetching worksapce metadata...' + `${config.apiBaseUrl}/${workspace}/metadata`);
      const response = await fetch(`${config.apiBaseUrl}/${workspace}/metadata`, {
          cache: 'no-store',
          headers: {
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
          }
        });
  
      if (!response.ok) {
        throw new Error(`Failed to metadata for workspace ${workspace}`);
      }
  
      const data = await response.json();
      console.log('Workspace Metadata:', data);
      return NextResponse.json(data, {
          headers: {
            'Cache-Control': 'no-store, max-age=0',
            'Pragma': 'no-cache'
          }
        });
    } catch (error) {
      return NextResponse.json({ message: `Error fetching metadata for workspace ${workspace}` }, { status: 500 });
    }
  }
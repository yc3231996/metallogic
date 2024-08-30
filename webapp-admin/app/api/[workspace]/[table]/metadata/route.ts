import { NextRequest, NextResponse } from 'next/server';
import config from '@/config';

export async function GET(
  request: NextRequest,
  { params }: { params: { workspace: string; table: string } }
) {
  const { workspace, table } = params;

  try {
    console.log(`Fetching metadata for workspace ${workspace} and table ${table}...`);
    const response = await fetch(`${config.apiBaseUrl}/${workspace}/${table}/metadata`, {
      cache: 'no-store',
      headers: {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
      }
    });
    
    if (!response.ok) {
      throw new Error(`Failed to fetch metadata for workspace ${workspace} and table ${table}`);
    }
    
    const data = await response.json();
    console.log('Metadata:', data);
    
    return NextResponse.json(data, {
      headers: {
        'Cache-Control': 'no-store, max-age=0',
        'Pragma': 'no-cache'
      }
    });
  } catch (error) {
    console.error('Error fetching metadata:', error);
    return NextResponse.json({ message: 'Error fetching metadata' }, { status: 500 });
  }
}

export async function POST(
  request: NextRequest,
  { params }: { params: { workspace: string; table: string } }
) {
  const { workspace, table } = params;

  try {
    const body = await request.json();
    console.log(`Saving metadata for workspace ${workspace} and table ${table}...`);
    
    const response = await fetch(`${config.apiBaseUrl}/${workspace}/${table}/metadata`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
      },
      body: JSON.stringify(body)
    });

    if (!response.ok) {
      throw new Error(`Failed to save metadata for workspace ${workspace} and table ${table}`);
    }

    const data = await response.json();
    console.log('Saved metadata:', data);

    return NextResponse.json(data, {
      headers: {
        'Cache-Control': 'no-store, max-age=0',
        'Pragma': 'no-cache'
      }
    });
  } catch (error) {
    console.error('Error saving metadata:', error);
    return NextResponse.json({ message: 'Error saving metadata' }, { status: 500 });
  }
}
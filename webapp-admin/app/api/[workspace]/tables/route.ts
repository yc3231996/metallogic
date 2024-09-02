import { NextRequest, NextResponse } from 'next/server';
import config from '@/config';

export async function GET(request: NextRequest, { params }: { params: { workspace: string } }) {
  const { workspace } = params;
  try {
    console.log('Fetching tables...' + `${config.apiBaseUrl}/${workspace}/tables`);
    const response = await fetch(`${config.apiBaseUrl}/${workspace}/tables`, {
        cache: 'no-store',
        headers: {
          'Cache-Control': 'no-cache',
          'Pragma': 'no-cache',
          'X-API-Key': config.apiKey,
          'Content-Type': 'application/json'
        }
      });

    if (!response.ok) {
      throw new Error(`Failed to fetch tables for workspace ${workspace}`);
    }

    //sample data structure {"tables":["salesdata","productionplan","productionprogress","productionefficiency"]}
    const data = await response.json();
    return NextResponse.json(data.tables || [], {
        headers: {
          'Cache-Control': 'no-store, max-age=0',
          'Pragma': 'no-cache'
        }
      });
  } catch (error) {
    return NextResponse.json({ message: `Error fetching tables for workspace ${workspace}` }, { status: 500 });
  }
}
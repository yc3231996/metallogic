import { NextRequest, NextResponse } from 'next/server';
import config from '@/config';

export async function GET(
  request: NextRequest,
  { params }: { params: { workspace: string; table: string } }
) {
  const { workspace, table } = params;
  try {
    const response = await fetch(`${config.apiBaseUrl}/${workspace}/${table}/fields`, {
        cache: 'no-store',
        headers: {
          'Cache-Control': 'no-cache',
          'Pragma': 'no-cache',
          'X-API-Key': config.apiKey,
          'Content-Type': 'application/json'
        }
      });

    if (!response.ok) {
      throw new Error(`Failed to fetch fields for table ${table} in workspace ${workspace}`);
    }

    //sample data structure {"fields":[{"name":"id","type":"int","comment":"主键"},{"name":"name","type":"varchar","comment":"名称"},{"name":"date","type":"date","comment":"日期"}]}， it is 'comment' isntead of 'description'
    const data = await response.json();
    return NextResponse.json(data.fields || [], {
        headers: {
          'Cache-Control': 'no-store, max-age=0',
          'Pragma': 'no-cache'
        }
      });
  } catch (error) {
    return NextResponse.json(
      { message: `Error fetching fields for table ${table} in workspace ${workspace}` },
      { status: 500 }
    );
  }
}
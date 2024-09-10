import { NextRequest, NextResponse } from 'next/server';
import config from '@/config';

export async function GET(request: NextRequest, { params }: { params: { workspace: string } }) {
    const { workspace } = params;
    try {
        console.log('Fetching question_sql...' + `${config.apiBaseUrl}/${workspace}/question_sql`);
        const response = await fetch(`${config.apiBaseUrl}/${workspace}/question_sql`, {
            cache: 'no-store',
            headers: {
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'X-API-Key': config.apiKey,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`Failed to fetch question_sql for workspace ${workspace}`);
        }

        const data = await response.json();
        console.log('Question SQL data:', data);
        return NextResponse.json(data, {
            headers: {
                'Cache-Control': 'no-store, max-age=0',
                'Pragma': 'no-cache'
            }
        });
    } catch (error) {
        return NextResponse.json({ message: `Error fetching question_sql for workspace ${workspace}` }, { status: 500 });
    }
}
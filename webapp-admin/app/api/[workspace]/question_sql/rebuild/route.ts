import { NextRequest, NextResponse } from 'next/server';
import config from '@/config';

export async function POST(request: NextRequest, { params }: { params: { workspace: string } }) {
    const { workspace } = params;
    try {
        const body = await request.json();
        console.log('Rebuilding question_sql...' + `${config.apiBaseUrl}/${workspace}/question_sql/rebuild`);
        const response = await fetch(`${config.apiBaseUrl}/${workspace}/question_sql/rebuild`, {
            method: 'POST',
            headers: {
                'X-API-Key': config.apiKey,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        });

        if (!response.ok) {
            throw new Error(`Failed to rebuild question_sql for workspace ${workspace}`);
        }

        const data = await response.json();
        console.log('Question SQL rebuild result:', data);
        return NextResponse.json(data);
    } catch (error) {
        return NextResponse.json({ message: `Error rebuilding question_sql for workspace ${workspace}` }, { status: 500 });
    }
}
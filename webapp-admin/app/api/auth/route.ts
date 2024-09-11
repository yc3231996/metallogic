import { NextResponse } from 'next/server';
import config from '@/config';

export async function POST(request: Request) {
  const body = await request.json();
  const { username, password } = body;

  if (username === config.auth.username && password === config.auth.password) {
    return NextResponse.json({ success: true, token: `${username}_dummytoken` });
  } else {
    return NextResponse.json({ success: false, message: 'Invalid credentials' }, { status: 401 });
  }
}
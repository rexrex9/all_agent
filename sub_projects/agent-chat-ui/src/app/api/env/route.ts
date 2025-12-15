import { NextResponse } from 'next/server'

export async function GET(request: Request) {

  console.log('API Route Request - Current Environment Variables:');
  console.log('API_URL:', process.env.API_URL);
  console.log('ASSISTANT_ID:', process.env.ASSISTANT_ID);
  console.log('NEXT_PUBLIC_API_URL:', process.env.NEXT_PUBLIC_API_URL);
  console.log('NEXT_PUBLIC_ASSISTANT_ID:', process.env.NEXT_PUBLIC_ASSISTANT_ID);
//
  // 获取请求参数
  const url = new URL(request.url)
  const testParam = url.searchParams.get('test')
  
  return NextResponse.json({
    API_URL: process.env.API_URL || process.env.NEXT_PUBLIC_API_URL,
    ASSISTANT_ID: process.env.ASSISTANT_ID || process.env.NEXT_PUBLIC_ASSISTANT_ID,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    timestamp: new Date().toISOString(),
    testParam: testParam,
    nodeVersion: process.version
  })
}
export const dynamic = 'force-dynamic'; // 确保每次请求都重新获取

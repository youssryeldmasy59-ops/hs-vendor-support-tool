/**
 * Vercel Serverless Function: /api/triage
 * Handles vendor support ticket classification & AI triage securely with strict CORS and origin protection.
 */

const ALLOWED_ORIGINS = [
  'https://youssryeldmasy59-ops.github.io',
  'http://localhost:3000',
  'http://localhost:5173',
  'http://localhost:8080',
  'http://127.0.0.1:5500',
  'http://127.0.0.1:8080'
];

export default async function handler(req, res) {
  const origin = req.headers.origin || req.headers.referer || '';
  const isAllowed = ALLOWED_ORIGINS.some(o => origin.startsWith(o)) || !origin;
  const allowOriginHeader = (isAllowed && origin) ? origin : 'https://youssryeldmasy59-ops.github.io';

  // Secure CORS Headers
  res.setHeader('Access-Control-Allow-Credentials', 'true');
  res.setHeader('Access-Control-Allow-Origin', allowOriginHeader);
  res.setHeader('Access-Control-Allow-Methods', 'POST,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version, Authorization');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { text, context } = req.body || {};
    if (!text || text.trim() === '') {
      return res.status(400).json({ error: 'Missing text in request body' });
    }

    const apiKey = process.env.OPENAI_API_KEY;
    if (!apiKey) {
      return res.status(500).json({ error: 'OPENAI_API_KEY environment variable is not configured on server' });
    }

    const systemPrompt = `You are an expert AI Support Specialist for the "Vendor Support Portal".
Your task is to analyze the vendor ticket and return a strictly valid JSON response without markdown:
{
  "category": "Authentication | Payments | Technical | Operations",
  "priority": "Low | Medium | High | Urgent",
  "sentiment": "Positive | Neutral | Frustrated",
  "summary": "ملخص المشكلة في 5 إلى 10 كلمات باللغة العربية",
  "recommended_action": "إجراء فوري مقترح لفريق الدعم"
}

Context Knowledge:
${context || "HungerStation Vendor Portal Support Guidelines"}
`;

    const openAiResponse = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: process.env.OPENAI_MODEL || 'gpt-4o-mini',
        response_format: { type: 'json_object' },
        temperature: 0.2,
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: text }
        ]
      })
    });

    if (!openAiResponse.ok) {
      const errDetail = await openAiResponse.text();
      return res.status(openAiResponse.status).json({ error: 'OpenAI API request failed', details: errDetail });
    }

    const data = await openAiResponse.json();
    const parsedData = JSON.parse(data.choices[0].message.content);
    return res.status(200).json(parsedData);
  } catch (error) {
    return res.status(500).json({ error: error.message || 'Server error' });
  }
}

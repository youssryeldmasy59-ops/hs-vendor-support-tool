/**
 * Cloudflare Worker - Vendor Support Tool AI Middleware Proxy
 * Secures OPENAI_API_KEY & GEMINI_API_KEY away from client-side code and GitHub Pages.
 */

const ALLOWED_ORIGINS = [
  'https://youssryeldmasy59-ops.github.io',
  'http://localhost:3000',
  'http://localhost:5173',
  'http://localhost:8080',
  'http://127.0.0.1:5500',
  'http://127.0.0.1:8080'
];

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || request.headers.get("Referer") || "";
    const isAllowed = ALLOWED_ORIGINS.some(o => origin.startsWith(o)) || (env.ALLOWED_ORIGIN && origin.startsWith(env.ALLOWED_ORIGIN));
    const activeAllowedOrigin = isAllowed && origin ? origin : (env.ALLOWED_ORIGIN || "https://youssryeldmasy59-ops.github.io");

    const corsHeaders = {
      "Access-Control-Allow-Origin": activeAllowedOrigin,
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders });
    }

    if (request.method !== "POST") {
      return new Response(JSON.stringify({ error: "Method not allowed" }), {
        status: 405,
        headers: { ...corsHeaders, "Content-Type": "application/json" }
      });
    }

    try {
      const payload = await request.json();
      const { text, action, provider, context } = payload;

      if (!text || text.trim() === "") {
        return new Response(JSON.stringify({ error: "No text provided" }), {
          status: 400,
          headers: { ...corsHeaders, "Content-Type": "application/json" }
        });
      }

      // --- GEMINI PROXY ACTION ---
      if (action === "gemini" || provider === "gemini") {
        const geminiKey = env.GEMINI_API_KEY;
        if (!geminiKey) {
          return new Response(JSON.stringify({ error: "Missing GEMINI_API_KEY in worker secrets" }), {
            status: 500,
            headers: { ...corsHeaders, "Content-Type": "application/json" }
          });
        }

        const model = env.GEMINI_MODEL || "gemini-2.0-flash";
        const geminiEndpoint = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${geminiKey}`;
        
        const geminiRes = await fetch(geminiEndpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            contents: [{ parts: [{ text: text }] }],
            generationConfig: {
              temperature: payload.temperature ?? 0.2,
              maxOutputTokens: payload.maxOutputTokens ?? 800
            }
          })
        });

        if (!geminiRes.ok) {
          const errTxt = await geminiRes.text();
          return new Response(JSON.stringify({ error: "Gemini API Error", details: errTxt }), {
            status: geminiRes.status,
            headers: { ...corsHeaders, "Content-Type": "application/json" }
          });
        }

        const geminiData = await geminiRes.json();
        return new Response(JSON.stringify(geminiData), {
          status: 200,
          headers: { ...corsHeaders, "Content-Type": "application/json" }
        });
      }

      // --- OPENAI TRIAGE ACTION (Default) ---
      const apiKey = env.OPENAI_API_KEY;
      if (!apiKey) {
        return new Response(JSON.stringify({ error: "Missing OPENAI_API_KEY in worker secrets" }), {
          status: 500,
          headers: { ...corsHeaders, "Content-Type": "application/json" }
        });
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

      const response = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${apiKey}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: env.OPENAI_MODEL || "gpt-4o-mini",
          response_format: { type: "json_object" },
          temperature: 0.2,
          messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: text }
          ]
        })
      });

      if (!response.ok) {
        const errorText = await response.text();
        return new Response(JSON.stringify({ error: "OpenAI API Error", details: errorText }), {
          status: response.status,
          headers: { ...corsHeaders, "Content-Type": "application/json" }
        });
      }

      const data = await response.json();
      const triageResult = JSON.parse(data.choices[0].message.content);

      return new Response(JSON.stringify(triageResult), {
        status: 200,
        headers: { ...corsHeaders, "Content-Type": "application/json" }
      });
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message || "Internal server error" }), {
        status: 500,
        headers: { ...corsHeaders, "Content-Type": "application/json" }
      });
    }
  }
};

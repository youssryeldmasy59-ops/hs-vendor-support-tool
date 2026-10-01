/**
 * Cloudflare Worker - Vendor Support Tool AI Middleware Proxy
 * Secures OPENAI_API_KEY / Groq / Anthropic API keys away from GitHub Pages.
 */

export default {
  async fetch(request, env) {
    const allowedOrigin = env.ALLOWED_ORIGIN || "*";
    const corsHeaders = {
      "Access-Control-Allow-Origin": allowedOrigin,
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type, Authorization",
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
      const { text, action, context } = await request.json();

      if (!text || text.trim() === "") {
        return new Response(JSON.stringify({ error: "No text provided" }), {
          status: 400,
          headers: { ...corsHeaders, "Content-Type": "application/json" }
        });
      }

      const apiKey = env.OPENAI_API_KEY;
      if (!apiKey) {
        return new Response(JSON.stringify({ error: "Missing OPENAI_API_KEY in worker secrets" }), {
          status: 500,
          headers: { ...corsHeaders, "Content-Type": "application/json" }
        });
      }

      // Triage / Analysis Action
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

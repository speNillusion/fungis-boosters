import express from "express";
import fetch from "node-fetch";
import "dotenv/config";
import https from "https";
import { JSDOM } from "jsdom";
const app = express();
app.use(express.json());

// --- Environment variables (required) ---
const REALM = process.env.REALM;
const CLIENT_ID = process.env.CLIENT_ID;
const CLIENT_SECRET = process.env.CLIENT_SECRET;

// Validate required environment variables
if (!REALM || !CLIENT_ID || !CLIENT_SECRET) {
  console.error('❌ Missing required environment variables:');
  if (!REALM) console.error('  - REALM');
  if (!CLIENT_ID) console.error('  - CLIENT_ID');
  if (!CLIENT_SECRET) console.error('  - CLIENT_SECRET');
  console.error('\n📝 Please set these variables in your environment or .env file');
  process.exit(1);
}

let JWT = "";
let tokenExpiry = 0;

async function authenticate() {
  const authUrl = `https://idm.stackspot.com/${REALM}/oidc/oauth/token`;
  const authPayload = new URLSearchParams({
    grant_type: "client_credentials",
    client_id: CLIENT_ID,
    client_secret: CLIENT_SECRET,
  });
  const authHeaders = {
    "Content-Type": "application/x-www-form-urlencoded",
  };

  const response = await fetch(authUrl, {
    method: "POST",
    body: authPayload,
    headers: authHeaders,
  });

  if (!response.ok) {
    throw new Error(`Authentication failed: ${response.statusText}`);
  }

  const data = await response.json();
  JWT = data.access_token;
  tokenExpiry = Date.now() + (data.expires_in - 60) * 1000; // refresh 1 min early
}

async function ensureValidToken() {
  if (!JWT || Date.now() >= tokenExpiry) {
    await authenticate();
  }
}

async function searchGoogle(query) {
  const url = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
  const headers = {
    "User-Agent":
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
  };
  const response = await fetch(url, { headers });
  if (!response.ok) throw new Error("Google search failed");
  const html = await response.text();
  const dom = new JSDOM(html);
  const anchors = Array.from(dom.window.document.querySelectorAll("a"));
  for (const a of anchors) {
    const href = a.href;
    if (href && href.startsWith("/url?q=")) {
      const realUrl = href.split("/url?q=")[1].split("&")[0];
      if (realUrl && !realUrl.includes("google")) return realUrl;
    }
  }
  return null;
}

async function fetchDocumentText(url) {
  const response = await fetch(url, {
    agent: new https.Agent({ rejectUnauthorized: false }),
  });
  if (!response.ok) throw new Error("Cannot fetch document");
  const html = await response.text();
  const dom = new JSDOM(html);
  return dom.window.document.body.textContent || "";
}

async function askStackspot(prompt) {
  await ensureValidToken();
  const qUrl = "https://genai-code-buddy-api.stackspot.com/v3/chat";
  const qPayload = {
    context: {
      conversation_id: "01K6T6JHQ9B6185BB7CC1S6472",
      knowledge_sources: ["01K6SZYH93MQW6BKFJ7VF5K2KX"],
      upload_ids: [],
      agent_id: "01K6SZ1GGPBT6MV0C8GNWN0XQ7",
      agent_built_in: false,
      os: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
      platform: "web-widget",
      platform_version:
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
      stackspot_ai_version: "2.0.0",
    },
    user_prompt: prompt,
  };
  const headers = {
    Authorization: `Bearer ${JWT}`,
    "Content-Type": "application/json",
  };
  const response = await fetch(qUrl, {
    method: "POST",
    headers,
    body: JSON.stringify(qPayload),
  });
  if (!response.ok) throw new Error("Stackspot API failed");
  return new Promise((resolve, reject) => {
    let raw = "";
    let answer = "";
    response.body.on("data", (chunk) => {
      raw += chunk.toString();
      const lines = raw.split("\n");
      raw = lines.pop();
      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const str = line.substring(6);
          if (!str.trim()) continue;
          try {
            const parsed = JSON.parse(str);
            if (parsed.answer) answer += parsed.answer;
          } catch {}
        }
      }
    });
    response.body.on("end", () => resolve(answer));
    response.body.on("error", reject);
  });
}

// Health check
app.get("/health", (_req, res) => res.status(200).json({ status: "ok" }));

// Chat endpoint
app.post("/chat", async (req, res) => {
  const { prompt } = req.body;
  if (!prompt || typeof prompt !== "string") {
    return res.status(400).json({ error: "Missing or invalid 'prompt' field" });
  }
  try {
    const result = await askStackspot(prompt);
    res.json(result);
  } catch (err) {
    console.error("Chat error:", err);
    res.status(500).json({ error: "Internal server error" });
  }
});

// Graceful shutdown
process.on("SIGINT", () => {
  console.log("\nShutting down gracefully...");
  server.close(() => process.exit(0));
});

const PORT = process.env.PORT || 5000;
const server = app.listen(PORT, () =>
  console.log(`Server listening on port ${PORT}`)
);

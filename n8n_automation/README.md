# N8N Automation Workflows

This repository contains multiple n8n automation workflows and demo examples designed to streamline communication, customer support, content generation, and AI tooling integration.

## 📋 Table of Contents

- [Overview](#overview)
- [Workflows](#workflows)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [How to Execute Workflows](#how-to-execute-workflows)
- [Workflow Details](#workflow-details)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 Overview

This repository includes the following automation workflows (JSON exports):

1. **AI Voice Assistance** (`AI_voice_assitance.json`) - Telegram-based voice & text assistant that transcribes audio via OpenAI, runs through an LLM agent, and replies via Telegram (can optionally send emails).
2. **Birthday Wishes UI Agent** (`birthday_wishes_ui_agent.json`) - UI/chat-triggered agent that drafts and sends birthday wishes via Gmail using OpenAI.
3. **Email Automation** (`email_automation.json`) - Personalized thank you email generator using Google Sheets + OpenAI + Gmail.
4. **Email to Slack Automation** (`email_to_slack_automation.json`) - Customer support flow: fetch Gmail messages, parse and append tickets to Google Sheets, and post formatted Slack notifications.
5. **Image Analyser** (`image_analyser.json`) - Webhook-based image analysis using OpenAI vision; returns structured JSON analysis.
6. **MCP Demo** (`MCP_demo.json`) - Multi-tool demonstration workflow (MCP/agent + Google Drive/Sheets/Docs + Gmail + SerpAPI) showcasing tool orchestration.
7. **RAG Agent 2.0** (`rag_2.0.json`) - Retrieval-Augmented Generation pipeline using Google Drive, Pinecone vector store, OpenAI embeddings and LLM for question answering.
8. **Simple AI Agent Send Email** (`simple_AI_agent_send_email.json`) - Chat-triggered AI agent that composes and sends an email via Gmail.
9. **Slack Image Generation** (`slack_image_generation.json`) - Slack-triggered Gemini image generator that uploads the resulting image back to a channel.
10. **Slack Post Image Builder** (`slackPost_nano_banana_image_builder.json`) - Slack historical message-driven Gemini image builder; pulls message text then generates and uploads a promotional image.
11. **Telegram Trigger** (`telegram_trigger.json`) - Telegram-to-LLM reply flow: on Telegram message, send to LLM and reply with a generated response.

---

## 🔧 Workflows

### 1. Email Automation (`email_automation.json`)
**Assignment-1**: Automated guest follow-up system

**Purpose**: Send personalized thank you emails to Silver Nest homestay guests after their stay.

**Flow**:
```
Manual Trigger → Google Sheets → Edit Fields → OpenAI GPT-4 → Markdown → Gmail
```

### 2. Email to Slack Automation (`email_to_slack_automation.json`)
**Assignment-2**: Customer support ticketing system

**Purpose**: Convert customer emails into formatted Slack notifications and track tickets in Google Sheets.

**Flow**:
```
Manual Trigger → Gmail → Parse Email → Extract Data → Google Sheets → Slack
```

### 3. Slack Post Image Generator (`slackPost_nano_banana_image_builder.json`)
**Assignment-3**: AI-powered promotional content generator

**Purpose**: Generate professional promotional images from Slack channel messages using Google Gemini AI.

**Flow**:
```
Manual Trigger → Slack History → Google Gemini Image Generation → Slack Upload
```

### 4. AI Voice Assistance (`AI_voice_assitance.json`)
**Purpose**: Transcribe Telegram voice messages, process via OpenAI, reply via Telegram (can send notifications or emails).

**Flow**:
```
Telegram Trigger → Transcribe (OpenAI) / Text → LLM Agent → Reply via Telegram (optional Gmail)
```

### 5. Birthday Wishes UI Agent (`birthday_wishes_ui_agent.json`)
**Purpose**: Compose personalized birthday wishes using OpenAI and send via Gmail.

**Flow**:
```
Webhook/UI Chat Trigger → OpenAI Agent → Gmail Tool
```

### 6. Image Analyser (`image_analyser.json`)
**Purpose**: API endpoint / Webhook that accepts an image and returns structured analysis using OpenAI vision capabilities.

**Flow**:
```
Webhook → OpenAI Vision/Analyze Image → Code Transform → Respond to Webhook
```

### 7. MCP Demo (`MCP_demo.json`)
**Purpose**: Demonstration of multiple tools (MCP, SerpAPI, Drive/Sheets/Docs, Gmail) orchestrated via agent flows.

**Flow**:
```
Chat Trigger / MCP Client → Agent → Tool Integrations (Drive, Docs, Gmail, SerpAPI) → Outputs
```

### 8. RAG Agent 2.0 (`rag_2.0.json`)
**Purpose**: Retrieval-Augmented Generation flow for vectorizing documents and answering queries with Pinecone + OpenAI embeddings.

**Flow**:
```
Google Drive Trigger → Download → Split → Embeddings → Pinecone Store → Query via LLM
```

### 9. Simple AI Agent Send Email (`simple_AI_agent_send_email.json`)
**Purpose**: Minimal chat-based AI agent that composes and sends emails using Gmail.

**Flow**:
```
Chat Trigger → LLM Agent → Gmail Tool
```

### 10. Slack Image Generation (`slack_image_generation.json`)
**Purpose**: Realtime Slack mention-triggered Gemini image generation; uploads the generated image in the channel.

**Flow**:
```
Slack Trigger → Google Gemini Image Generation → Upload File to Slack
```

### 11. Telegram Trigger (`telegram_trigger.json`)
**Purpose**: Simple Telegram LLM reply flow: LLM chain processes messages and replies.

**Flow**:
```
Telegram Trigger → LLM Chain → OpenAI Chat Model → Reply via Telegram
```

---

## ✅ Prerequisites

### Required Accounts & Services

1. **N8N Instance** (Cloud or Self-hosted)
2. **Google Account** with:
   - Gmail API enabled
   - Google Sheets API enabled
3. **Slack Workspace** with:
   - OAuth2 App configured
   - Bot token with appropriate permissions
4. **OpenAI API Key** (for email_automation.json)
5. **Google Gemini API Key** (for slackPost_nano_banana_image_builder.json)

### N8N Node Requirements

Ensure the following N8N nodes are available:
- Gmail (OAuth2)
- Google Sheets (OAuth2)
- Slack (OAuth2)
- OpenAI/GPT
- Google Gemini
- Code (JavaScript)
- Markdown
- Manual Trigger

**Important — use your own credentials:**
- These workflows include references to external services (Google, Slack, OpenAI, Gemini, Telegram, etc.). You must create and use your own API keys and OAuth credentials in your n8n instance. Do NOT commit or share secret keys. Replace any placeholder values in nodes with your own credentials after importing the workflows.

---

## 🚀 Setup Instructions

### Step 1: Google Sheets Configuration

#### For Email Automation (Assignment-1)

Create a Google Sheet named `trigger_email` with the following structure:

| Customer Name | Email ID |
|--------------|----------|
| John Doe | john@example.com |
| Jane Smith | jane@example.com |

**Column Details:**
- `Customer Name`: Guest's full name
- `Email ID`: Guest's email address

**Sheet URL Format**: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`

---

#### For Email to Slack Automation (Assignment-2)

Create a Google Sheet named `n8n_automation_user_tickets` with the following structure:

| TicketID | CreatedAt | From | FromEmail | Subject | Snippet | Body | Status |
|----------|-----------|------|-----------|---------|---------|------|--------|
| 20251206001 | 2025-12-06 | John Doe | john@example.com | Login Issue | Can't access... | Full description | P1 / Open |

**Column Details:**
- `TicketID`: Unique identifier (auto-generated: YYYYMMDD + sequence)
- `CreatedAt`: Ticket creation date (YYYY-MM-DD format)
- `From`: Customer name extracted from email
- `FromEmail`: Customer email address
- `Subject`: Email subject line
- `Snippet`: Short preview of the issue
- `Body`: Complete issue description
- `Status`: Priority and status (e.g., "P1 / Open", "P2 / Open")

**Sheet URL Format**: `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit`

---

### Step 2: Import Workflows to N8N

1. Open your n8n instance and click **Workflows** in the left sidebar.
2. Click **Import** → **Import from File** (or **Import from URL** if you host the JSON files remotely).
3. Select one or more JSON files from this repository to import. Files available:
    - `AI_voice_assitance.json`
    - `birthday_wishes_ui_agent.json`
    - `email_automation.json`
    - `email_to_slack_automation.json`
    - `image_analyser.json`
    - `MCP_demo.json`
    - `rag_2.0.json`
    - `simple_AI_agent_send_email.json`
    - `slack_image_generation.json`
    - `slackPost_nano_banana_image_builder.json`
    - `telegram_trigger.json`
4. Click **Import** to add the workflow(s) to your n8n workspace.
5. After import, open each workflow and configure credentials for nodes that require them (Gmail, Google Sheets, Slack, OpenAI, Google Gemini, Telegram, etc.).

Tips after importing:
- Use **Credential > Create New** within each node to add your own OAuth/key credentials.
- For Google APIs, ensure the service account or OAuth user has access to the target spreadsheets and Gmail.
- For Slack workflows, install or invite the bot to target channels and copy the bot token into n8n credentials.
- For OpenAI / Gemini, add API keys under the respective credential types in n8n.
- If a node references a `documentId`, `channelId`, or other resource ID, update it to your own resource identifiers.

---

### Step 3: Configure Credentials

#### Gmail OAuth2
1. Navigate to node requiring Gmail
2. Click **"Create New Credential"**
3. Select **"Gmail OAuth2 API"**
4. Follow Google OAuth2 setup wizard
5. Grant required permissions:
   - Read emails
   - Send emails
   - Modify labels

#### Google Sheets OAuth2
1. Navigate to Google Sheets node
2. Click **"Create New Credential"**
3. Select **"Google Sheets OAuth2 API"**
4. Authorize with your Google account
5. Grant spreadsheet access permissions

#### Slack OAuth2
1. Go to [Slack API](https://api.slack.com/apps)
2. Create a new app or select existing
3. Configure OAuth scopes:
   - `channels:history`
   - `channels:read`
   - `chat:write`
   - `files:write`
4. Install app to workspace
5. Copy OAuth token to N8N credential

#### OpenAI API
1. Get API key from [OpenAI Platform](https://platform.openai.com/)
2. Add credential in N8N
3. Paste API key

#### Google Gemini API
1. Get API key from [Google AI Studio](https://makersuite.google.com/)
2. Add credential in N8N
3. Paste API key

---

### Step 4: Update Node Configurations

#### Email Automation Workflow

**Google Sheets Node:**
- Update `documentId` with your `trigger_email` sheet ID
- Verify sheet name is `Sheet1` or update accordingly

**Gmail Node:**
- Update sender name: `"GenAI4Titans Team"` (optional)
- Verify email template formatting

**OpenAI Node:**
- Update system prompt if needed
- Verify model: `gpt-4.1-mini`

---

#### Email to Slack Automation Workflow

**Gmail Node:**
- Update sender filter: `"kandas22@gmail.com"` → your monitored email
- Adjust limit if needed (default: 1)

**Google Sheets Node:**
- Update `documentId` with your `n8n_automation_user_tickets` sheet ID
- Verify column mappings match sheet headers

**Slack Node:**
- Update `channelId` to your target channel
- Customize Slack block layout (optional)

**Code Nodes:**
- Review JavaScript parsing logic
- Adjust field extraction if email format differs

---

#### Slack Image Generator Workflow

**Slack History Node:**
- Update `channelId` to monitor target channel
- Adjust limit for message history

**Google Gemini Node:**
- Update image generation prompt if needed
- Verify model: `gemini-2.5-flash-image`

**Slack Upload Node:**
- Update `channelId` for image posting
- Customize file title/name

---

## ▶️ How to Execute Workflows

After importing and configuring credentials, follow these steps to run any workflow in this repo:

1. Open the imported workflow in the n8n editor.
2. Verify and attach credentials for each node that requires them (Credentials → Create New). Always use your own API keys/OAuth — do not commit or share secrets.
3. Update resource IDs and paths in nodes (examples: `documentId`, `sheetName`, `channelId`, `fileId`, webhook `path`).
4. Run a test:
    - If workflow contains a Manual Trigger: click **Execute Workflow** or trigger the Manual node.
    - If workflow uses a platform trigger (Slack/Telegram/GDrive): perform the external action (post a message, send a Telegram message, upload a file) or use the trigger's test utility.
    - For webhook workflows, send a test POST with `curl`:

```bash
curl -X POST "https://<your-n8n-host>/webhook/<your-webhook-path>" \
   -H 'Content-Type: application/json' \
   -d '{"test":"data"}'
```

5. Inspect the execution in n8n's Execution List, correct node errors, and re-run tests until successful.
6. Toggle the workflow to **Active** when ready for production.

Quick run notes for each workflow (after import & credentials):

- `AI_voice_assitance.json` — attach Telegram/OpenAI creds; send a Telegram message to test.
- `birthday_wishes_ui_agent.json` — attach OpenAI and Gmail creds; POST to webhook or use chat trigger to generate/send test email.
- `email_automation.json` — set Google Sheets `documentId`, attach Google Sheets/Gmail/OpenAI creds; run Manual Trigger to send sample email.
- `email_to_slack_automation.json` — attach Gmail/Google Sheets/Slack creds; send a test email to the monitored Gmail and execute the workflow.
- `image_analyser.json` — attach OpenAI creds; POST a base64/binary image to the webhook to test analysis and response.
- `MCP_demo.json` — attach needed tool creds (OpenAI, Google Drive/Sheets/Docs, Gmail); use chat triggers or MCP client endpoints for testing.
- `rag_2.0.json` — attach Pinecone, Google Drive, and OpenAI creds; upload documents to the watched Drive folder and query the RAG agent.
- `simple_AI_agent_send_email.json` — attach OpenAI and Gmail creds; use chat trigger to instruct the agent to send a test email.
- `slack_image_generation.json` — attach Slack and Gemini creds; mention the bot or post in the configured channel to generate/upload images.
- `slackPost_nano_banana_image_builder.json` — attach Gemini and Slack creds; run or post a message in the channel to generate images.
- `telegram_trigger.json` — attach Telegram/OpenAI creds and message the bot to test the reply flow.

Important: credentials are intentionally not embedded in these JSON files. Create credentials in the n8n UI and attach them to nodes after importing.

---

## ✅ Post-import Checklist
Follow this checklist immediately after importing a workflow to avoid runtime errors:

- **Replace placeholders**: Search each imported workflow for placeholder values and replace with your resource identifiers:
   - `<YOUR_SPREADSHEET_ID>` for Google Sheets `documentId`
   - `<YOUR_CHANNEL_ID>` for Slack `channelId`
   - `<YOUR_DRIVE_FOLDER_ID>` for Google Drive folder watches
   - `<YOUR_WEBHOOK_PATH>` for webhook nodes (if present)
   - `<YOUR_MONITORED_EMAIL>` for Gmail sender filters
- **Create credentials** in n8n for each external service (Gmail, Google Sheets, Slack, OpenAI, Google Gemini, Telegram, Pinecone, SerpAPI) and attach them to the corresponding nodes.
- **Run node-level tests**: For OAuth nodes, use the built-in credential test (Authorize account) where available; ensure permissions/scopes match required actions.
- **Execute a quick end-to-end test**: Use a single sample input (send test email, post Slack message, or POST to webhook) and follow the execution trace in n8n.
- **Inspect results and logs**: Fix any mapping (column names, JSON paths) or permission errors and re-run tests.

If you'd like, I can replace all remaining IDs and sample emails with placeholders (already done for major items) and provide a short validation script or sample `curl` payloads for webhook workflows.

---

## 🔧 Changes Made in This Repo
- Added all workflows (11 total) to **Overview** and **Workflow Details** with one-line descriptions and quick-run notes.
- Standardized top-level workflow names with `n8n_automation - ` prefix and added `n8n_meta` metadata to each JSON file.
- **Removed embedded credentials** from workflow JSONs (replaced with empty `credentials` objects) to avoid leaking secrets.
- Replaced key resource IDs (Google Sheet IDs, Slack channel IDs, Drive folder IDs, monitored email examples) with placeholders like `<YOUR_SPREADSHEET_ID>`, `<YOUR_CHANNEL_ID>`, `<YOUR_DRIVE_FOLDER_ID>`, and `<YOUR_MONITORED_EMAIL>`.

If you want, I can also create a small script that checks all JSON files for remaining credential ids and lists them for manual review.

---

## 📖 Workflow Details

### 1. Email Automation Workflow

**Use Case**: Post-stay guest engagement for Silver Nest homestay

**Process**:
1. Manual trigger starts workflow
2. Fetches guest data from Google Sheets (`trigger_email`)
3. Extracts `Customer Name` and `Email ID`
4. Sends data to OpenAI GPT-4 with hospitality-focused prompt
5. Generates personalized, formatted thank you email
6. Converts markdown to HTML
7. Sends email via Gmail with embedded image

**Customization Points**:
- Email template in OpenAI prompt
- Image URL in markdown node
- Sender name and subject line
- HTML formatting rules

---

### 2. Email to Slack Automation Workflow

**Use Case**: Customer support ticket automation

**Process**:
1. Manual trigger initiates workflow
2. Retrieves latest email from Gmail (filtered by sender)
3. **Code Node 1**: Parses sender information
   - Extracts email address from `From` field
   - Separates name and email
4. **Code Node 2**: Generates ticket data
   - Creates unique `TicketID` (YYYYMMDD format)
   - Extracts subject, snippet, body
   - Assigns priority/status
5. Appends ticket to Google Sheets (`n8n_automation_user_tickets`)
6. Formats and sends Slack notification with:
   - Ticket details
   - Action buttons
   - Professional layout

**Email Format Expected**:
```
From: John Doe <john@example.com>
Subject: Login Issue - Cannot Access Dashboard
Body: The user interface does not allow login...
```

**Slack Message Format**:
- Header: Email subject
- Fields: Customer name, email, ticket ID, priority
- Issue description
- Action buttons (View Ticket, Assign to Me)

---

### 3. Slack Image Generator Workflow

**Use Case**: Automated promotional content creation

**Process**:
1. Manual trigger starts workflow
2. Fetches latest message from Slack channel
3. Extracts message text
4. Sends to Google Gemini with prompt template:
   - "A high-impact, professional promotional poster design for a [MESSAGE TEXT]"
   - Optimized for digital media
5. Generates AI image
6. Uploads image to Slack channel with title: "GenAI4Titans Offers"

**Example Input**:
```
Slack message: "Summer Sale - 50% Off All Courses"
```

**Output**: Professional promotional poster uploaded to Slack

---

### 4. AI Voice Assistance Workflow

**Use Case**: Telegram voice/text assistant for fast conversational automation (auto-replies, email notifications).

**Process**:
1. Telegram Trigger receives message (voice or text)
2. If voice: Telegram Node `Get a file` -> OpenAI Transcribe (audio) -> set `text`
3. LLM Agent processes the `text` and optionally stores/retrieves memory
4. Workflow posts a reply back to Telegram; optionally uses Gmail to send messages

**Customization Points**:
- Model selection for transcription and chat
- Memory/session keys for multi-turn conversations
- Telegram webhook and bot configuration

---

### 5. Birthday Wishes UI Agent Workflow

**Use Case**: Generate and send birthday wishes.

**Process**:
1. Chat or webhook trigger invokes the agent
2. OpenAI agent drafts a personalized birthday message
3. Gmail tool sends the email using configured credentials

**Customization Points**:
- Prompt style and template
- Sender name and email formatting

---

### 6. Image Analyser Workflow

**Use Case**: Provide structured image insights for incoming images.

**Process**:
1. Webhook receives image (binary or base64)
2. OpenAI Image analysis runs over the binary input
3. Code node parses/normalizes the analysis to a simple JSON response
4. Webhook returns JSON to the caller

**Customization Points**:
- Adjust model and analyze options
- Response structure mapping

---

### 7. MCP Demo Workflow

**Use Case**: Demonstrates orchestration of tools and endpoints for custom AI pipelines.

**Process**:
1. Chat/MCP client triggers the workflow
2. Agent orchestrates calls to SerpAPI, Google Drive/Docs/Sheets, Gmail, and other tools
3. Returns outputs and triggers tool-specific actions

**Customization Points**:
- Which tools are active (toggle nodes)
- Endpoint/URL for MCP client

---

### 8. RAG Agent 2.0 Workflow

**Use Case**: Document ingestion & RAG queries with Pinecone + OpenAI embeddings.

**Process**:
1. Google Drive Trigger detects new documents
2. Download and split documents
3. Generate embeddings via OpenAI and insert into Pinecone
4. Client queries are handled via LLM using recent context from Pinecone

**Customization Points**:
- Splitting strategy & overlap
- Pinecone namespace and index settings

---

### 9. Simple AI Agent Send Email Workflow

**Use Case**: Minimal example of a chat-based agent that can perform an email send operation.

**Process**:
1. Chat trigger receives a request
2. Agent composes a subject and message
3. Gmail tool sends the message

---

### 10. Slack Image Generation Workflow

**Use Case**: Realtime image generation in response to Slack mentions.

**Process**:
1. Slack Th trigger or app mention
2. Gemini image generation creates the image
3. Upload file back to Slack channel or thread

---

### 11. Telegram Trigger Workflow

**Use Case**: Quick LLM reply flow for Telegram messages using a simple chain

**Process**:
1. Telegram trigger receives message
2. Chain LLM / OpenAI handles the prompt
3. Reply message is sent via Telegram node

---

## 🔍 Troubleshooting

### Common Issues

#### Google Sheets Not Found
**Error**: `Document not found`
**Solution**: 
- Verify sheet sharing permissions
- Ensure OAuth credentials have access
- Check `documentId` matches your sheet

#### Gmail Not Fetching Emails
**Error**: No emails retrieved
**Solution**:
- Check sender filter matches email address
- Verify Gmail OAuth permissions
- Ensure emails exist in inbox/spam

#### Slack Channel Access Denied
**Error**: `channel_not_found`
**Solution**:
- Invite bot to channel
- Verify `channelId` is correct
- Check OAuth scopes include `channels:read`

#### OpenAI/Gemini API Errors
**Error**: `Invalid API key` or `Rate limit exceeded`
**Solution**:
- Verify API key is active
- Check billing/quota limits
- Test credentials in N8N settings

#### Code Node Errors
**Error**: JavaScript execution failed
**Solution**:
- Review console logs in N8N
- Verify input data format matches expected structure
- Check variable references (e.g., `$json.From` exists)

---

## 🧪 Testing Workflows

### Test Email Automation
1. Add test data to `trigger_email` sheet
2. Click **"Execute Workflow"** in N8N
3. Verify email received with correct personalization
4. Check HTML formatting displays correctly

### Test Email to Slack Automation
1. Send test email to monitored Gmail address
2. Execute workflow manually
3. Verify:
   - Ticket added to Google Sheet
   - Slack notification posted
   - All fields populated correctly

### Test Slack Image Generator
1. Post a message in monitored Slack channel
2. Execute workflow
3. Verify:
   - Image generated matches message content
   - File uploaded to Slack
   - Image quality is acceptable

---

## 📊 Data Flow Diagrams

### Email Automation Flow
```
┌─────────────────┐
│ Google Sheets   │
│ (trigger_email) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ OpenAI GPT-4    │
│ (Email Gen)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Gmail Send      │
└─────────────────┘
```

### Email to Slack Flow
```
┌─────────────────┐
│ Gmail Inbox     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Parse & Extract │
└────────┬────────┘
         │
         ├────────────────┐
         ▼                ▼
┌─────────────────┐ ┌─────────────────┐
│ Google Sheets   │ │ Slack Channel   │
│ (Tickets)       │ │ (Notification)  │
└─────────────────┘ └─────────────────┘
```

### Image Generator Flow
```
┌─────────────────┐
│ Slack Message   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Google Gemini   │
│ (Image Gen)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Slack Upload    │
└─────────────────┘
```

---

## 🔐 Security Best Practices

1. **API Keys**: Store in N8N credentials manager (encrypted)
2. **OAuth Tokens**: Rotate periodically
3. **Sheet Permissions**: Grant minimum required access
4. **Email Filters**: Validate sender addresses
5. **Rate Limiting**: Monitor API usage quotas
6. **Logging**: Review execution logs for errors

---

## 📝 Notes

- All workflows use manual triggers by default
- Can be converted to schedule/webhook triggers
- Customize prompts and templates as needed
- Monitor API usage to avoid rate limits
- Test with sample data before production use

---

## 🤝 Contributing

To modify workflows:
1. Export workflow from N8N as JSON
2. Edit nodes and connections
3. Test thoroughly
4. Update this README with changes
5. Commit updated JSON files

---

## 📧 Support

For issues or questions:
- Check N8N execution logs
- Review node documentation
- Test credentials individually
- Verify Google Sheets structure matches specifications

---

## 📄 License

This project is for educational purposes as part of GenAI4Titans assignments.

---

## 🏷️ Tags

- Assignment-1: Email Automation
- Assignment-2: Email to Slack Automation
- Assignment-3: Slack Image Generator

---

**Last Updated**: December 6, 2025
**Version**: 1.0.0

# N8N Automation Workflows

This repository contains three N8N automation workflows designed to streamline communication, customer support, and promotional content generation.

## 📋 Table of Contents

- [Overview](#overview)
- [Workflows](#workflows)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Workflow Details](#workflow-details)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 Overview

This collection includes three automation workflows:

1. **Email Automation** - Automated thank you email system for homestay guests
2. **Email to Slack Automation** - Customer support ticket system with Gmail to Slack integration
3. **Slack Post Image Generator** - AI-powered promotional image generation from Slack messages

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

1. Open your N8N instance
2. Click on **"Workflows"** in the left sidebar
3. Click **"Import from File"** or **"Import from URL"**
4. Select the JSON file(s):
   - `email_automation.json`
   - `email_to_slack_automation.json`
   - `slackPost_nano_banana_image_builder.json`
5. Click **"Import"**

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

# Twilio WhatsApp Setup Guide

This guide shows you how to configure Twilio credentials for sending WhatsApp messages in the Streamlit app.

## 🔐 Three Methods to Set Credentials

### Method 1: Streamlit Secrets (Recommended for Production)

1. **Create/Edit `.streamlit/secrets.toml`** (already created):
   ```toml
   [twilio]
   ACCOUNT_SID = "your_account_sid_here"
   AUTH_TOKEN = "your_auth_token_here"
   WHATSAPP_FROM = "whatsapp:+14155238886"
   ```

2. **Add to `.gitignore`** (if not already):
   ```bash
   echo ".streamlit/secrets.toml" >> .gitignore
   ```

3. **Run Streamlit normally**:
   ```bash
   cd streamlit_assignment
   source .venv/bin/activate
   streamlit run src/kavihealthcare.py
   ```

✅ **Benefits**: Most secure, works on Streamlit Cloud, no terminal commands needed

---

### Method 2: Environment Variables via Shell Script

1. **Source the environment file**:
   ```bash
   cd streamlit_assignment
   source .env.sh
   ```

2. **Run Streamlit**:
   ```bash
   source .venv/bin/activate
   streamlit run src/kavihealthcare.py
   ```

✅ **Benefits**: Works for any Python script, good for local development

---

### Method 3: One-Command Script (Easiest)

Just run:
```bash
cd streamlit_assignment
./run_streamlit.sh
```

This script automatically:
- Loads environment variables from `.env.sh`
- Activates the virtual environment
- Runs Streamlit

✅ **Benefits**: One command does everything

---

## 🧪 Testing the Setup

### Test 1: Verify credentials are loaded

```bash
cd streamlit_assignment
source .env.sh
echo "Account SID: $TWILIO_ACCOUNT_SID"
echo "WhatsApp From: $TWILIO_WHATSAPP_FROM"
```

### Test 2: Test the WhatsApp sender module

```bash
cd streamlit_assignment/src
source ../.venv/bin/activate
export TEST_PHONE="+919711172197"
python whatsapp_sender.py
```

### Test 3: Run the full Streamlit app

```bash
cd streamlit_assignment
./run_streamlit.sh
```

Then:
1. Go to http://localhost:8502
2. Navigate to **Lab Tests** → **Print Report**
3. Enter a patient ID
4. Click **Send via WhatsApp**

---

## 🔧 Troubleshooting

### Issue: "Failed to upload PDF"

**Solution**: The app now uses 3 fallback PDF hosting services:
1. tmpfiles.org (most reliable)
2. 0x0.st (simple and fast)
3. file.io (fallback)

If all fail, check your internet connection.

### Issue: "Twilio API error"

**Possible causes**:
1. ❌ Wrong credentials → Check `.streamlit/secrets.toml` or `.env.sh`
2. ❌ Invalid phone number → Must include country code (e.g., `+919711172197`)
3. ❌ WhatsApp not enabled → Activate in Twilio Console
4. ❌ Sandbox not configured → Join sandbox or use Business API

**Solution**:
```bash
# Verify credentials
cd streamlit_assignment
source .env.sh
python -c "import os; print('SID:', os.getenv('TWILIO_ACCOUNT_SID')[:10] + '...'); print('From:', os.getenv('TWILIO_WHATSAPP_FROM'))"
```

### Issue: Streamlit doesn't see credentials

**Solution**: Make sure you're using ONE of these methods:

**Option A - Streamlit Secrets**:
```bash
# Credentials in .streamlit/secrets.toml
streamlit run src/kavihealthcare.py
```

**Option B - Environment Variables**:
```bash
# Load env vars first
source .env.sh
streamlit run src/kavihealthcare.py
```

**Option C - Use the script**:
```bash
# Automatically loads everything
./run_streamlit.sh
```

### Issue: "command not found: streamlit"

**Solution**: Activate virtual environment first:
```bash
cd streamlit_assignment
source .venv/bin/activate
streamlit run src/kavihealthcare.py
```

Or use the run script (does this automatically):
```bash
./run_streamlit.sh
```

---

## 📁 File Structure

```
streamlit_assignment/
├── .streamlit/
│   └── secrets.toml          # ✅ Streamlit secrets (Method 1)
├── .env.sh                    # ✅ Environment variables (Method 2)
├── run_streamlit.sh          # ✅ One-command script (Method 3)
├── .venv/                    # Virtual environment
├── src/
│   ├── kavihealthcare.py     # Main Streamlit app
│   └── whatsapp_sender.py    # ✅ Updated with multi-host support
└── requirements.txt
```

---

## 🚀 Quick Start (Choose One)

### Easiest Way (Script):
```bash
cd streamlit_assignment
./run_streamlit.sh
```

### Using Streamlit Secrets:
```bash
cd streamlit_assignment
source .venv/bin/activate
streamlit run src/kavihealthcare.py
```

### Using Environment Variables:
```bash
cd streamlit_assignment
source .env.sh
source .venv/bin/activate
streamlit run src/kavihealthcare.py
```

---

## 🔑 Getting Your Own Twilio Credentials

Currently using default test credentials. For production:

1. **Sign up**: https://www.twilio.com/try-twilio
2. **Get credentials**: Console → Account Info
3. **Enable WhatsApp**: Messaging → Try It Out → WhatsApp
4. **Update credentials**:
   - Edit `.streamlit/secrets.toml`, OR
   - Edit `.env.sh`

---

## 🌐 PDF Hosting Services Used

The app now tries multiple services in order:

| Service | Reliability | Expiration | Notes |
|---------|-------------|------------|-------|
| tmpfiles.org | ⭐⭐⭐⭐⭐ | 1 hour | Most reliable |
| 0x0.st | ⭐⭐⭐⭐ | Varies | Simple & fast |
| file.io | ⭐⭐⭐ | 1 download | Often rate-limited |

If all three fail, the error message will show which services were tried.

---

## 📝 Summary

✅ **Credentials configured** in `.streamlit/secrets.toml` and `.env.sh`  
✅ **Multiple PDF hosting** services with automatic fallback  
✅ **Easy run script** created: `./run_streamlit.sh`  
✅ **Works with both** Streamlit secrets and environment variables  

**Just run**: `./run_streamlit.sh` 🚀

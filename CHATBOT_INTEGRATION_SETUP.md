# Chatbot Lead Integration Setup Guide

Your chatbot now sends leads to **both Google Sheets and HubSpot**!

## 📊 What Data Gets Captured:

- **Name** (First & Last)
- **Email** (required)
- **Company Name**
- **Phone Number**
- **Timestamp**
- **Source** ("Website Chatbot")
- **Page URL** (where they submitted)
- **Conversation History** (last 5 messages for context)

---

## 🟢 Part 1: Google Sheets Setup

### Step 1: Create Your Google Sheet

1. Go to [Google Sheets](https://sheets.google.com)
2. Create a new spreadsheet named "Chatbot Leads"
3. Add these column headers in Row 1:
   - A1: `Name`
   - B1: `Email`
   - C1: `Company`
   - D1: `Phone`
   - E1: `Source`
   - F1: `Timestamp`
   - G1: `Page URL`
   - H1: `Conversation`

### Step 2: Create Google Apps Script

1. In your Google Sheet, click **Extensions** → **Apps Script**
2. Delete any existing code
3. Paste this code:

```javascript
function doPost(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    const data = JSON.parse(e.postData.contents);
    
    // Add row with lead data
    sheet.appendRow([
      data.name,
      data.email,
      data.company,
      data.phone,
      data.source,
      data.timestamp,
      data.page_url,
      data.conversation_history
    ]);
    
    return ContentService.createTextOutput(JSON.stringify({
      'status': 'success'
    })).setMimeType(ContentService.MimeType.JSON);
    
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      'status': 'error',
      'message': error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}
```

4. Click **Save** (💾 icon)
5. Click **Deploy** → **New deployment**
6. Click ⚙️ (gear icon) → Select **Web app**
7. Settings:
   - **Description**: "Chatbot Lead Capture"
   - **Execute as**: Me
   - **Who has access**: Anyone
8. Click **Deploy**
9. **Copy the Web App URL** (looks like: `https://script.google.com/macros/s/...../exec`)
10. Click **Authorize access** if prompted

### Step 3: Add URL to Your Website

In `index.html`, find this line (around line 1644):
```javascript
const GOOGLE_SCRIPT_URL = 'YOUR_GOOGLE_APPS_SCRIPT_URL_HERE';
```

Replace with your actual URL:
```javascript
const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/YOUR_ACTUAL_URL/exec';
```

---

## 🟠 Part 2: HubSpot Setup

### Step 1: Create a HubSpot Form

1. Log into [HubSpot](https://app.hubspot.com)
2. Go to **Marketing** → **Lead Capture** → **Forms**
3. Click **Create Form**
4. Choose **Embedded form**
5. Add these fields:
   - First Name (firstname)
   - Last Name (lastname)
   - Email (email)
   - Company Name (company)
   - Phone Number (phone)
   - Lead Source (lead_source) - Single-line text
   - Message (message) - Multi-line text
6. Click **Publish**

### Step 2: Get Your HubSpot Credentials

1. In the form editor, click on the form **Options** (⚙️)
2. Find your **Portal ID**:
   - Go to **Settings** (top right) → **Account Setup** → **Account Defaults**
   - Copy your **Hub ID** (looks like: `12345678`)

3. Find your **Form GUID**:
   - In your form, look at the URL or form settings
   - The GUID is a long string like: `a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6`
   - Or click **Share** → Look in the embed code for `formId`

### Step 3: Add Credentials to Your Website

In `index.html`, find these lines (around line 1672-1673):
```javascript
const HUBSPOT_PORTAL_ID = 'YOUR_HUBSPOT_PORTAL_ID';
const HUBSPOT_FORM_GUID = 'YOUR_HUBSPOT_FORM_GUID';
```

Replace with your actual values:
```javascript
const HUBSPOT_PORTAL_ID = '12345678';
const HUBSPOT_FORM_GUID = 'a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6';
```

---

## ✅ Step 4: Test Your Integration

1. **Commit and push** your changes to `dev` branch
2. Wait for GitHub Pages deployment
3. **Open your dev site**: https://raulmendesrosa-debug.github.io/verakore-prod/
4. **Click the chatbot**
5. **Ask**: "I want a quote" or "Contact sales"
6. **Fill out the form** with test data
7. **Check**:
   - Google Sheet for new row
   - HubSpot Contacts for new contact
   - Browser console for success messages

---

## 🔍 Troubleshooting

### Google Sheets Not Working?

- **Check Apps Script URL**: Make sure it ends with `/exec`
- **Check Permissions**: Redeploy and authorize again
- **Check Console**: Look for "Google Sheets error" in browser console
- **Check Sheet**: Make sure column headers match exactly

### HubSpot Not Working?

- **Check Portal ID**: Should be all numbers (8-9 digits)
- **Check Form GUID**: Should have dashes (UUID format)
- **Check Form Fields**: Field names must match exactly (firstname, lastname, email, etc.)
- **Check Console**: Look for "HubSpot error" in browser console
- **Check HubSpot**: Go to Contacts → check if contact was created

### Both Failing?

- **Check Browser Console**: Look for error messages
- **Check Network Tab**: See if requests are being sent
- **Test with Postman**: Send test data directly to URLs
- **Check CORS**: Make sure Google Script allows "Anyone" access

---

## 📊 What You'll See:

### Google Sheets:
Every lead creates a new row with all data in columns.

### HubSpot:
- Creates new contact (or updates existing)
- Sets lead source to "Website Chatbot"
- Adds conversation history to "Message" field
- You can then trigger workflows, assign to sales, etc.

---

## 🎯 Next Steps:

### In HubSpot:
1. Create a **Workflow** triggered by "Lead Source = Website Chatbot"
2. **Assign** to sales rep
3. **Send email** notification
4. **Add to sequence** for follow-up

### In Google Sheets:
1. **Add formulas** for analysis
2. **Create charts** for lead tracking
3. **Set up email notifications** (Google Apps Script)
4. **Export** for other tools

---

## 💡 Pro Tips:

- **Test thoroughly** before deploying to production
- **Monitor both systems** for the first few days
- **Set up HubSpot notifications** so you don't miss leads
- **Review conversation history** to improve chatbot responses
- **Add more fields** if needed (just update both integrations)

---

Need help? Contact your development team or reach out with questions! 🚀


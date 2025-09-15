# Verakore Website API Implementation Guide

## 🎯 API Requirements for Verakore

### **Core API Endpoints Needed:**
1. **Contact Form API** - `/api/contact`
2. **Careers Application API** - `/api/careers`
3. **Quote Request API** - `/api/quote`
4. **Meeting Scheduler API** - `/api/schedule`
5. **Service Inquiry API** - `/api/services`

## 🔧 Implementation Options

### **Option 1: Netlify Functions (Recommended for Netlify)**
```javascript
// netlify/functions/contact.js
exports.handler = async (event, context) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }
  
  try {
    const { name, email, company, phone, service, message } = JSON.parse(event.body);
    
    // Send email via SendGrid
    const emailData = {
      to: 'info@verakore.com',
      from: 'noreply@verakore.com',
      subject: `New Contact Form Submission from ${name}`,
      html: `
        <h2>New Contact Form Submission</h2>
        <p><strong>Name:</strong> ${name}</p>
        <p><strong>Email:</strong> ${email}</p>
        <p><strong>Company:</strong> ${company || 'Not provided'}</p>
        <p><strong>Phone:</strong> ${phone || 'Not provided'}</p>
        <p><strong>Service Interest:</strong> ${service}</p>
        <p><strong>Message:</strong></p>
        <p>${message}</p>
      `
    };
    
    // Send email (implement with your email service)
    await sendEmail(emailData);
    
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ success: true, message: 'Thank you for your message!' })
    };
    
  } catch (error) {
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to send message' })
    };
  }
};
```

### **Option 2: Cloudflare Workers (Recommended for Cloudflare Pages)**
```javascript
// workers/contact.js
export default {
  async fetch(request) {
    const { method, url } = request;
    
    if (method === 'POST' && url.includes('/api/contact')) {
      try {
        const data = await request.json();
        const { name, email, company, phone, service, message } = data;
        
        // Send email via Cloudflare Email Workers or external service
        await sendEmail({
          to: 'info@verakore.com',
          subject: `New Contact Form Submission from ${name}`,
          body: `Name: ${name}\nEmail: ${email}\nCompany: ${company}\nPhone: ${phone}\nService: ${service}\nMessage: ${message}`
        });
        
        return new Response(JSON.stringify({ 
          success: true, 
          message: 'Thank you for your message!' 
        }), {
          headers: { 'Content-Type': 'application/json' }
        });
        
      } catch (error) {
        return new Response(JSON.stringify({ 
          error: 'Failed to send message' 
        }), { 
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }
    
    return new Response('Not Found', { status: 404 });
  }
};
```

### **Option 3: External API Services**

#### **Formspree Integration:**
```html
<!-- Replace Netlify form with Formspree -->
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
  <input type="text" name="name" required>
  <input type="email" name="email" required>
  <textarea name="message" required></textarea>
  <button type="submit">Send Message</button>
</form>
```

#### **Airtable for Careers Database:**
```javascript
// Store job applications in Airtable
const AIRTABLE_API_KEY = 'your_airtable_api_key';
const AIRTABLE_BASE_ID = 'your_base_id';
const AIRTABLE_TABLE_NAME = 'Job Applications';

async function submitApplication(applicationData) {
  const response = await fetch(`https://api.airtable.com/v0/${AIRTABLE_BASE_ID}/${AIRTABLE_TABLE_NAME}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${AIRTABLE_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      fields: {
        'Name': applicationData.name,
        'Email': applicationData.email,
        'Phone': applicationData.phone,
        'Position': applicationData.position,
        'Experience': applicationData.experience,
        'Resume': applicationData.resume,
        'Cover Letter': applicationData.coverLetter,
        'Date Submitted': new Date().toISOString()
      }
    })
  });
  
  return response.json();
}
```

## 📧 Email Service Integration

### **SendGrid Setup:**
```javascript
const sgMail = require('@sendgrid/mail');
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

async function sendEmail(emailData) {
  const msg = {
    to: emailData.to,
    from: emailData.from,
    subject: emailData.subject,
    html: emailData.html
  };
  
  try {
    await sgMail.send(msg);
    console.log('Email sent successfully');
  } catch (error) {
    console.error('Error sending email:', error);
    throw error;
  }
}
```

### **Mailgun Setup:**
```javascript
const mailgun = require('mailgun-js')({
  apiKey: process.env.MAILGUN_API_KEY,
  domain: process.env.MAILGUN_DOMAIN
});

async function sendEmail(emailData) {
  const data = {
    from: emailData.from,
    to: emailData.to,
    subject: emailData.subject,
    html: emailData.html
  };
  
  try {
    const result = await mailgun.messages().send(data);
    console.log('Email sent:', result);
  } catch (error) {
    console.error('Error sending email:', error);
    throw error;
  }
}
```

## 🗄️ Database Options

### **Supabase (PostgreSQL):**
```javascript
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_ANON_KEY
);

// Store contact form submissions
async function storeContactSubmission(data) {
  const { data: result, error } = await supabase
    .from('contact_submissions')
    .insert([
      {
        name: data.name,
        email: data.email,
        company: data.company,
        phone: data.phone,
        service: data.service,
        message: data.message,
        created_at: new Date().toISOString()
      }
    ]);
    
  if (error) throw error;
  return result;
}
```

### **Firebase Firestore:**
```javascript
import { initializeApp } from 'firebase/app';
import { getFirestore, collection, addDoc } from 'firebase/firestore';

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

async function storeContactSubmission(data) {
  try {
    const docRef = await addDoc(collection(db, 'contact_submissions'), {
      name: data.name,
      email: data.email,
      company: data.company,
      phone: data.phone,
      service: data.service,
      message: data.message,
      timestamp: new Date()
    });
    
    console.log('Document written with ID: ', docRef.id);
    return docRef.id;
  } catch (error) {
    console.error('Error adding document: ', error);
    throw error;
  }
}
```

## 🔒 Security Considerations

### **API Security Best Practices:**
1. **Rate Limiting** - Prevent spam and abuse
2. **Input Validation** - Sanitize all inputs
3. **CORS Configuration** - Control cross-origin requests
4. **Authentication** - Secure admin endpoints
5. **Data Encryption** - Encrypt sensitive data
6. **Logging** - Monitor API usage

### **Rate Limiting Example:**
```javascript
// Netlify Functions rate limiting
const rateLimit = new Map();

function checkRateLimit(ip) {
  const now = Date.now();
  const windowMs = 15 * 60 * 1000; // 15 minutes
  const maxRequests = 5;
  
  if (!rateLimit.has(ip)) {
    rateLimit.set(ip, { count: 1, resetTime: now + windowMs });
    return true;
  }
  
  const userLimit = rateLimit.get(ip);
  
  if (now > userLimit.resetTime) {
    rateLimit.set(ip, { count: 1, resetTime: now + windowMs });
    return true;
  }
  
  if (userLimit.count >= maxRequests) {
    return false;
  }
  
  userLimit.count++;
  return true;
}
```

## 🎯 Recommended Implementation Plan

### **Phase 1: Contact Form API**
1. **Choose hosting platform** (Netlify Functions or Cloudflare Workers)
2. **Set up email service** (SendGrid or Mailgun)
3. **Implement contact form API**
4. **Test and deploy**

### **Phase 2: Careers Database**
1. **Set up database** (Supabase or Airtable)
2. **Create careers application API**
3. **Update careers page**
4. **Test application submission**

### **Phase 3: Advanced Features**
1. **Quote request API**
2. **Meeting scheduler integration**
3. **Service inquiry tracking**
4. **Analytics and reporting**

## 💰 Cost Comparison

| Service | Free Tier | Paid Plans | Best For |
|---------|-----------|------------|----------|
| **Netlify Functions** | 125k requests/month | $19/month | Netlify users |
| **Cloudflare Workers** | 100k requests/day | $5/month | Security-focused |
| **Formspree** | 50 submissions/month | $10/month | Simple forms |
| **SendGrid** | 100 emails/day | $15/month | Email delivery |
| **Supabase** | 500MB database | $25/month | Full database |

## 🚀 Next Steps

1. **Choose your hosting platform** (Netlify vs Cloudflare Pages)
2. **Select email service** (SendGrid vs Mailgun)
3. **Pick database solution** (Supabase vs Airtable)
4. **Implement APIs** based on your choices
5. **Test and deploy**

**Would you like me to implement any specific API functionality for your Verakore website?** 🚀

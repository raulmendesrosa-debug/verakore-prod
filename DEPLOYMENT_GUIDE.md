# Verakore Website - Netlify Deployment Guide

## 🚀 Quick Deployment Steps

### Method 1: Drag & Drop (Fastest)
1. **Zip the public folder contents**
   - Navigate to `website/public/`
   - Select all files and folders
   - Create a ZIP file named `verakore-website.zip`

2. **Deploy to Netlify**
   - Go to [netlify.com](https://netlify.com)
   - Sign up/Login to your account
   - Drag the ZIP file to the deploy area
   - Your site will be live in minutes!

### Method 2: Git Integration (Recommended)
1. **Connect GitHub Repository**
   - Push your code to GitHub
   - Connect Netlify to your GitHub repo
   - Set build command: (leave empty)
   - Set publish directory: `website/public`
   - Deploy!

### Method 3: Netlify CLI
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Login to Netlify
netlify login

# Deploy from public directory
cd website/public
netlify deploy --prod --dir .
```

## 📧 Contact Form Setup

### Automatic Email Notifications
1. **Go to Netlify Dashboard**
   - Select your site
   - Go to "Forms" section
   - Find "contact-form" submissions

2. **Configure Email Notifications**
   - Go to Site Settings → Forms
   - Add notification email: `info@verakore.com`
   - Enable email notifications

3. **Test the Form**
   - Submit a test message
   - Check your email for notifications

## 🌐 Custom Domain Setup

### Connect verakore.com
1. **Add Custom Domain**
   - Go to Site Settings → Domain Management
   - Add `verakore.com` and `www.verakore.com`

2. **DNS Configuration**
   - Add CNAME record: `www` → `your-site-name.netlify.app`
   - Add A record: `@` → Netlify's IP (provided in dashboard)

3. **SSL Certificate**
   - Netlify automatically provides SSL
   - Force HTTPS redirect enabled

## 🔧 Configuration Files

### netlify.toml
- ✅ Build configuration
- ✅ Redirect rules
- ✅ Security headers
- ✅ Form handling

### Form Attributes
- ✅ `data-netlify="true"`
- ✅ `name="contact-form"`
- ✅ `netlify-honeypot="bot-field"`
- ✅ All fields have `name` attributes

## 📱 Features Included

### ✅ Contact Form
- **Netlify Forms integration**
- **Email to:** info@verakore.com
- **Spam protection:** Honeypot field
- **Required fields:** Name, Email, Message

### ✅ Video Meeting Options
- **Zoom, Teams, Google Meet**
- **Pre-filled email templates**
- **One-click scheduling**

### ✅ Responsive Design
- **Mobile-friendly**
- **Bootstrap framework**
- **Font Awesome icons**

### ✅ SEO Optimized
- **Meta tags**
- **Structured data**
- **Fast loading**

## 🎯 Post-Deployment Checklist

### ✅ Test These Features
- [ ] Contact form submission
- [ ] Email notifications working
- [ ] Phone number links (tel:)
- [ ] Email links (mailto:)
- [ ] Video meeting requests
- [ ] All page navigation
- [ ] Mobile responsiveness
- [ ] Logo display
- [ ] Footer links

### ✅ Verify Email Setup
- [ ] Form submissions arrive at info@verakore.com
- [ ] Video meeting requests work
- [ ] Partnership inquiries received
- [ ] Career applications processed

## 🚨 Troubleshooting

### Form Not Working?
1. Check Netlify Forms section
2. Verify `data-netlify="true"` attribute
3. Ensure all fields have `name` attributes
4. Check spam folder for notifications

### Domain Not Working?
1. Verify DNS records
2. Wait 24-48 hours for propagation
3. Check SSL certificate status
4. Test both www and non-www versions

### Images Not Loading?
1. Check file paths in HTML
2. Verify assets folder structure
3. Check browser console for errors
4. Ensure proper file permissions

## 📞 Support Contacts

- **Technical Issues:** Check Netlify documentation
- **Domain Issues:** Contact your domain registrar
- **Email Problems:** Check Netlify Forms settings

## 🎉 Success!

Once deployed, your Verakore website will be live at:
- **Temporary URL:** `https://your-site-name.netlify.app`
- **Custom Domain:** `https://verakore.com` (after DNS setup)

**Your professional IT services website is ready to attract clients!** 🚀

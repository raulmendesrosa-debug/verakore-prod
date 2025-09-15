# Contact Form Setup Guide

## Email Destination: info@verakore.com

### Option 1: Netlify Forms (Recommended)
1. Deploy website to Netlify
2. Forms work automatically
3. Configure notifications in Netlify dashboard:
   - Go to Site Settings -> Forms
   - Add notification email: info@verakore.com
   - Set up email templates

### Option 2: SMTP Configuration
1. Update email_config.json with your SMTP settings
2. Use Gmail App Password for authentication
3. Test form submission

### Form Fields Captured:
- Name (required)
- Email (required) 
- Company
- Phone
- Service Interest (dropdown)
- Message (required)

### Verification Checklist:
- [ ] Form submissions appear in Netlify dashboard
- [ ] Emails sent to info@verakore.com
- [ ] Professional email templates
- [ ] Spam protection working
- [ ] Mobile form works correctly

## Success!
All contact form submissions will be sent to info@verakore.com

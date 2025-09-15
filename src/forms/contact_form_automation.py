#!/usr/bin/env python3
"""
Verakore Contact Form Email Automation
Handles contact form submissions and sends emails to info@verakore.com
"""

import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import requests

class ContactFormHandler:
    def __init__(self):
        self.config_file = "email_config.json"
        self.recipient_email = "info@verakore.com"
        self.backup_email = "support@verakore.com"
        
    def create_email_config(self):
        """Create email configuration for form handling"""
        
        config = {
            "smtp_settings": {
                "server": "smtp.gmail.com",
                "port": 587,
                "username": "your-email@gmail.com",
                "password": "your-app-password"
            },
            "email_settings": {
                "recipient_email": "info@verakore.com",
                "backup_email": "support@verakore.com",
                "sender_name": "Verakore Contact Form",
                "subject_template": "New Contact Form Submission - {service_interest}"
            },
            "form_fields": {
                "name": "Name",
                "email": "Email",
                "company": "Company",
                "phone": "Phone",
                "service": "Service Interest",
                "message": "Message"
            },
            "netlify_forms": {
                "enabled": True,
                "form_name": "contact-form",
                "webhook_url": "https://api.netlify.com/build_hooks/your-build-hook"
            }
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
        
        print(f"✅ Created email configuration: {self.config_file}")
        
    def create_netlify_form_handler(self):
        """Create Netlify Forms integration"""
        
        # Update the HTML form to work with Netlify Forms
        form_html = '''
        <!-- Contact Form with Netlify Forms -->
        <form name="contact-form" method="POST" data-netlify="true" netlify-honeypot="bot-field">
            <input type="hidden" name="form-name" value="contact-form" />
            <p style="display: none;">
                <label>Don't fill this out if you're human: <input name="bot-field" /></label>
            </p>
            
            <div class="row g-3">
                <div class="col-md-6">
                    <label for="name" class="form-label">Name *</label>
                    <input type="text" class="form-control" id="name" name="name" required>
                </div>
                <div class="col-md-6">
                    <label for="email" class="form-label">Email *</label>
                    <input type="email" class="form-control" id="email" name="email" required>
                </div>
                <div class="col-md-6">
                    <label for="company" class="form-label">Company</label>
                    <input type="text" class="form-control" id="company" name="company">
                </div>
                <div class="col-md-6">
                    <label for="phone" class="form-label">Phone</label>
                    <input type="tel" class="form-control" id="phone" name="phone">
                </div>
                <div class="col-12">
                    <label for="service" class="form-label">Service Interest</label>
                    <select class="form-control" id="service" name="service">
                        <option value="Staff Augmentation - Networking & Infrastructure">Staff Augmentation - Networking & Infrastructure</option>
                        <option value="Fractional IT Leadership">Fractional IT Leadership</option>
                        <option value="Compliance & GxP Documentation">Compliance & GxP Documentation</option>
                        <option value="Project Delivery">Project Delivery</option>
                        <option value="Managed Services (Phase 2)">Managed Services (Phase 2)</option>
                        <option value="Cybersecurity Readiness (Phase 2)">Cybersecurity Readiness (Phase 2)</option>
                        <option value="Partnership Opportunities">Partnership Opportunities</option>
                    </select>
                </div>
                <div class="col-12">
                    <label for="message" class="form-label">Message *</label>
                    <textarea class="form-control" id="message" name="message" rows="5" required></textarea>
                </div>
                <div class="col-12">
                    <button type="submit" class="btn btn-primary-custom w-100">Send Message</button>
                </div>
            </div>
        </form>
        '''
        
        with open("contact_form_netlify.html", 'w') as f:
            f.write(form_html)
        
        print("✅ Created Netlify Forms integration")
        
    def create_email_template(self):
        """Create email template for form submissions"""
        
        template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>New Contact Form Submission</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #2563eb; color: white; padding: 20px; text-align: center; }
        .content { background: #f8fafc; padding: 20px; }
        .field { margin-bottom: 15px; }
        .label { font-weight: bold; color: #1e293b; }
        .value { margin-top: 5px; }
        .footer { background: #1e293b; color: white; padding: 15px; text-align: center; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>New Contact Form Submission</h2>
            <p>Verakore Website Contact Form</p>
        </div>
        
        <div class="content">
            <div class="field">
                <div class="label">Name:</div>
                <div class="value">{name}</div>
            </div>
            
            <div class="field">
                <div class="label">Email:</div>
                <div class="value">{email}</div>
            </div>
            
            <div class="field">
                <div class="label">Company:</div>
                <div class="value">{company}</div>
            </div>
            
            <div class="field">
                <div class="label">Phone:</div>
                <div class="value">{phone}</div>
            </div>
            
            <div class="field">
                <div class="label">Service Interest:</div>
                <div class="value">{service}</div>
            </div>
            
            <div class="field">
                <div class="label">Message:</div>
                <div class="value">{message}</div>
            </div>
            
            <div class="field">
                <div class="label">Submitted:</div>
                <div class="value">{timestamp}</div>
            </div>
        </div>
        
        <div class="footer">
            <p>This email was automatically generated from the Verakore contact form.</p>
            <p>Please respond to the customer's email address: {email}</p>
        </div>
    </div>
</body>
</html>"""
        
        with open("email_template.html", 'w') as f:
            f.write(template)
        
        print("✅ Created email template")
        
    def create_form_processing_script(self):
        """Create form processing script"""
        
        script = """#!/usr/bin/env python3
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

def send_contact_email(form_data):
    '''Send contact form email to info@verakore.com'''
    
    # Load configuration
    with open('email_config.json', 'r') as f:
        config = json.load(f)
    
    # Email settings
    recipient = config['email_settings']['recipient_email']
    sender = config['smtp_settings']['username']
    password = config['smtp_settings']['password']
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = f"New Contact Form Submission - {form_data.get('service', 'General Inquiry')}"
    
    # Create HTML content
    html_content = f"""
    <h2>New Contact Form Submission</h2>
    <p><strong>Name:</strong> {form_data.get('name', 'N/A')}</p>
    <p><strong>Email:</strong> {form_data.get('email', 'N/A')}</p>
    <p><strong>Company:</strong> {form_data.get('company', 'N/A')}</p>
    <p><strong>Phone:</strong> {form_data.get('phone', 'N/A')}</p>
    <p><strong>Service Interest:</strong> {form_data.get('service', 'N/A')}</p>
    <p><strong>Message:</strong></p>
    <p>{form_data.get('message', 'N/A')}</p>
    <hr>
    <p><em>Submitted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em></p>
    """
    
    html_part = MIMEText(html_content, 'html')
    msg.attach(html_part)
    
    # Send email
    try:
        server = smtplib.SMTP(config['smtp_settings']['server'], config['smtp_settings']['port'])
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Email sent successfully to {recipient}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

if __name__ == "__main__":
    # Test with sample data
    test_data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'company': 'Test Company',
        'phone': '555-1234',
        'service': 'Staff Augmentation',
        'message': 'This is a test message'
    }
    
    send_contact_email(test_data)
"""
        
        with open("form_processor.py", 'w') as f:
            f.write(script)
        
        print("✅ Created form processing script")
        
    def create_form_setup_guide(self):
        """Create setup guide for form automation"""
        
        guide = """# Verakore Contact Form Email Automation Setup

## 🎯 Overview
This system automatically sends contact form submissions to **info@verakore.com** using multiple methods for reliability.

## 📧 Email Configuration Options

### Option 1: Netlify Forms (Recommended - FREE)
**Best for: Easy setup, no server required**

1. **Deploy to Netlify** with the updated form
2. **Netlify automatically handles** form submissions
3. **Set up email notifications** in Netlify dashboard:
   - Go to Site Settings → Forms
   - Add notification email: `info@verakore.com`
   - Configure email templates

### Option 2: SMTP Email (Advanced)
**Best for: Custom email handling**

1. **Configure SMTP settings** in `email_config.json`:
   ```json
   {
     "smtp_settings": {
       "server": "smtp.gmail.com",
       "port": 587,
       "username": "your-email@gmail.com",
       "password": "your-app-password"
     }
   }
   ```

2. **Set up Gmail App Password**:
   - Enable 2-factor authentication
   - Generate app password
   - Use app password (not regular password)

### Option 3: Third-Party Services
**Best for: Professional email handling**

- **Formspree**: Free tier available
- **EmailJS**: Client-side email sending
- **Netlify Forms**: Built-in form handling

## 🔧 Implementation Steps

### Step 1: Update Contact Form
The form has been updated to work with Netlify Forms:
- Added `data-netlify="true"` attribute
- Added proper `name` attributes to all fields
- Added honeypot field for spam protection

### Step 2: Deploy to Netlify
1. Upload your website to Netlify
2. Forms will automatically work
3. Check Netlify dashboard for submissions

### Step 3: Configure Email Notifications
1. Go to Netlify dashboard → Site Settings → Forms
2. Add notification email: `info@verakore.com`
3. Set up email templates
4. Test form submission

## 📋 Form Fields
The contact form captures:
- **Name** (required)
- **Email** (required)
- **Company**
- **Phone**
- **Service Interest** (dropdown with Verakore services)
- **Message** (required)

## ✅ Verification
After setup, verify:
- [ ] Form submissions appear in Netlify dashboard
- [ ] Emails are sent to `info@verakore.com`
- [ ] Email templates look professional
- [ ] Spam protection is working
- [ ] Mobile form works correctly

## 🆘 Troubleshooting

### Common Issues:
1. **Emails not received**: Check spam folder, verify email address
2. **Form not submitting**: Check Netlify deployment, verify form attributes
3. **Missing fields**: Ensure all fields have proper `name` attributes

### Support:
- [Netlify Forms Documentation](https://docs.netlify.com/forms/setup/)
- [Netlify Support](https://support.netlify.com/)

## 🎉 Success!
Once configured, all contact form submissions will automatically be sent to **info@verakore.com** with professional formatting and spam protection.
"""
        
        with open("FORM_SETUP_GUIDE.md", 'w') as f:
            f.write(guide)
        
        print("✅ Created form setup guide")
        
    def setup_complete_form_system(self):
        """Setup the complete form automation system"""
        
        print("📧 Setting up contact form email automation...")
        print("=" * 50)
        
        # Create all form automation files
        self.create_email_config()
        self.create_netlify_form_handler()
        self.create_email_template()
        self.create_form_processing_script()
        self.create_form_setup_guide()
        
        print("\n✅ Contact form automation system ready!")
        print("\n📋 What's been created:")
        print("   • email_config.json - Email configuration")
        print("   • contact_form_netlify.html - Updated form")
        print("   • email_template.html - Professional email template")
        print("   • form_processor.py - Email processing script")
        print("   • FORM_SETUP_GUIDE.md - Complete setup guide")
        
        print("\n🎯 Next steps:")
        print("1. Deploy to Netlify (forms work automatically)")
        print("2. Configure email notifications in Netlify dashboard")
        print("3. Set notification email to: info@verakore.com")
        print("4. Test form submission")
        
        print("\n📧 Email Destination: info@verakore.com")
        print("✅ All form submissions will be sent to this email!")
        
        return True

def main():
    form_handler = ContactFormHandler()
    form_handler.setup_complete_form_system()

if __name__ == "__main__":
    main()

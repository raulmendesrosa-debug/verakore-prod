# 🚀 Verakore Website - Netlify Deployment Instructions

## 📋 **QUICK START GUIDE**

### **What You Need:**
- ✅ **`verakore-website-deploy.zip`** file (already created)
- ✅ **Netlify account** (free)
- ✅ **Domain registrar access** (for verakore.com)
- ✅ **Email access** to info@verakore.com

### **Total Time:** ~22 minutes
- **Deploy to Netlify:** 5 minutes
- **Configure email notifications:** 2 minutes
- **Set up custom domain:** 10 minutes
- **Test all features:** 5 minutes

---

## 🎯 **STEP 1: DEPLOY TO NETLIFY (5 minutes)**

### **1.1 Create Netlify Account**
1. **Go to [netlify.com](https://netlify.com)**
2. **Click "Sign up"** in the top right
3. **Choose sign-up method:**
   - **Email** (recommended)
   - **GitHub** (if you want Git integration)
   - **Google** (if you prefer)
4. **Complete registration** and verify your email

### **1.2 Deploy Your Website**
1. **Login to Netlify**
2. **On the dashboard, look for the deploy area** (large box with dashed border)
3. **Drag `verakore-website-deploy.zip`** from your computer to the deploy area
4. **Wait 2-3 minutes** for deployment to complete
5. **Note your site URL** (e.g., `https://amazing-name-123456.netlify.app`)

### **1.3 Verify Deployment**
1. **Click on your site name** in the dashboard
2. **Click "Open production deploy"** to view your live site
3. **Test that all pages load:**
   - Homepage
   - Services page
   - Careers page
   - Legal pages (Privacy Policy, Terms, Cookies)

---

## 📧 **STEP 2: CONFIGURE EMAIL NOTIFICATIONS (2 minutes)**

### **2.1 Access Forms Section**
1. **In your site dashboard, click "Forms"** in the left sidebar
2. **You should see "contact-form"** listed
3. **Click on "contact-form"** to view submissions

### **2.2 Set Up Email Notifications**
1. **Click "Settings and usage"** tab
2. **Scroll down to "Form notifications"**
3. **Click "Add notification"**
4. **Enter email address:** `info@verakore.com`
5. **Click "Save"**

### **2.3 Test Contact Form**
1. **Go to your live website**
2. **Scroll to the contact form**
3. **Fill out the form with test data:**
   - **Name:** Test User
   - **Email:** your-email@example.com
   - **Company:** Test Company
   - **Phone:** (555) 123-4567
   - **Service Interest:** Staff Augmentation
   - **Message:** This is a test message
4. **Click "Send Message"**
5. **Check info@verakore.com** for the notification email

---

## 🌐 **STEP 3: SET UP CUSTOM DOMAIN (10 minutes)**

### **3.1 Add Domain to Netlify**
1. **In your site dashboard, click "Domain management"**
2. **Click "Add custom domain"**
3. **Enter:** `verakore.com`
4. **Click "Verify"**
5. **Repeat for:** `www.verakore.com`

### **3.2 Get DNS Records from Netlify**
1. **In Domain management, you'll see DNS records needed**
2. **Note these records:**
   ```
   Type: CNAME
   Name: www
   Value: your-site-name.netlify.app
   
   Type: A
   Name: @
   Value: 75.2.60.5
   ```

### **3.3 Update DNS at Your Domain Registrar**
1. **Login to your domain registrar** (GoDaddy, Namecheap, etc.)
2. **Go to DNS management** for verakore.com
3. **Add/Update these records:**
   - **CNAME Record:** `www` → `your-site-name.netlify.app`
   - **A Record:** `@` → `75.2.60.5`
4. **Save changes**

### **3.4 Wait for DNS Propagation**
1. **DNS changes take 24-48 hours** to propagate worldwide
2. **You can check status** at [whatsmydns.net](https://whatsmydns.net)
3. **Netlify will automatically issue SSL certificate** once DNS is active

---

## ✅ **STEP 4: TEST ALL FEATURES (5 minutes)**

### **4.1 Test Contact Form**
- [ ] **Form submits successfully**
- [ ] **Email notification arrives at info@verakore.com**
- [ ] **All fields are captured correctly**
- [ ] **Spam protection works** (honeypot field)

### **4.2 Test Phone & Email Links**
- [ ] **Phone numbers click to open dialer** (tel: protocol)
- [ ] **Email addresses click to open email client** (mailto: protocol)
- [ ] **Video meeting requests open email** with pre-filled template

### **4.3 Test All Pages**
- [ ] **Homepage loads correctly**
- [ ] **Services page loads correctly**
- [ ] **Careers page loads correctly**
- [ ] **Privacy Policy page loads**
- [ ] **Terms of Service page loads**
- [ ] **Cookie Policy page loads**

### **4.4 Test Mobile Responsiveness**
- [ ] **Website works on mobile devices**
- [ ] **Logo displays properly on all pages**
- [ ] **Navigation menu works on mobile**
- [ ] **Contact form works on mobile**

### **4.5 Test Security Features**
- [ ] **HTTPS is enabled** (green lock icon in browser)
- [ ] **Security headers are applied**
- [ ] **SSL certificate is valid**

---

## 🚨 **TROUBLESHOOTING**

### **Contact Form Not Working?**
1. **Check Netlify Forms section** in dashboard
2. **Verify `data-netlify="true"`** is in the form tag
3. **Ensure all fields have `name` attributes**
4. **Check spam folder** for notifications
5. **Try different email address** for testing

### **Domain Not Working?**
1. **Verify DNS records** are correct at registrar
2. **Wait 24-48 hours** for DNS propagation
3. **Check SSL certificate status** in Netlify dashboard
4. **Test both www and non-www** versions
5. **Clear browser cache** and try again

### **Images Not Loading?**
1. **Check file paths** in HTML
2. **Verify assets folder structure**
3. **Check browser console** for errors
4. **Ensure proper file permissions**

### **Site Not Loading?**
1. **Check Netlify dashboard** for build errors
2. **Verify all files uploaded** correctly
3. **Check browser console** for errors
4. **Try different browser** or incognito mode

---

## 📞 **SUPPORT RESOURCES**

### **Netlify Support:**
- **Documentation:** [docs.netlify.com](https://docs.netlify.com)
- **Community:** [community.netlify.com](https://community.netlify.com)
- **Support:** [support.netlify.com](https://support.netlify.com)

### **Domain Registrar Support:**
- **GoDaddy:** [help.godaddy.com](https://help.godaddy.com)
- **Namecheap:** [support.namecheap.com](https://support.namecheap.com)
- **Google Domains:** [support.google.com/domains](https://support.google.com/domains)

---

## 🎉 **SUCCESS CHECKLIST**

### **Your Verakore Website Will Have:**
- ✅ **Professional appearance** with consistent branding
- ✅ **Working contact form** sending emails to info@verakore.com
- ✅ **Clickable phone numbers** for direct calling
- ✅ **Video meeting options** for client consultations
- ✅ **Mobile-responsive** design for all devices
- ✅ **Fast loading** with global CDN
- ✅ **Secure hosting** with enterprise compliance
- ✅ **Custom domain** at verakore.com
- ✅ **SSL certificate** for secure connections

### **Features Ready:**
- ✅ **Contact Form** → Emails to info@verakore.com
- ✅ **Phone Links** → (617) 865-9705
- ✅ **Email Links** → info@verakore.com
- ✅ **Video Meetings** → Zoom, Teams, Google Meet
- ✅ **Career Applications** → Database ready
- ✅ **Legal Pages** → Privacy, Terms, Cookies

---

## 🚀 **YOU'RE READY TO GO LIVE!**

**Your Verakore website is professionally designed and ready for deployment!**

**Follow these instructions step-by-step and you'll have a live, professional IT services website in under 30 minutes!**

**Good luck with your deployment!** 🎉

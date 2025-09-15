This website is automatically deployed to **Cloudflare Pages** when changes are pushed to the main branch.

### Current Deployment Process
1. **Make changes** in `netlify_fresh/` folder
2. **Commit changes**: `git commit -m "Description of changes"`
3. **Push to GitHub**: `git push origin main`
4. **Cloudflare automatically deploys** the website
5. **Website updates live** in 2-3 minutes

### Finding Your Live Website
1. Go to [Cloudflare Dashboard](https://dash.cloudflare.com)
2. Log in to your Cloudflare account
3. Click **"Pages"** in the left sidebar
4. Find your **"verakore-website"** project
5. Click on it to see the live URL

### Manual Deployment (Alternative)
If you need to deploy manually:
1. Go to [Cloudflare Pages](https://pages.cloudflare.com)
2. Connect your GitHub repository
3. Configure build settings
4. Deploy

3. Website updates live in 2-3 minutes

## 📁 File Structure

```
verakore-website/
├── netlify_fresh/ # Main website files (deployed)
│ ├── index.html # Homepage
│ ├── services.html # Services page
│ ├── careers.html # Careers page
│ ├── privacy-policy.html # Privacy policy
│ ├── terms-of-service.html# Terms of service
│ ├── cookie-policy.html # Cookie policy
│ ├── headers # Security headers
│ ├── assets/
│ │ ├── css/
│ │ │ └── styles.css # Main stylesheet
│ │ ├── images/
│ │ │ ├── logos/ # Company logos
│ │ │ ├── hero/ # Hero images
│ │ │ ├── services/ # Service images
│ │ │ ├── team/ # Team photos
│ │ │ └── portfolio/ # Portfolio images
│ │ └── js/
│ │ └── scripts.js # JavaScript files
│ └── README.md # This file
├── website/ # Development files
├── docs/ # Documentation
└── tools/ # Deployment tools
```


## �� Development

### Local Development
1. Clone the repository
2. Navigate to `netlify_fresh/` folder
3. Open `index.html` in a web browser
4. Make changes to HTML, CSS, or JavaScript
5. Test locally before pushing

### Making Changes
1. Edit files in `netlify_fresh/` folder
2. Test changes in browser
3. Commit changes: `git commit -m "Description of changes"`
4. Push to GitHub: `git push origin main`
5. Cloudflare automatically deploys

## �� Performance

- **Fast Loading** - Optimized images and code
- **Global CDN** - Cloudflare's worldwide network
- **Mobile Responsive** - Works on all devices
- **SEO Optimized** - Search engine friendly
- **SSL/HTTPS** - Secure connections included

## 🔒 Security

- **HTTPS** - Secure connections
- **Security Headers** - Protection against common attacks
- **Form Validation** - Spam protection via Formspree
- **Regular Updates** - Keep dependencies updated

## 📞 Support

For technical support or questions about this website, contact:
- **Email:** info@verakore.com
- **Phone:** (617) 865-9705

## 📄 License

© 2025 Verakore IT Services. All rights reserved.

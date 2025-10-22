# Development Environment Setup - GitHub Pages

## ✅ Setup Complete

### Branches Created
- ✅ `main` branch - Production (deploys to Cloudflare)
- ✅ `dev` branch - Development (will deploy to GitHub Pages for testing)

---

## 🚀 Enable GitHub Pages (2 Steps)

### Step 1: Go to Repository Settings
1. Open: **https://github.com/raulmendesrosa-debug/verakore-prod**
2. Click the **Settings** tab (top right)
3. In the left sidebar, click **Pages**

### Step 2: Configure GitHub Pages
1. Under **"Build and deployment"** section:
   - **Source**: Select **"Deploy from a branch"**
   - **Branch**: Select **`dev`** (NOT main!)
   - **Folder**: Select **`/ (root)`**
2. Click **Save**
3. Wait 1-2 minutes for deployment

### Your Dev Website URL:
**https://raulmendesrosa-debug.github.io/verakore-prod/**

---

## 📱 How to Use for Mobile Testing

### Development Workflow:
1. **Work locally on `dev` branch**
   ```bash
   git checkout dev
   # Make your changes to HTML/CSS/JS
   ```

2. **Test locally first**
   - Open files in browser
   - Check everything works

3. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin dev
   ```

4. **Test on mobile devices**
   - Wait 1-2 minutes for GitHub Pages to update
   - Visit: `https://raulmendesrosa-debug.github.io/verakore-prod/`
   - Test on iPhone, Android, tablets, etc.

5. **When satisfied, merge to production**
   ```bash
   git checkout main
   git merge dev
   git push origin main
   # This deploys to Cloudflare production
   ```

---

## 🎯 Quick Mobile Testing Tips

### Easy Mobile Access:
1. Generate QR code: https://www.qr-code-generator.com/
2. Enter your dev URL: `https://raulmendesrosa-debug.github.io/verakore-prod/`
3. Scan with phone camera
4. Bookmark on your phone for quick access

### Test These Pages:
- `index.html` - Homepage
- `services.html` - Services
- `partnerships.html` - Partnerships
- `careers.html` - Careers

### Mobile Testing Checklist:
- [ ] Mobile menu opens/closes smoothly
- [ ] Links work correctly
- [ ] Scroll lock works (page doesn't scroll when menu open)
- [ ] Close-on-click works (menu closes when link tapped)
- [ ] Hamburger icon visible on all devices
- [ ] All pages responsive on different screen sizes

---

## 🔄 Branch Strategy

### `dev` Branch (GitHub Pages)
- **Purpose**: Development and testing
- **URL**: https://raulmendesrosa-debug.github.io/verakore-prod/
- **Use for**: Testing mobile changes, new features, experiments
- **Deploys**: Automatically on push to GitHub

### `main` Branch (Cloudflare)
- **Purpose**: Production website
- **URL**: https://verakore.com (or your Cloudflare URL)
- **Use for**: Live production site
- **Deploys**: Automatically via Cloudflare Pages

---

## 📝 Next Steps

1. **Enable GitHub Pages** (follow Step 1 & 2 above)
2. **Wait 2 minutes** for first deployment
3. **Visit dev URL** on your mobile device
4. **Test the mobile menu** improvements
5. **If satisfied**, merge to main for production

---

## 🆘 Troubleshooting

### GitHub Pages not working?
- Make sure you selected `dev` branch (not main)
- Check that files are in root folder (not subfolder)
- Wait 2-3 minutes after enabling
- Check Settings → Pages for deployment status

### Changes not appearing?
- Clear browser cache (hard refresh: Ctrl+Shift+R)
- On mobile: Clear Safari/Chrome cache
- Check GitHub Actions tab to see if deployment completed

### Different from production?
- That's expected! Dev branch is for testing
- Only merge to `main` when you're happy with changes

---

**Current Status:**
- ✅ Branches created
- ✅ Pushed to GitHub
- ⏳ Waiting for you to enable GitHub Pages
- ⏳ Then test on mobile!


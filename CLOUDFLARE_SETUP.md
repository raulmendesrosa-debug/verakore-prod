# Cloudflare Setup Instructions
# Follow these steps to complete your Cloudflare integration

## 1. Get Cloudflare API Token
- Go to: https://dash.cloudflare.com/profile/api-tokens
- Click "Create Token"
- Use "Custom token" template
- Permissions: Cloudflare Pages:Edit
- Account Resources: Include your account
- Zone Resources: Include all zones
- Create Token and copy it

## 2. Get Account ID
- Go to Cloudflare Dashboard
- Select any domain
- Copy Account ID from right sidebar

## 3. Update deployment_config.json
Replace these values in deployment_config.json:
- "account_id": "YOUR_ACCOUNT_ID_HERE"
- "api_token": "YOUR_API_TOKEN_HERE"

## 4. Add GitHub Secrets
- Go to your GitHub repository
- Settings → Secrets and variables → Actions
- Add these secrets:
  - CLOUDFLARE_API_TOKEN: Your API token
  - CLOUDFLARE_ACCOUNT_ID: Your account ID

## 5. Test Deployment
Run: python deploy.py deploy

## 6. Your Website Will Be Available At:
https://verakore-website.pages.dev

## Next Steps:
1. Complete Cloudflare setup
2. Test deployment
3. Push to GitHub for automatic deployment
4. Monitor deployment logs

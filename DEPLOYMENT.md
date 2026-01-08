# Deployment Guide for Vercel

## Quick Deploy to Vercel

### Step 1: Prepare for Deployment

1. **Ensure all dependencies are in `requirements.txt`**
   ```bash
   # Already done - xrpl-py is listed
   ```

2. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Vercel deployment files"
   git push
   ```

### Step 2: Deploy to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Sign up/Login with GitHub
3. Click "New Project"
4. Import your GitHub repository
5. Vercel will auto-detect settings:
   - Framework Preset: Other
   - Root Directory: ./
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
6. Click "Deploy"

### Step 3: Configure Environment (if needed)

Vercel will automatically:
- Install dependencies from `requirements.txt`
- Deploy serverless functions from `api/`
- Serve static files from `ui/`

### Step 4: Get Your URLs

After deployment, you'll get:
- **Base URL**: `https://your-app.vercel.app`
- **API Endpoint**: `https://your-app.vercel.app/api/check-trustline`
- **Issuer Info**: `https://your-app.vercel.app/api/issuer-info/{issuer_key}`
- **Opt-in Page**: `https://your-app.vercel.app/ui/opt-in.html?issuer=community_aid`

## Testing Locally (Before Deploy)

### Install Vercel CLI
```bash
npm i -g vercel
```

### Run Locally
```bash
vercel dev
```

This will:
- Start local server at `http://localhost:3000`
- Test serverless functions
- Test UI page

## Dify Integration

### 1. Add API Tool in Dify

**Tool Configuration:**
- Name: `check_trustline_status`
- API URL: `https://your-app.vercel.app/api/check-trustline`
- Method: `POST`
- Headers: `Content-Type: application/json`
- Body: 
  ```json
  {
    "wallet_address": "{{user_wallet_address}}"
  }
  ```

### 2. Update Dify Instructions

Add to your Dify agent instructions:
```
When user provides wallet address, call check_trustline_status tool.

If opted_in is false, provide opt-in link:
"To opt in to [Issuer Name], visit: https://your-app.vercel.app/ui/opt-in.html?issuer=community_aid&return_to=https://your-dify-url.com/chat"

If opted_in is true, acknowledge and present resources from allowed_resources.
```

### 3. Test Flow

1. User chats with Dify
2. Dify asks for wallet address
3. Dify calls API → checks trustline
4. If no trustline → Dify provides opt-in link
5. User clicks link → UI page → Crossmark → creates trustline
6. User returns to Dify
7. Dify checks again → unlocks resources

## Troubleshooting

### Serverless Function Errors

If functions fail:
1. Check Vercel logs: Dashboard → Your Project → Functions
2. Ensure `xrpl-py` is in `requirements.txt`
3. Check that imports work (sys.path adjustments)

### CORS Issues

CORS is handled in the serverless functions. If issues persist:
- Check `vercel.json` headers configuration
- Ensure Dify can call your API

### Crossmark Not Working

- Ensure user has Crossmark extension installed
- Test on testnet (functions use testnet by default)
- Check browser console for errors

## Production Considerations

For production:
1. Switch to mainnet in `api/check-trustline.py`:
   ```python
   xrpl_client = XRPLClient(testnet=False)
   ```
2. Update UI to use mainnet explorer
3. Add error handling and logging
4. Consider rate limiting for API


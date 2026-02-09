# Vercel Deployment Guide

## Issue
Getting 404: NOT_FOUND error after deploying to Vercel.

## Root Cause
The Next.js app is in a subdirectory (`phase-2-web/frontend/`), but Vercel is trying to deploy from the root directory.

## Solution

### Option 1: Configure Root Directory in Vercel Dashboard (RECOMMENDED)

1. Go to your Vercel project dashboard
2. Click on **Settings**
3. Scroll to **Build & Development Settings**
4. Set **Root Directory** to: `phase-2-web/frontend`
5. Click **Save**
6. Go to **Deployments** tab
7. Click **Redeploy** on the latest deployment

### Option 2: Use vercel.json (Already Added)

The `vercel.json` file has been added to the repository root. This should automatically configure Vercel to deploy from the subdirectory.

If Option 1 doesn't work, this file will serve as a fallback.

## Environment Variables

Add these environment variables in Vercel dashboard:

### Required Variables

1. **NEXT_PUBLIC_API_URL**
   - Value: Your backend API URL
   - Example: `https://your-backend.railway.app/api/v1`
   - Or: `http://localhost:8080/api/v1` (for development)

2. **NEXTAUTH_URL**
   - Value: Your Vercel deployment URL
   - Example: `https://your-app.vercel.app`

3. **NEXTAUTH_SECRET**
   - Value: A random secret string (32+ characters)
   - Generate with: `openssl rand -base64 32`

### Optional OAuth Variables (if using OAuth)

4. **GOOGLE_CLIENT_ID**
   - Get from: https://console.cloud.google.com/

5. **GOOGLE_CLIENT_SECRET**
   - Get from: https://console.cloud.google.com/

6. **FACEBOOK_CLIENT_ID**
   - Get from: https://developers.facebook.com/

7. **FACEBOOK_CLIENT_SECRET**
   - Get from: https://developers.facebook.com/

## Steps to Fix

1. ✅ Push vercel.json to GitHub (DONE)
2. ⏳ Configure Root Directory in Vercel
3. ⏳ Add Environment Variables
4. ⏳ Redeploy

## Verification

After redeployment, you should see:
- ✅ Homepage loads correctly
- ✅ Login page accessible at `/login`
- ✅ Register page accessible at `/register`
- ✅ No 404 errors

## Backend Deployment

Note: The frontend needs a backend API. Deploy the backend separately:

### Backend Options:
1. **Railway** (Recommended)
   - Deploy `phase-2-web/backend/`
   - Add DATABASE_URL, OPENAI_API_KEY, etc.

2. **Render**
   - Deploy as Python web service
   - Root directory: `phase-2-web/backend`

3. **Heroku**
   - Deploy with Procfile
   - Add buildpack: `heroku/python`

## Common Issues

### Issue: Still getting 404
**Solution**: Make sure Root Directory is set to `phase-2-web/frontend` (not `phase-2-web/frontend/`)

### Issue: Build fails
**Solution**: Check that all dependencies are in package.json

### Issue: Environment variables not working
**Solution**: Make sure variables start with `NEXT_PUBLIC_` for client-side access

## Need Help?

If you're still getting errors:
1. Check Vercel deployment logs
2. Check browser console for errors
3. Verify environment variables are set correctly

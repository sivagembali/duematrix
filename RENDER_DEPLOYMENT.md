# Render Deployment Guide for DueMatrix

## Prerequisites
- GitHub account with your code pushed
- Render account (free tier works)
- PostgreSQL database (Render provides free tier)

## Step 1: Push Code to GitHub

```powershell
cd C:\Users\ssiva\Dev\duematrix
git add .
git commit -m "Configure for Render deployment"
git push origin duematrix
```

## Step 2: Create PostgreSQL Database on Render

1. Go to https://dashboard.render.com/
2. Click **New +** → **PostgreSQL**
3. Fill in:
   - **Name**: `duematrix-db`
   - **Database**: `duematrix`
   - **User**: `duematrix_user`
   - **Region**: Choose closest to your users
   - **Plan**: Free
4. Click **Create Database**
5. Copy the **Internal Database URL** (starts with `postgres://`)

## Step 3: Deploy Backend API

1. Click **New +** → **Web Service**
2. Connect your GitHub repository
3. Fill in:
   - **Name**: `duematrix-api`
   - **Region**: Same as database
   - **Branch**: `duematrix`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --workers 3 --timeout 120 --bind 0.0.0.0:$PORT`
   - **Plan**: Free

4. **Environment Variables** - Add these:
   ```
   DATABASE_URL = [paste Internal Database URL from Step 2]
   JWT_SECRET_KEY = [generate random string, e.g., use: openssl rand -hex 32]
   FLASK_ENV = production
   CORS_ORIGINS = https://duematrix-frontend.onrender.com
   PYTHON_VERSION = 3.11.0
   ```

5. Click **Create Web Service**

6. **After deployment**, copy the service URL (e.g., `https://duematrix-api.onrender.com`)

## Step 4: Update Frontend Environment for Production

Update `duematrix-app/src/environments/environment.prod.ts`:

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://duematrix-api.onrender.com/api'  // Use your actual backend URL
};
```

Rebuild frontend:
```powershell
cd duematrix-app
ng build --configuration production
```

## Step 5: Deploy Frontend Static Site

1. Click **New +** → **Static Site**
2. Connect same GitHub repository
3. Fill in:
   - **Name**: `duematrix-frontend`
   - **Branch**: `duematrix`
   - **Root Directory**: `duematrix-app`
   - **Build Command**: `npm install && npm run build -- --configuration production`
   - **Publish Directory**: `dist/duematrix-app/browser`
   - **Plan**: Free

4. Add **Rewrite Rule** for Angular routing:
   - Click **Redirects/Rewrites** tab
   - Add rule:
     - **Source**: `/*`
     - **Destination**: `/index.html`
     - **Action**: Rewrite

5. Click **Create Static Site**

## Step 6: Initialize Database

After backend is deployed, run migrations:

1. In Render dashboard, go to your `duematrix-api` service
2. Click **Shell** tab
3. Run:
   ```bash
   cd backend
   flask db upgrade
   python seed_roles_users.py
   python seed_comprehensive_headers.py
   python seed_cycles.py
   python seed_customer_data.py
   ```

## Step 7: Update Backend CORS

After frontend is deployed, update the backend `CORS_ORIGINS` environment variable:

1. Go to `duematrix-api` service settings
2. Update **Environment Variables**:
   ```
   CORS_ORIGINS = https://duematrix-frontend.onrender.com
   ```
3. Service will auto-redeploy

## Step 8: Test Your Application

1. Visit your frontend URL: `https://duematrix-frontend.onrender.com`
2. Test login with seeded admin user
3. Verify all features work

## Important Notes

### Free Tier Limitations
- Backend spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- Database limited to 90 days retention

### Performance Optimization
- Consider upgrading to paid tier for production use
- Backend: $7/month keeps service always running
- Database: $7/month for persistent storage

### Troubleshooting

**Backend won't start:**
- Check logs in Render dashboard
- Verify `DATABASE_URL` is set correctly
- Ensure all dependencies in `requirements.txt`

**Frontend 404 errors:**
- Verify rewrite rule is configured
- Check build output path matches publish directory

**API calls fail:**
- Check `CORS_ORIGINS` includes frontend URL
- Verify backend URL in `environment.prod.ts`
- Check browser console for CORS errors

**Database connection errors:**
- Use Internal Database URL (not External)
- Verify database is in same region as backend

### Monitoring

- **Logs**: Available in Render dashboard under "Logs" tab
- **Metrics**: View CPU, memory, bandwidth usage
- **Alerts**: Configure email alerts for service downtime

## Alternative: One-Click Deploy

If you prefer using the `render.yaml` file in the repo:

1. Push code to GitHub with `render.yaml`
2. Go to Render Dashboard
3. Click **New +** → **Blueprint**
4. Connect repository and select `duematrix` branch
5. Render will automatically create all services from `render.yaml`
6. Follow Step 6 to initialize database

## Environment Variables Reference

### Backend (duematrix-api)
| Variable | Value | Description |
|----------|-------|-------------|
| DATABASE_URL | [from Render DB] | PostgreSQL connection string |
| JWT_SECRET_KEY | [random string] | Secret for JWT tokens |
| FLASK_ENV | production | Environment mode |
| CORS_ORIGINS | [frontend URL] | Allowed CORS origins |
| PYTHON_VERSION | 3.11.0 | Python version |

### Database (duematrix-db)
All configuration automatic, just copy Internal Database URL.

## Cost Estimate

**Free Tier:**
- Backend: Free (with spin-down)
- Frontend: Free (100 GB bandwidth/month)
- Database: Free (90 days)
- **Total: $0/month**

**Production Tier:**
- Backend: $7/month (always on, 512MB RAM)
- Frontend: Free
- Database: $7/month (persistent, 1GB RAM)
- **Total: $14/month**

## Support

For issues:
1. Check Render documentation: https://render.com/docs
2. View service logs in dashboard
3. Test locally first with same environment variables
4. Contact Render support or check their community forum

# Quick Render.com Setup Checklist

## Your Current Error
The app is trying to connect to `localhost` PostgreSQL, but Render doesn't have access to your local database. You need to configure it to use Render's PostgreSQL.

## Fix: Deploy with Render Database

### Step 1: Go to Render Dashboard
Visit: https://dashboard.render.com

### Step 2: Use Blueprint (Easiest Method)

1. Click **"New +"** → **"Blueprint"**
2. Connect GitHub: Select `oyeks-ayo/SeenITApp`
3. Render will detect `render.yaml` and show:
   - ✅ PostgreSQL database: `seenit-db`
   - ✅ Web service: `seenit-app`
4. Click **"Apply"**

### Step 3: Wait for Setup (5-10 minutes)
- Database provisioning: ~5 min
- First deployment: ~5 min
- Watch the deploy logs

### Step 4: Run Database Migrations

Once deployed:

1. Go to **seenit-app** → **Shell** tab
2. Run these commands:
   ```bash
   flask --app starter.py db upgrade
   ```

3. Verify:
   ```bash
   flask --app starter.py db current
   ```

### Step 5: Access Your App

Your app will be live at:
```
https://seenit-app.onrender.com
```

## Important Notes

### Free Tier Behavior
- App sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds (cold start)
- This is normal for free tier

### Environment Variables (Auto-Configured)
The `render.yaml` automatically sets:
- ✅ `SECRET_KEY` - Auto-generated
- ✅ `SQLALCHEMY_DATABASE_URI` - Connected to database
- ✅ `PYTHON_VERSION` - Set to 3.13.0

### Database Details
- **Name:** seenit-db
- **Type:** PostgreSQL
- **Size:** 1 GB (free tier)
- **Region:** Oregon
- **Note:** Data deleted after 90 days of inactivity on free tier

## If You Already Have a Web Service on Render

If you already created a web service manually:

1. Go to that service → **Environment**
2. Add this environment variable:
   ```
   SQLALCHEMY_DATABASE_URI = [Internal Database URL from seenit-db]
   ```
3. To get the Internal Database URL:
   - Go to `seenit-db` dashboard
   - Copy the **Internal Database URL**
   - Paste it into the environment variable

## Testing After Deployment

### 1. Check Homepage
Visit: `https://seenit-app.onrender.com`

### 2. Test User Registration
Go to: `https://seenit-app.onrender.com/signup`

### 3. Check Logs
Dashboard → seenit-app → Logs

Look for:
- ✅ `Listening at: http://0.0.0.0:xxxxx` (app started)
- ❌ Any database connection errors

## Troubleshooting

### Still Getting Localhost Error?

1. **Check Environment Variable:**
   - Go to seenit-app → Environment
   - Verify `SQLALCHEMY_DATABASE_URI` is set
   - Should start with `postgresql://` not `localhost`

2. **Redeploy:**
   - Dashboard → seenit-app → Manual Deploy
   - Click "Clear build cache & deploy"

3. **Check Database Status:**
   - Go to seenit-db dashboard
   - Status should be "Available"

### Database Not Created?

Run migrations in the Shell:
```bash
flask --app starter.py db upgrade
```

### App Won't Start?

Check logs for:
- Missing dependencies
- Import errors
- Configuration issues

## Next Steps After Successful Deployment

1. **Test all features:**
   - User registration
   - Login/logout
   - Profile creation
   - Project uploads

2. **Set up monitoring:**
   - Check metrics regularly
   - Monitor error logs

3. **Optional: Add custom domain**
   - Settings → Custom Domains
   - Configure your own domain

4. **Consider upgrades when needed:**
   - More traffic → Upgrade web service
   - More data → Upgrade database
   - No sleep → Paid plan ($7/month)

## Quick Commands Reference

**Access Shell:**
Dashboard → seenit-app → Shell

**Run Migrations:**
```bash
flask --app starter.py db upgrade
```

**Check Migration Status:**
```bash
flask --app starter.py db current
```

**Connect to Database:**
```bash
psql $DATABASE_URL
```

**View Tables:**
```sql
\dt
```

**Check Users:**
```sql
SELECT * FROM users;
```

## Support Links

- Render Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com
- Your Repo: https://github.com/oyeks-ayo/SeenITApp

---

**Total Setup Time:** ~15 minutes
**Cost:** $0 (Free tier)
**Next Deployment:** Automatic on git push to main

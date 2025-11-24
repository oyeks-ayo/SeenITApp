# SeenIT App - Render.com Deployment Guide

## Prerequisites
- GitHub account with SeenITApp repository
- Render.com account (sign up at https://render.com)

## Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "feat: Add Render deployment configuration"
   git push origin main
   ```

2. **Connect to Render**
   - Go to https://dashboard.render.com
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository: `oyeks-ayo/SeenITApp`
   - Render will automatically detect `render.yaml` and create:
     - PostgreSQL database (seenit-db)
     - Web service (seenit-app)

3. **Wait for Deployment**
   - Database creation: ~5 minutes
   - First deployment: ~10 minutes
   - Subsequent deployments: ~3-5 minutes

4. **Run Database Migrations**
   - In Render Dashboard → seenit-app → Shell
   - Run:
     ```bash
     flask --app starter.py db upgrade
     ```

### Option 2: Manual Setup

#### Step 1: Create PostgreSQL Database

1. Go to https://dashboard.render.com
2. Click "New +" → "PostgreSQL"
3. Configure:
   - **Name:** seenit-db
   - **Database:** seenITApp
   - **User:** seenit_user (auto-generated)
   - **Region:** Oregon (or closest to your users)
   - **Plan:** Free
4. Click "Create Database"
5. **Save the Internal Database URL** (will look like):
   ```
   postgresql://seenit_user:password@dpg-xxxxx.oregon-postgres.render.com/seenITApp
   ```

#### Step 2: Create Web Service

1. Click "New +" → "Web Service"
2. Connect GitHub repository: `oyeks-ayo/SeenITApp`
3. Configure:
   - **Name:** seenit-app
   - **Region:** Oregon (same as database)
   - **Branch:** main
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn starter:app`
   - **Plan:** Free

#### Step 3: Set Environment Variables

In the Web Service settings → Environment:

1. **SECRET_KEY**
   - Click "Generate Value" or use your own secure key
   - Example: `python -c "import secrets; print(secrets.token_hex(32))"`

2. **SQLALCHEMY_DATABASE_URI**
   - Paste the Internal Database URL from Step 1
   - Format: `postgresql://user:password@host/database`

3. **PYTHON_VERSION** (optional)
   - Value: `3.13.0`

#### Step 4: Deploy

1. Click "Create Web Service"
2. Wait for initial deployment (~10 minutes)
3. Once deployed, open the Shell tab
4. Run migrations:
   ```bash
   flask --app starter.py db upgrade
   ```

## Post-Deployment

### Verify Deployment

1. **Check Service Status**
   - Go to your web service dashboard
   - Status should show "Live"

2. **Access Your App**
   - URL will be: `https://seenit-app.onrender.com`
   - Or your custom domain if configured

3. **Test Database Connection**
   - Visit the homepage
   - Try registering a user
   - Check for any errors in Logs tab

### Database Management

**Connect to Database:**
```bash
# From Render Shell
psql $DATABASE_URL
```

**Run Migrations:**
```bash
flask --app starter.py db upgrade
```

**Create Migration:**
```bash
flask --app starter.py db migrate -m "description"
```

**Check Current Version:**
```bash
flask --app starter.py db current
```

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | Auto-generated on Render |
| `SQLALCHEMY_DATABASE_URI` | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `PYTHON_VERSION` | Python runtime version | `3.13.0` |

## Troubleshooting

### Issue: Database Connection Failed

**Error:**
```
psycopg2.OperationalError: connection to server at "localhost" failed
```

**Solution:**
- Verify `SQLALCHEMY_DATABASE_URI` is set correctly
- Use the **Internal Database URL** from Render dashboard
- Ensure database and web service are in the same region

### Issue: Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'gunicorn'
```

**Solution:**
- Ensure `gunicorn` is in `requirements.txt`
- Check build logs for installation errors
- Trigger a manual deploy

### Issue: Port Already in Use

**Error:**
```
Address already in use
```

**Solution:**
- Don't specify port in `app.run()` for production
- Render automatically assigns the port via `$PORT`
- Gunicorn handles this automatically

### Issue: Static Files Not Loading

**Solution:**
- Verify static files are in `pkg/static/`
- Check Flask static folder configuration
- For production, consider using a CDN

### Issue: Database Migration Failed

**Solution:**
```bash
# Check current migration state
flask --app starter.py db current

# View migration history
flask --app starter.py db history

# Force to specific version
flask --app starter.py db stamp head

# Retry upgrade
flask --app starter.py db upgrade
```

## Free Tier Limitations

### Web Service (Free Plan)
- 750 hours/month (enough for 24/7 operation)
- Automatic spin down after 15 minutes of inactivity
- Spins up on request (~30 seconds cold start)
- 512 MB RAM
- 0.1 CPU

### PostgreSQL (Free Plan)
- 1 GB storage
- 90-day data retention
- Expires after 90 days of inactivity
- **Important:** Set up backups before expiration

## Monitoring

### View Logs
- Dashboard → seenit-app → Logs
- Shows real-time application logs
- Check for errors and warnings

### Performance Metrics
- Dashboard → seenit-app → Metrics
- Monitor CPU, memory, and response times

### Set Up Alerts
- Dashboard → Settings → Notifications
- Configure deploy success/failure alerts
- Set up health check alerts

## Custom Domain (Optional)

1. Go to Settings → Custom Domains
2. Add your domain (e.g., `www.seenit.com`)
3. Add DNS records at your domain provider:
   ```
   CNAME www seenit-app.onrender.com
   ```
4. SSL certificate is automatically provisioned

## Automatic Deployments

With render.yaml, deployments are automatic:
- Push to `main` branch triggers deployment
- Each push creates a new deploy
- Previous deploys are kept for rollback

**Disable Auto-Deploy:**
- Dashboard → Settings → Auto-Deploy
- Turn off for manual control

## Backup Strategy

### Database Backups

**Manual Backup:**
```bash
# From local machine
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

**Automated Backups:**
- Render Pro plan includes automatic backups
- Free tier: Set up scheduled backups via GitHub Actions

### Code Backups
- Always on GitHub
- Use tags for releases:
  ```bash
  git tag -a v1.0.0 -m "Production release"
  git push origin v1.0.0
  ```

## Scaling (Paid Plans)

When you outgrow the free tier:

### Upgrade Database
- Render Standard: $7/month, 10 GB, faster
- Render Pro: $20/month, 50 GB, daily backups

### Upgrade Web Service
- Starter: $7/month, 512 MB RAM, no spin down
- Standard: $25/month, 2 GB RAM, better performance

## Security Checklist

- [ ] Never commit `.env` file
- [ ] Use strong `SECRET_KEY`
- [ ] Keep dependencies updated
- [ ] Enable CSRF protection (already configured)
- [ ] Use HTTPS (automatic on Render)
- [ ] Validate user inputs
- [ ] Sanitize file uploads
- [ ] Set up database connection pooling
- [ ] Configure CORS if needed
- [ ] Monitor logs for suspicious activity

## Additional Resources

- Render Documentation: https://render.com/docs
- Flask Deployment: https://flask.palletsprojects.com/en/latest/deploying/
- PostgreSQL on Render: https://render.com/docs/databases
- Troubleshooting: https://render.com/docs/troubleshooting

## Support

- Render Community: https://community.render.com
- Render Status: https://status.render.com
- GitHub Issues: https://github.com/oyeks-ayo/SeenITApp/issues

# Deployment and Testing Guide

## Pre-Deployment Checklist

Before deploying the application, ensure you have:

- [ ] PostgreSQL database (Neon DB, AWS RDS, or similar)
- [ ] Anthropic API key or OpenAI API key
- [ ] Domain name (optional, for production)
- [ ] SSL certificate (for HTTPS)
- [ ] OAuth credentials (Google, Facebook) if using OAuth
- [ ] Hosting accounts (Backend: Railway/Render/AWS, Frontend: Vercel/Netlify)

---

## Environment Configuration

### Backend Environment Variables

Create a `.env` file with production values:

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname

# AI Services (at least one required)
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-...

# MCP Server
MCP_SERVER_URL=http://localhost:8001

# JWT Authentication
SECRET_KEY=<generate-strong-random-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS (add your frontend domain)
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# OAuth Providers (optional)
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
FACEBOOK_CLIENT_ID=...
FACEBOOK_CLIENT_SECRET=...
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Frontend Environment Variables

Create a `.env.production` file:

```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXTAUTH_URL=https://yourdomain.com
NEXTAUTH_SECRET=<generate-strong-random-key>

# OAuth Providers (optional)
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
FACEBOOK_CLIENT_ID=...
FACEBOOK_CLIENT_SECRET=...
```

---

## Database Setup

### 1. Create Database

**Using Neon DB:**
1. Sign up at https://neon.tech
2. Create a new project
3. Copy the connection string
4. Update DATABASE_URL in backend .env

**Using PostgreSQL:**
```bash
createdb todo_app_production
```

### 2. Run Migrations

```bash
cd phase-2-web/backend
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
alembic upgrade head
```

### 3. Verify Database Schema

```bash
# Connect to database
psql $DATABASE_URL

# List tables
\dt

# Expected tables:
# - user
# - task
# - conversation
# - alembic_version
```

---

## Backend Deployment

### Option 1: Railway

1. **Install Railway CLI:**
```bash
npm install -g @railway/cli
```

2. **Login and Initialize:**
```bash
railway login
cd phase-2-web/backend
railway init
```

3. **Add Environment Variables:**
```bash
railway variables set DATABASE_URL="postgresql://..."
railway variables set ANTHROPIC_API_KEY="sk-ant-..."
railway variables set SECRET_KEY="..."
# Add all other environment variables
```

4. **Deploy:**
```bash
railway up
```

5. **Run Migrations:**
```bash
railway run alembic upgrade head
```

### Option 2: Render

1. Create new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables in Render dashboard
5. Deploy

### Option 3: AWS EC2

1. **Launch EC2 Instance:**
   - Ubuntu 22.04 LTS
   - t2.small or larger
   - Open ports 80, 443, 8000

2. **SSH into instance and setup:**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.10 python3-pip python3-venv nginx -y

# Clone repository
git clone https://github.com/yourusername/todo-app.git
cd todo-app/phase-2-web/backend

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
nano .env
# Add all environment variables

# Run migrations
alembic upgrade head

# Install and configure supervisor
sudo apt install supervisor -y
sudo nano /etc/supervisor/conf.d/todo-backend.conf
```

**Supervisor Configuration:**
```ini
[program:todo-backend]
directory=/home/ubuntu/todo-app/phase-2-web/backend
command=/home/ubuntu/todo-app/phase-2-web/backend/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
user=ubuntu
autostart=true
autorestart=true
stderr_logfile=/var/log/todo-backend.err.log
stdout_logfile=/var/log/todo-backend.out.log
```

3. **Configure Nginx:**
```bash
sudo nano /etc/nginx/sites-available/todo-backend
```

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

4. **Enable site and restart:**
```bash
sudo ln -s /etc/nginx/sites-available/todo-backend /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start todo-backend
```

5. **Setup SSL with Let's Encrypt:**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d api.yourdomain.com
```

---

## Frontend Deployment

### Option 1: Vercel (Recommended)

1. **Install Vercel CLI:**
```bash
npm install -g vercel
```

2. **Deploy:**
```bash
cd phase-2-web/frontend
vercel
```

3. **Add Environment Variables:**
   - Go to Vercel dashboard
   - Project Settings > Environment Variables
   - Add all variables from `.env.production`

4. **Deploy to Production:**
```bash
vercel --prod
```

### Option 2: Netlify

1. **Install Netlify CLI:**
```bash
npm install -g netlify-cli
```

2. **Build and Deploy:**
```bash
cd phase-2-web/frontend
npm run build
netlify deploy --prod
```

3. **Configure Environment Variables:**
   - Go to Netlify dashboard
   - Site Settings > Environment Variables
   - Add all variables

### Option 3: AWS S3 + CloudFront

1. **Build the application:**
```bash
cd phase-2-web/frontend
npm run build
```

2. **Create S3 bucket:**
```bash
aws s3 mb s3://your-todo-app
aws s3 sync out/ s3://your-todo-app --acl public-read
```

3. **Configure CloudFront distribution**
4. **Setup custom domain and SSL certificate**

---

## Post-Deployment Verification

### Backend Health Check

```bash
# Check API is responding
curl https://api.yourdomain.com/docs

# Test authentication
curl -X POST https://api.yourdomain.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"testpass123"}'

# Test chat endpoint (with token)
curl -X POST https://api.yourdomain.com/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message":"list all tasks"}'
```

### Frontend Health Check

1. Visit https://yourdomain.com
2. Check console for errors
3. Test login functionality
4. Verify API connection

---

## Testing Checklist

### User Story 1: Natural Language Todo Management

#### Basic Commands
- [ ] "Add buy groceries" - Creates task
- [ ] "Add high priority task finish report" - Creates task with priority
- [ ] "List all my tasks" - Shows task list
- [ ] "Show my tasks" - Shows task list
- [ ] "Mark task complete" - Marks task as complete
- [ ] "Delete task" - Deletes task

#### Advanced Commands
- [ ] "Add buy groceries tomorrow" - Creates task with due date
- [ ] "Create urgent task call client" - Creates urgent priority task
- [ ] "Add task review code with tags work and urgent" - Creates task with tags
- [ ] "Update task priority to high" - Updates task priority
- [ ] "Change due date to next Monday" - Updates due date

#### Chat Interface
- [ ] Chat widget displays correctly
- [ ] Messages send successfully
- [ ] AI responses appear in chat
- [ ] Typing indicator shows while processing
- [ ] Error messages display for failed requests
- [ ] Conversation history persists

#### AI Agent
- [ ] Anthropic Claude processes commands (if configured)
- [ ] OpenAI GPT fallback works (if Anthropic unavailable)
- [ ] Intent analysis correctly identifies actions
- [ ] Parameter extraction works for dates, priorities, tags
- [ ] Natural language date parsing works ("tomorrow", "next week")

### User Story 2: Advanced Features

#### Recurring Tasks
- [ ] "Add daily standup every day at 9am" - Creates daily recurring task
- [ ] "Add weekly meeting every Monday" - Creates weekly recurring task
- [ ] "Add monthly report due last day of month" - Creates monthly recurring task
- [ ] Completing recurring task creates next occurrence
- [ ] Next occurrence has correct date based on pattern
- [ ] Recurrence pattern persists in database

#### Due Dates
- [ ] "Add task due tomorrow" - Parses "tomorrow"
- [ ] "Add task due next Monday" - Parses "next Monday"
- [ ] "Add task due in 3 days" - Parses relative dates
- [ ] "Add task due 2026-02-15" - Parses ISO dates
- [ ] Due date displays correctly in UI
- [ ] Tasks sorted by due date work

#### Notifications
- [ ] Browser notification permission prompt appears
- [ ] Notifications scheduled for tasks with due dates
- [ ] Notifications appear at correct time
- [ ] Notification shows task title and due date
- [ ] Clicking notification opens app
- [ ] Notification polling works (every 5 minutes)
- [ ] Mark notification as sent works

#### Priority and Tags
- [ ] Priority levels work (low, medium, high, urgent)
- [ ] Tags can be added to tasks
- [ ] Multiple tags per task work
- [ ] Filter by priority works
- [ ] Filter by tags works

### User Story 3: Enhanced UI

#### Layout Components
- [ ] Header displays correctly
- [ ] Footer displays correctly
- [ ] Sidebar displays correctly
- [ ] Layout is responsive on mobile
- [ ] Layout is responsive on tablet
- [ ] Layout is responsive on desktop

#### Theme System
- [ ] Light theme applies correctly
- [ ] Dark theme applies correctly
- [ ] Purple theme applies correctly
- [ ] Theme toggle works in header
- [ ] Theme preference persists after refresh
- [ ] Theme preference saves to backend
- [ ] Theme loads from backend on login

#### Authentication
- [ ] Email/password registration works
- [ ] Email/password login works
- [ ] Google OAuth login works (if configured)
- [ ] Facebook OAuth login works (if configured)
- [ ] Password visibility toggle works
- [ ] Password strength indicator shows correct strength
- [ ] Character length indicator updates in real-time
- [ ] JWT token stored correctly
- [ ] Protected routes require authentication
- [ ] Logout works correctly

#### Filtering and Sorting
- [ ] Filter by priority works
- [ ] Filter by status works
- [ ] Filter by tags works
- [ ] Filter by due date range works
- [ ] Sort by created date works
- [ ] Sort by due date works
- [ ] Sort by priority works
- [ ] Sort order (asc/desc) works
- [ ] Multiple filters work together
- [ ] Clear filters works

### Performance Testing

- [ ] Chat response time < 3 seconds (95th percentile)
- [ ] Task list loads < 1 second
- [ ] Page load time < 2 seconds
- [ ] API response time < 500ms for CRUD operations
- [ ] No memory leaks in frontend
- [ ] No memory leaks in backend

### Security Testing

- [ ] SQL injection protection works
- [ ] XSS protection works
- [ ] CSRF protection works
- [ ] JWT tokens expire correctly
- [ ] Password hashing works (bcrypt)
- [ ] OAuth tokens verified with providers
- [ ] Rate limiting works on chat endpoint
- [ ] CORS configured correctly
- [ ] HTTPS enforced in production

### Browser Compatibility

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS)
- [ ] Mobile Chrome (Android)

---

## Monitoring and Logging

### Backend Logging

Logs are written to:
- Console (stdout/stderr)
- Log files (if configured)

**Log Levels:**
- `INFO` - Normal operations
- `WARNING` - Potential issues
- `ERROR` - Errors with stack traces
- `DEBUG` - Detailed debugging info

**Key Log Events:**
- User authentication
- AI agent processing
- MCP tool calls
- Database operations
- API errors

### Frontend Logging

Check browser console for:
- API request/response errors
- React component errors
- Authentication issues
- WebSocket connection issues (if applicable)

### Monitoring Tools

**Recommended:**
- **Sentry** - Error tracking
- **LogRocket** - Session replay
- **DataDog** - APM and logging
- **Prometheus + Grafana** - Metrics

---

## Backup and Recovery

### Database Backups

**Automated Backups (Neon DB):**
- Automatic daily backups
- Point-in-time recovery

**Manual Backup:**
```bash
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

**Restore from Backup:**
```bash
psql $DATABASE_URL < backup_20260208.sql
```

### Application Backups

- Code: Git repository
- Environment variables: Secure vault (1Password, AWS Secrets Manager)
- User data: Database backups

---

## Rollback Procedure

If deployment fails:

1. **Revert Backend:**
```bash
# Railway
railway rollback

# Render
# Use Render dashboard to rollback

# AWS EC2
git checkout previous-commit
sudo supervisorctl restart todo-backend
```

2. **Revert Frontend:**
```bash
# Vercel
vercel rollback

# Netlify
# Use Netlify dashboard to rollback
```

3. **Rollback Database:**
```bash
# Downgrade one migration
alembic downgrade -1

# Downgrade to specific version
alembic downgrade <revision_id>
```

---

## Troubleshooting

### Backend Issues

**Issue: Database connection fails**
- Check DATABASE_URL is correct
- Verify database is running
- Check firewall rules
- Verify SSL mode if required

**Issue: AI service errors**
- Verify API keys are valid
- Check API rate limits
- Ensure at least one provider is configured
- Check API service status

**Issue: CORS errors**
- Add frontend domain to ALLOWED_ORIGINS
- Verify CORS middleware is configured
- Check preflight requests

### Frontend Issues

**Issue: API requests fail**
- Verify NEXT_PUBLIC_API_URL is correct
- Check CORS configuration
- Verify authentication token
- Check browser console for errors

**Issue: OAuth login fails**
- Verify OAuth credentials
- Check redirect URLs in provider console
- Verify NEXTAUTH_SECRET is set
- Check callback URL configuration

**Issue: Notifications don't work**
- Check browser notification permissions
- Verify notification service is running
- Check notification polling interval
- Verify due dates are set correctly

---

## Performance Optimization

### Backend

1. **Database Indexing:**
```sql
CREATE INDEX idx_task_user_id ON task(user_id);
CREATE INDEX idx_task_due_date ON task(due_date);
CREATE INDEX idx_task_status ON task(status);
```

2. **Caching:**
- Add Redis for session caching
- Cache AI responses for common queries
- Cache user preferences

3. **Connection Pooling:**
- Configure SQLAlchemy pool size
- Use connection pooling for database

### Frontend

1. **Code Splitting:**
- Already enabled with Next.js
- Lazy load heavy components

2. **Image Optimization:**
- Use Next.js Image component
- Optimize images before upload

3. **Bundle Size:**
```bash
npm run build
# Check bundle size in output
```

---

## Success Criteria Validation

From spec.md, verify:

- [ ] **95% accuracy** - AI correctly interprets natural language commands
- [ ] **3-second response time** - Chat responses within 3 seconds (95th percentile)
- [ ] **Recurring tasks work** - Auto-rescheduling functions correctly
- [ ] **Notifications delivered** - Browser notifications appear on time
- [ ] **Theme persistence** - Theme preference saves and loads correctly
- [ ] **OAuth works** - Google/Facebook login functional
- [ ] **Mobile responsive** - UI works on mobile devices
- [ ] **Error handling** - Graceful error messages for all failures

---

## Maintenance

### Regular Tasks

**Daily:**
- Monitor error logs
- Check API response times
- Verify backup completion

**Weekly:**
- Review user feedback
- Check database size
- Update dependencies (security patches)

**Monthly:**
- Full security audit
- Performance review
- Dependency updates (minor versions)

### Updating Dependencies

**Backend:**
```bash
pip list --outdated
pip install --upgrade package-name
pip freeze > requirements.txt
```

**Frontend:**
```bash
npm outdated
npm update
npm audit fix
```

---

## Support and Documentation

- **API Docs:** https://api.yourdomain.com/docs
- **README:** See README.md in repository
- **Specs:** See specs/ directory for design documents
- **Issues:** Report on GitHub

---

## Conclusion

This guide covers deployment, testing, and maintenance of the AI-powered todo application. Follow the checklists systematically to ensure a successful deployment.

For additional help, refer to:
- README.md - Setup instructions
- docs/api.md - API documentation
- specs/phase3-ai-chatbot/ - Design specifications

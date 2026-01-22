# 🚀 RecallX Login System - Quick Start Guide

## Installation & Setup

### Step 1: Install Dependencies
```bash
cd RecallX
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

### Step 3: Open in Browser
Go to: `http://localhost:5000`

---

## Using the Login System

### 🔐 Demo Credentials (Pre-configured)
**Username:** `demo_user`
**Password:** `demo_password_123`

Use these to test all features immediately!

### 📝 Create New Account
1. Click **"Sign Up"** button in navbar
2. Fill in the registration form:
   - Username (3-100 characters)
   - Email address
   - Password (min 6 chars, must include uppercase & number)
   - Confirm password
3. Click **"Create Account"**
4. You'll be redirected to login
5. Enter your new credentials

### 🔑 Login
1. Click **"Login"** button
2. Enter username and password
3. Check **"Remember me"** to stay logged in 30 days (optional)
4. Click **"Login"**
5. You'll be redirected to your dashboard

### 🚪 Logout
Click **"Logout"** button in navbar (visible when logged in)

---

## Features

✅ **Secure Authentication** - Passwords are encrypted with bcrypt  
✅ **Session Management** - Automatic login persistence  
✅ **User Isolation** - Each user sees only their topics  
✅ **Real-time Validation** - Password strength checker  
✅ **Mobile Responsive** - Works on all devices  
✅ **Error Messages** - Clear feedback on issues  
✅ **Demo Account** - Test without registering  

---

## Navigation Guide

| Page | Path | Required Login? |
|------|------|-----------------|
| Home | `/` | No |
| Login | `/login` | No |
| Register | `/register` | No |
| Dashboard | `/dashboard` | Yes ✓ |
| Add Topic | `/add-topic` | Yes ✓ |
| Upload PDF | `/upload` | Yes ✓ |
| Performance Report | `/report` | Yes ✓ |
| Forgetting Curve | `/forgetting-curve/<id>` | Yes ✓ |
| Stress Test | `/stress-test/<id>` | Yes ✓ |

---

## Workflow Example

```
1. Open http://localhost:5000
   ↓
2. Click "Login" or "Sign Up"
   ↓
3. Enter credentials (use demo_user / demo_password_123)
   ↓
4. Click "Login" → You're in the dashboard!
   ↓
5. See your topics and study stats
   ↓
6. Create new topic → Add content → Study → Get reports
   ↓
7. Click "Logout" when done
```

---

## Troubleshooting

**Q: "Invalid username or password"**
- Check your username/password are correct
- Use demo_user / demo_password_123 to test
- Passwords are case-sensitive

**Q: "Username already exists"**
- Choose a different username when registering
- Try demo_user if you haven't created one yet

**Q: "Password must be at least 6 characters"**
- Use a password with at least 6 characters
- Include at least one uppercase letter (A-Z)
- Include at least one number (0-9)

**Q: "All fields are required"**
- Make sure you filled in all form fields
- Don't leave any blank

**Q: Logged out after closing browser?**
- Check "Remember me" on login to persist session
- Default session expires when browser closes

**Q: Can't access dashboard after login?**
- The page might be loading - wait a moment
- Check if you're actually logged in (look for username in navbar)
- Try logging in again

---

## For Developers

### Key Files Modified:
- `app.py` - Authentication routes & logic
- `requirements.txt` - New dependencies
- `templates/login.html` - Login page
- `templates/register.html` - Registration page
- `templates/index.html` - Updated navbar
- `static/css/style.css` - New button styles

### Key Components:
```python
# Password hashing
user.set_password("password123")  # Creates hash
user.check_password("password123")  # Returns True/False

# Session management
@login_required  # Decorator to protect routes
current_user  # Access logged-in user anywhere

# Authentication
login_user(user)  # Create session
logout_user()  # Destroy session
```

### Database:
- Users stored in `instance/database.db`
- Passwords stored as bcrypt hashes (never plain text)
- Each topic is linked to a user ID

---

## Security Notes

🔒 **Good Security Practices Applied:**
- Passwords encrypted with bcrypt
- Session-based authentication
- CSRF protection enabled
- SQL injection prevention (SQLAlchemy ORM)
- User data isolation

⚠️ **For Production Use:**
- Change the SECRET_KEY to a random value
- Use environment variables for config
- Enable HTTPS
- Add rate limiting on login
- Consider email verification
- Add password reset functionality

---

## Next Steps

After login:
1. Add a new study topic
2. Upload learning materials (PDFs)
3. Generate AI questions
4. Track your forgetting curve
5. Take stress-based recall tests
6. View performance reports
7. Review Forgettable Topic Index

---

## Support

For issues:
1. Check the troubleshooting section above
2. Verify all dependencies installed: `pip list`
3. Restart the app: Stop and run `python app.py` again
4. Clear browser cache if needed
5. Check console for error messages

---

## Demo Walkthrough

**Login with demo account:**
```
1. Go to http://localhost:5000
2. Click "Login" in navbar
3. Username: demo_user
4. Password: demo_password_123
5. Click "Login" button
6. Explore dashboard with pre-loaded sample topics
7. Try stress test, forgetting curve, and reports
```

**Create your own account:**
```
1. Go to http://localhost:5000
2. Click "Sign Up" in navbar
3. Username: yourname (any unique name)
4. Email: your@email.com
5. Password: MyPassword123 (6+ chars, uppercase, number)
6. Confirm password: MyPassword123
7. Click "Create Account"
8. You'll be taken to login - enter your new credentials
9. Your personal dashboard will load (empty initially)
10. Add your first topic to get started!
```

---

Enjoy using RecallX! 🎓

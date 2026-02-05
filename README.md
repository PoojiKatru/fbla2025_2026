# ByteSized Business Boost - Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Move the HTML file**
   ```bash
   # Copy index.html to the same directory as backend.py
   cp index.html backend.py requirements.txt to_the_same_folder/
   ```

3. **Run the Backend Server**
   ```bash
   python backend.py
   ```

4. **Open Your Browser**
   Navigate to: `http://localhost:5000`

## 📧 How It Works

### Signup Flow:
1. User fills out signup form (name, email, password)
2. Backend creates account and generates verification token
3. Verification email is printed to console (check your terminal!)
4. User sees confirmation screen with their email
5. User clicks verification link from email
6. Account is verified
7. User can now log in

### Email Verification (Development Mode):
Currently, the verification emails are **printed to the console** where you ran `python backend.py`. Look for a section like:

```
============================================================
VERIFICATION EMAIL
============================================================
To: user@example.com
Subject: Verify Your ByteSized Business Boost Account

Hi John Doe,

Thank you for signing up! Please verify your email by clicking:

http://localhost:5000/verify/abc123xyz...
============================================================
```

**To verify your account:**
- Copy the verification link from the console
- Paste it into your browser
- You'll see a success page
- Now you can log in!

### For Production (Actual Email Sending):
To send real emails, you need to:
1. Uncomment the SMTP code in `backend.py` (lines marked with `"""`)
2. Set up an email service (Gmail, SendGrid, etc.)
3. Add your SMTP credentials

Example for Gmail:
```python
sender_email = "your-email@gmail.com"
sender_password = "your-app-password"  # Generate from Google Account settings
```

## 🗄️ Database

The app uses SQLite (file: `business_boost.db`) which is created automatically when you first run the server.

### Database Schema:
```sql
users table:
- id (INTEGER PRIMARY KEY)
- name (TEXT)
- email (TEXT UNIQUE)
- password_hash (TEXT)
- verification_token (TEXT)
- is_verified (BOOLEAN)
- created_at (TIMESTAMP)
```

## 🔐 Security Notes

**Current Implementation (Development Only):**
- Passwords are hashed with SHA-256
- No rate limiting
- No CSRF protection
- Tokens stored in localStorage

**For Production, You Should Add:**
- Use bcrypt or Argon2 for password hashing
- Implement JWT tokens for authentication
- Add rate limiting to prevent brute force attacks
- Use HTTPS
- Add CSRF tokens
- Implement session management
- Add reCAPTCHA for bot prevention
- Use environment variables for sensitive data

## 📝 Testing the Flow

1. **Sign Up:**
   - Go to http://localhost:5000
   - Click "Get Started"
   - Click "Sign Up" tab
   - Fill in your details
   - Click "Create Account"

2. **Verify Email:**
   - Check the console where backend.py is running
   - Copy the verification link
   - Open it in your browser
   - See success message

3. **Log In:**
   - Click "Go to Login"
   - Enter your email and password
   - Click "Login"
   - You're in the dashboard!

## 🎨 Features Implemented

✅ Beautiful gradient welcome page with animations
✅ Login/Signup modal with tab switching
✅ Email verification flow
✅ Verification confirmation screen
✅ SQLite database for user storage
✅ Password hashing
✅ Success/error message handling
✅ Empty dashboard (ready for customization)

## 🔧 Troubleshooting

**Port already in use:**
```bash
# Change port in backend.py (last line):
app.run(debug=True, port=5001)  # Use 5001 instead
```

**Database locked:**
```bash
# Delete the database and restart:
rm business_boost.db
python backend.py
```

**Module not found:**
```bash
# Reinstall dependencies:
pip install -r requirements.txt
```

## 📂 File Structure

```
project/
├── index.html          # Frontend (with embedded CSS/JS)
├── backend.py          # Flask backend server
├── requirements.txt    # Python dependencies
├── business_boost.db   # SQLite database (auto-created)
└── README.md          # This file
```

## 🎯 Next Steps

Now that authentication is working, you can:
- Design your dashboard layout
- Add business listing features
- Implement search and filtering
- Create review/rating system
- Add favorite/bookmark functionality
- Build the deals/coupons section

Have fun building! 🚀

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
import hashlib
import secrets
import os
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Database setup
DATABASE = 'business_boost.db'

def init_db():
    """Initialize the database with users table"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            verification_token TEXT,
            is_verified BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def send_verification_email(email, name, token):
    """
    Send verification email to user
    Note: For production, you'll need to configure SMTP settings
    For now, this will just print the verification link
    """
    verification_link = f"http://localhost:5000/verify/{token}"
    
    # In production, you would send actual email here
    # For demo purposes, we'll just print it
    print("\n" + "="*60)
    print("VERIFICATION EMAIL")
    print("="*60)
    print(f"To: {email}")
    print(f"Subject: Verify Your ByteSized Business Boost Account")
    print(f"\nHi {name},")
    print(f"\nThank you for signing up! Please verify your email by clicking:")
    print(f"\n{verification_link}")
    print("\n" + "="*60 + "\n")
    
    # Uncomment below for actual email sending (requires SMTP configuration)
    """
    sender_email = "your-email@gmail.com"
    sender_password = "your-app-password"
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "Verify Your ByteSized Business Boost Account"
    message["From"] = sender_email
    message["To"] = email
    
    html = f'''
    <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; text-align: center;">
                <h1 style="color: white; margin: 0;">🏪 ByteSized Business Boost</h1>
            </div>
            <div style="padding: 40px; background: #f5f5f5;">
                <h2>Hi {name},</h2>
                <p>Thank you for signing up! Please verify your email address to complete your registration.</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_link}" 
                       style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                              color: white; padding: 15px 40px; text-decoration: none; 
                              border-radius: 8px; display: inline-block; font-weight: bold;">
                        Verify Email
                    </a>
                </div>
                <p style="color: #666; font-size: 14px;">
                    If you didn't create this account, please ignore this email.
                </p>
            </div>
        </body>
    </html>
    '''
    
    part = MIMEText(html, "html")
    message.attach(part)
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, message.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")
    """
    
    return True

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/api/signup', methods=['POST'])
def signup():
    """Handle user signup"""
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        # Validate input
        if not all([name, email, password]):
            return jsonify({
                'success': False,
                'message': 'All fields are required'
            }), 400
        
        # Generate verification token
        verification_token = secrets.token_urlsafe(32)
        
        # Hash password
        password_hash = hash_password(password)
        
        # Insert user into database
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (name, email, password_hash, verification_token, is_verified)
                VALUES (?, ?, ?, ?, 0)
            ''', (name, email, password_hash, verification_token))
            
            conn.commit()
            
            # Send verification email
            send_verification_email(email, name, verification_token)
            
            return jsonify({
                'success': True,
                'message': 'Account created! Please check your email for verification.'
            })
            
        except sqlite3.IntegrityError:
            return jsonify({
                'success': False,
                'message': 'An account with this email already exists'
            }), 400
        finally:
            conn.close()
            
    except Exception as e:
        print(f"Error in signup: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred during signup'
        }), 500

@app.route('/verify/<token>')
def verify_email(token):
    """Verify user email with token"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users 
        SET is_verified = 1, verification_token = NULL
        WHERE verification_token = ?
    ''', (token,))
    
    if cursor.rowcount > 0:
        conn.commit()
        conn.close()
        
        # Return a success page
        return '''
        <html>
            <head>
                <title>Email Verified!</title>
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        min-height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    }
                    .container {
                        background: white;
                        padding: 60px;
                        border-radius: 20px;
                        text-align: center;
                        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                    }
                    h1 { color: #667eea; margin-bottom: 20px; }
                    p { color: #666; margin-bottom: 30px; }
                    a {
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 15px 40px;
                        text-decoration: none;
                        border-radius: 8px;
                        display: inline-block;
                        font-weight: bold;
                    }
                    .icon { font-size: 80px; margin-bottom: 20px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="icon">✅</div>
                    <h1>Email Verified!</h1>
                    <p>Your account has been successfully verified.<br>You can now log in to your account.</p>
                    <a href="/">Go to Login</a>
                </div>
            </body>
        </html>
        '''
    else:
        conn.close()
        return '''
        <html>
            <head>
                <title>Verification Failed</title>
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        min-height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    }
                    .container {
                        background: white;
                        padding: 60px;
                        border-radius: 20px;
                        text-align: center;
                        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                    }
                    h1 { color: #e74c3c; margin-bottom: 20px; }
                    p { color: #666; }
                    .icon { font-size: 80px; margin-bottom: 20px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="icon">❌</div>
                    <h1>Invalid Token</h1>
                    <p>This verification link is invalid or has already been used.</p>
                </div>
            </body>
        </html>
        ''', 400

@app.route('/api/login', methods=['POST'])
def login():
    """Handle user login"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        password_hash = hash_password(password)
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, is_verified 
            FROM users 
            WHERE email = ? AND password_hash = ?
        ''', (email, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            if not user[2]:  # is_verified
                return jsonify({
                    'success': False,
                    'message': 'Please verify your email before logging in'
                }), 403
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user[0],
                    'name': user[1]
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
            
    except Exception as e:
        print(f"Error in login: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred during login'
        }), 500

if __name__ == '__main__':
    # Initialize database
    init_db()
    print("\n🚀 Starting ByteSized Business Boost Server...")
    print("📧 Verification emails will be printed to console")
    print("🌐 Open http://localhost:5000 in your browser\n")
    
    # Run the app
    app.run(debug=True, port=5000)

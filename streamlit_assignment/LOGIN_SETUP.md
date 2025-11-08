# User Authentication Setup

## Overview
The KaviHealthCare application now includes a secure login system with user management capabilities.

## Features

### 🔐 Login System
- **Landing Page**: All users must login before accessing the application
- **Session Management**: User sessions are maintained throughout the application
- **Logout**: Users can logout at any time from the main interface

### 👥 User Roles

#### Admin Role
- **Default Credentials**: 
  - Username: `admin`
  - Password: `admin`
- **Capabilities**:
  - Create new users
  - View all users
  - Delete users (except admin)
  - Full access to patient management

#### Regular User Role
- **Capabilities**:
  - Full access to patient management (Add, Edit, Delete, Search)
  - Cannot access user management features
- **Creation**: Only admin can create new users

### 🎯 User Management (Admin Only)

#### Create New User
1. Login as admin
2. Click "Manage Users" in the sidebar
3. Go to "Create User" tab
4. Enter username and password
5. Confirm password
6. Click "Create User"

**Validation Rules**:
- Username must be at least 3 characters
- Username must be unique
- Password must be at least 3 characters
- Passwords must match

#### View Users
- See all registered users
- View user details (ID, username, role, created date, created by)
- Users list shows who created each user

#### Delete User
- Select a user from the dropdown
- Click "Delete Selected User"
- Admin account cannot be deleted

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT
);
```

## Usage Flow

### First Time Setup
1. Run the application
2. Login with admin/admin
3. Create users for your team
4. Users can now login with their credentials

### Daily Usage
1. Open application → Login page appears
2. Enter credentials
3. Access patient management
4. Logout when done

## Security Notes

⚠️ **Important**: This is a basic authentication system suitable for learning purposes. For production use, consider:
- Password hashing (bcrypt, argon2)
- Password strength requirements
- Session timeout
- HTTPS/SSL
- Password reset functionality
- Multi-factor authentication
- Rate limiting for login attempts

## Testing

### Test the Login System
1. Start the application: `streamlit run src/kavihealthcare.py`
2. Try logging in with admin/admin
3. Create a test user
4. Logout
5. Login with the test user
6. Verify the test user cannot access user management

### Test User Management
1. Login as admin
2. Create multiple users
3. View user list
4. Try deleting a user
5. Verify deleted user cannot login

## Troubleshooting

### Database Issues
If you encounter database issues:
```bash
# Remove the database and restart
rm patients.db
streamlit run src/kavihealthcare.py
```

### Admin Not Found
The admin user is automatically created on first run. If missing:
- Delete patients.db
- Restart the application
- Admin will be recreated automatically

## File Changes Made

1. **database/connection.py**
   - Added `init_users_table()` function
   - Auto-creates admin user

2. **database/operations.py**
   - Added `authenticate_user()`
   - Added `create_user()`
   - Added `fetch_all_users()`
   - Added `delete_user()`
   - Added `user_exists()`

3. **database/__init__.py**
   - Exported new user management functions

4. **kavihealthcare.py**
   - Added `login_page()` function
   - Added `user_management_section()` function
   - Updated `main()` with authentication check
   - Added session state management
   - Added logout functionality

## Next Steps

Consider implementing:
- Password change functionality
- Password strength indicator
- Remember me option
- Session timeout
- Audit logging
- Password reset via email

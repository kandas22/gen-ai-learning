# Authentication Flow Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    KaviHealthCare Application                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
                  ┌─────────────────┐
                  │  Login Page     │ ◄── Landing Page
                  │  (Not Logged In)│
                  └────────┬────────┘
                           │
                  ┌────────▼─────────┐
                  │ Enter Credentials│
                  │  Username/Password│
                  └────────┬─────────┘
                           │
                  ┌────────▼──────────┐
                  │  Authenticate     │
                  │  Check Database   │
                  └────────┬──────────┘
                           │
              ┌────────────┴────────────┐
              │                         │
        ┌─────▼──────┐           ┌─────▼──────┐
        │   Valid    │           │  Invalid   │
        │Credentials │           │Credentials │
        └─────┬──────┘           └─────┬──────┘
              │                         │
              │                         ▼
              │                  ┌──────────────┐
              │                  │ Show Error   │
              │                  │ Stay on Login│
              │                  └──────────────┘
              │
              ▼
    ┌──────────────────┐
    │ Set Session State│
    │  - authenticated │
    │  - username      │
    │  - role          │
    └────────┬─────────┘
             │
             ▼
    ┌─────────────────────────────────┐
    │    Main Application Access      │
    └─────────────────────────────────┘
             │
      ┌──────┴──────┐
      │             │
┌─────▼─────┐  ┌────▼────────┐
│Admin Role │  │  User Role  │
└─────┬─────┘  └────┬────────┘
      │             │
      │             └──────────────────┐
      │                                │
      ▼                                ▼
┌────────────────────┐     ┌──────────────────────┐
│ Full Access:       │     │ Access:              │
│ - Patient Mgmt     │     │ - Patient Management │
│ - User Management  │     │   (Add/Edit/Delete)  │
│   • Create Users   │     │ - Search & Filter    │
│   • View Users     │     │ - Export CSV         │
│   • Delete Users   │     │                      │
└────────────────────┘     └──────────────────────┘
```

## User Management Flow (Admin Only)

```
┌──────────────────────────────────────────────────┐
│            Admin User Management                 │
└──────────────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   ┌────▼────────┐         ┌─────▼──────┐
   │Create User  │         │ View Users │
   └────┬────────┘         └─────┬──────┘
        │                        │
        ▼                        ▼
┌──────────────────┐    ┌────────────────┐
│ Enter Details:   │    │ Display Table: │
│ - Username (new) │    │ - All Users    │
│ - Password       │    │ - Details      │
│ - Confirm Pass   │    │ - Created By   │
└────────┬─────────┘    └────────┬───────┘
         │                       │
         ▼                       ▼
┌──────────────────┐    ┌────────────────┐
│ Validate:        │    │ Select User    │
│ - Username ≥3    │    │ to Delete      │
│ - Unique Name    │    └────────┬───────┘
│ - Password ≥3    │             │
│ - Passwords Match│             ▼
└────────┬─────────┘    ┌────────────────┐
         │              │ Delete User    │
         ▼              │ (except admin) │
┌──────────────────┐    └────────────────┘
│ Create in DB:    │
│ - role='user'    │
│ - created_by     │
└──────────────────┘
```

## Session State Management

```
┌──────────────────────────────────────┐
│         Session State Keys           │
└──────────────────────────────────────┘

st.session_state = {
    "authenticated": True/False,
    "username": "admin",
    "role": "admin" or "user",
    "show_user_management": True/False
}

┌──────────────────────────────────────┐
│        Session Lifecycle             │
└──────────────────────────────────────┘

1. App Start
   └─► authenticated = False
       └─► Show Login Page

2. Successful Login
   └─► Set authenticated = True
   └─► Set username, role
   └─► Rerun app
       └─► Show Main App

3. Logout Button Click
   └─► Clear all session keys
   └─► Set authenticated = False
   └─► Rerun app
       └─► Show Login Page
```

## Database Tables Relationship

```
┌──────────────────────────────────────────┐
│           patients.db                    │
└──────────────────────────────────────────┘
                  │
         ┌────────┴────────┐
         │                 │
    ┌────▼─────┐    ┌──────▼──────┐
    │  users   │    │  patients   │
    └────┬─────┘    └──────┬──────┘
         │                 │
         │                 │
┌────────▼────────┐   ┌────▼────────────┐
│ • id (PK)       │   │ • id (PK)       │
│ • username      │   │ • first_name    │
│ • password      │   │ • last_name     │
│ • role          │   │ • phone         │
│ • created_at    │   │ • email         │
│ • created_by    │   │ • address       │
└─────────────────┘   │ • created_at    │
                      └─────────────────┘

Note: No foreign key relationship
(users table is independent)
```

## Security Considerations

```
┌──────────────────────────────────────────────┐
│         Current Implementation               │
└──────────────────────────────────────────────┘
✓ Login required for all pages
✓ Role-based access control
✓ Session state management
✓ Username uniqueness validation
✓ Password confirmation

┌──────────────────────────────────────────────┐
│      Production Recommendations              │
└──────────────────────────────────────────────┘
⚠ Add password hashing (bcrypt/argon2)
⚠ Implement session timeout
⚠ Add HTTPS/SSL encryption
⚠ Add password strength requirements
⚠ Implement rate limiting
⚠ Add audit logging
⚠ Add password reset functionality
⚠ Consider 2FA/MFA
```

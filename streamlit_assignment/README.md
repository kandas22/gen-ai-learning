# KaviHealthCare App - Patient Profile Management System

A comprehensive patient profile management system built with Streamlit and SQLite, featuring a modular architecture with separated database operations.

## 🏥 Overview

KaviHealthCare App is a web-based patient management system that allows healthcare professionals to:
- Add new patient records
- Search and filter existing patients
- Edit patient information
- Delete patient records
- Import patients from CSV files
- Export patient data to CSV

## ✨ Features

### Core Functionality
- ✅ **CRUD Operations**: Create, Read, Update, Delete patient records
- 🔍 **Advanced Search**: Filter patients by name, phone, or email
- 📊 **Data Export**: Download patient data as CSV
- 📥 **Bulk Import**: Import multiple patients from CSV files
- ✉️ **Email Validation**: Optional email field with validation
- 📱 **Phone Validation**: Ensures phone numbers have 7-15 digits
- 💾 **SQLite Database**: Persistent data storage
- 🎨 **Responsive UI**: Clean, modern interface with Streamlit

### Data Fields
- **First Name** (required)
- **Last Name** (required)
- **Phone** (required, 7-15 digits)
- **Email** (optional, validated if provided)
- **Address** (required)
- **Created At** (auto-generated timestamp)

## 📁 Code Structure

```
streamlit_assignment/
│
├── src/
│   ├── kavihealthcare.py          # Main Streamlit application
│   │
│   └── database/                  # Database package
│       ├── __init__.py            # Package initialization & exports
│       ├── connection.py          # Database connection & schema
│       └── operations.py          # CRUD operations
│
├── tests/
│   ├── test_kavihealthcare.py     # Comprehensive test suite (30 tests)
│   └── conftest.py                # Test fixtures
│
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── README_TESTS.md               # Testing documentation
```

### Module Breakdown

#### `src/kavihealthcare.py` (Main Application)
- **Purpose**: Streamlit UI and application logic
- **Key Components**:
  - User interface with sidebar navigation
  - Form handling for add/edit operations
  - Search and filter functionality
  - CSV import/export features
  - Validation functions for phone and email
  - Data visualization with pandas DataFrames

#### `src/database/__init__.py` (Package Interface)
- **Purpose**: Exposes database operations to the main app
- **Exports**: All database functions for easy import

#### `src/database/connection.py` (Database Layer)
- **Purpose**: Database connection and initialization
- **Functions**:
  - `get_connection()`: Creates SQLite connection with row factory
  - `init_db()`: Creates patients table schema
- **Constants**:
  - `DB_PATH`: Default database file path
  - `TABLE_NAME`: Patients table name

#### `src/database/operations.py` (Data Layer)
- **Purpose**: All CRUD operations for patient records
- **Functions**:
  - `insert_patient()`: Add new patient record
  - `update_patient()`: Update existing patient
  - `delete_patient()`: Remove patient record
  - `fetch_all_patients()`: Get all patients as DataFrame
  - `fetch_patient_by_id()`: Get single patient by ID

## 🚀 Step-by-Step Execution Guide

### Prerequisites

**For Local Development:**
- Python 3.11 or higher
- pip (Python package installer)
- Terminal/Command Prompt access

**For Docker Deployment:**
- Docker Engine 20.10+ ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose 2.0+ (included with Docker Desktop)

---

## 📦 Deployment Options

Choose one of the following deployment methods:

### Option A: Local Development Setup
### Option B: Docker Deployment (Production-Ready)

---

## Option A: Local Development Setup

### Step 1: Navigate to Project Directory

```bash
cd /path/to/gen-ai-learning/streamlit_assignment
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# The .venv folder will be created in your current directory
```

### Step 3: Activate Virtual Environment

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows:**
```cmd
.venv\Scripts\activate
```

**On Windows PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

✅ **Verify Activation**: Your terminal prompt should now show `(.venv)` at the beginning.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `streamlit==1.51.0` - Web application framework
- `pandas==2.3.3` - Data manipulation and analysis
- `validators==0.35.0` - Email validation
- `pytest==8.4.2` - Testing framework
- `pytest-cov==7.0.0` - Test coverage reporting

### Step 5: Run the Application

```bash
streamlit run src/kavihealthcare.py
```

### Step 6: Access the Application

After running the command, Streamlit will automatically:
1. Start a local web server
2. Open your default browser
3. Navigate to `http://localhost:8501`

**Expected Terminal Output:**
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

If the browser doesn't open automatically, manually navigate to: **http://localhost:8501**

### Step 7: Use the Application

#### Adding a Patient
1. In the sidebar, select **"Add patient"**
2. Fill in the required fields:
   - First Name
   - Last Name
   - Phone (7-15 digits)
   - Address
3. Optionally add email
4. Click **"Add patient"** button

#### Viewing & Managing Patients
1. In the sidebar, select **"View & manage patients"**
2. View the patient list in the table
3. Use the sidebar filters to search:
   - Name contains (searches first or last name)
   - Phone contains
   - Email contains
4. Click **"Apply filters"** to filter results
5. Select a patient ID from the dropdown to edit or delete

#### Editing a Patient
1. Select patient from dropdown
2. Modify the fields in the form
3. Click **"Save changes"**

#### Deleting a Patient
1. Select patient from dropdown
2. Scroll to **"Danger zone"**
3. Click **"Delete this patient"**

#### Importing from CSV
1. In the sidebar, select **"Import (CSV)"**
2. Prepare CSV with columns: `first_name`, `last_name`, `phone`, `email`, `address`
3. Click **"Upload CSV"** and select your file
4. Preview the data
5. Click **"Import rows"** to add patients

#### Exporting to CSV
1. Go to **"View & manage patients"**
2. Apply any filters (optional)
3. Click **"Download visible as CSV"** button
4. CSV file will be downloaded with visible patient records

### Step 8: Stopping the Application

Press `Ctrl+C` in the terminal to stop the Streamlit server.

### Step 9: Deactivate Virtual Environment

```bash
deactivate
```

---

## Option B: Docker Deployment (Production-Ready)

Docker deployment provides a consistent, isolated environment suitable for production use.

### Step 1: Verify Docker Installation

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker-compose --version
```

Expected output:
```
Docker version 24.0.x or higher
Docker Compose version 2.x.x or higher
```

### Step 2: Navigate to Project Directory

```bash
cd /path/to/gen-ai-learning/streamlit_assignment
```

### Step 3: Build Docker Image

```bash
# Build the Docker image
docker build -t kavihealthcare-app .
```

This will:
- Create a lightweight Python 3.11 container
- Install all dependencies
- Copy application code
- Configure security settings (non-root user)
- Set up health checks

**Build time:** ~2-3 minutes (first time)

### Step 4: Run with Docker Compose (Recommended)

```bash
# Start the application
docker-compose up -d
```

**Flags explained:**
- `-d` = Detached mode (runs in background)

**What happens:**
- ✅ Creates container named `kavihealthcare-app`
- ✅ Exposes port 8501
- ✅ Creates `./data` directory for database persistence
- ✅ Configures health checks
- ✅ Sets restart policy

### Step 5: Verify Container is Running

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs -f kavihealthcare
```

**Expected output:**
```
NAME                   STATUS              PORTS
kavihealthcare-app     Up (healthy)        0.0.0.0:8501->8501/tcp
```

### Step 6: Access the Application

Open your browser and navigate to:
```
http://localhost:8501
```

The application is now running in a production-ready container! 🎉

### Step 7: Managing the Docker Container

#### View Logs
```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View last 100 lines
docker-compose logs --tail=100
```

#### Stop the Application
```bash
# Stop container (preserves data)
docker-compose stop

# Stop and remove container (preserves data in ./data)
docker-compose down
```

#### Restart the Application
```bash
docker-compose restart
```

#### Check Health Status
```bash
docker inspect --format='{{.State.Health.Status}}' kavihealthcare-app
```

### Step 8: Database Persistence

The database is stored in the `./data` directory on your host machine:
```
streamlit_assignment/
├── data/
│   └── patients.db    # Persisted outside container
```

**Benefits:**
- ✅ Data survives container restarts
- ✅ Easy to backup
- ✅ Can be accessed directly if needed

### Step 9: Backup Database

```bash
# Create backup
cp data/patients.db data/backup_$(date +%Y%m%d_%H%M%S).db

# Or from within container
docker exec kavihealthcare-app cp /app/data/patients.db /app/data/backup.db
```

### Step 10: Update Application

When you make code changes:

```bash
# Rebuild image
docker-compose build

# Restart with new image
docker-compose up -d
```

### Alternative: Docker Run (Without Compose)

```bash
# Run container directly
docker run -d \
  --name kavihealthcare-app \
  -p 8501:8501 \
  -v $(pwd)/data:/app/data \
  --restart unless-stopped \
  kavihealthcare-app
```

### Docker Commands Quick Reference

| Action | Command |
|--------|---------|
| Start application | `docker-compose up -d` |
| Stop application | `docker-compose stop` |
| View logs | `docker-compose logs -f` |
| Restart application | `docker-compose restart` |
| Remove container | `docker-compose down` |
| Rebuild image | `docker-compose build` |
| Check status | `docker-compose ps` |
| Enter container | `docker exec -it kavihealthcare-app sh` |

---

## 🧪 Running Tests

### Run All Tests
```bash
pytest tests/test_kavihealthcare.py -v
```

### Run with Coverage Report
```bash
pytest tests/test_kavihealthcare.py -v --cov=src --cov-report=html
```

### View Coverage Report
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

**Test Suite Includes:**
- 30 comprehensive tests
- Database operations testing
- CRUD operations validation
- Input validation tests
- Integration tests
- Edge case handling

See `README_TESTS.md` for detailed testing documentation.

## 📊 Database Information

### Database File
- **Location**: `patients.db` (created in the same directory as the app)
- **Type**: SQLite3
- **Auto-created**: First time you run the app

### Database Schema

```sql
CREATE TABLE patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT,
    address TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔧 Configuration

### Changing Database Path

Edit `src/database/connection.py`:
```python
DB_PATH = "your_custom_path/patients.db"
```

### Changing Port

Run with custom port:
```bash
streamlit run src/kavihealthcare.py --server.port 8502
```

### Headless Mode (No Browser Auto-open)

```bash
streamlit run src/kavihealthcare.py --server.headless true
```

## 📝 Validation Rules

### Phone Number Validation
- ✅ Must contain 7-15 digits
- ✅ Can include spaces, hyphens, and + symbol
- ✅ Extracted digits must be in valid range
- ❌ Letters not allowed

**Valid Examples:**
- `1234567890`
- `+1 (555) 123-4567`
- `555-1234`

### Email Validation
- ✅ Optional field
- ✅ Must be valid email format if provided
- ✅ Uses `validators` library
- ✅ Empty email is accepted

**Valid Examples:**
- `user@example.com`
- `john.doe@company.co.uk`
- (empty field)

## 🐛 Troubleshooting

### Local Development Issues

### Issue: Import Error - "No module named 'database'"

**Solution:**
```bash
# Make sure you're in the streamlit_assignment directory
cd streamlit_assignment

# Run from the correct location
streamlit run src/kavihealthcare.py
```

### Issue: Import Error - "No module named 'pandas'"

**Solution:**
```bash
# Activate virtual environment first
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Port Already in Use

**Solution:**
```bash
# Use a different port
streamlit run src/kavihealthcare.py --server.port 8502
```

### Issue: Database Locked

**Solution:**
- Close any other instances of the app
- Delete `patients.db` file (warning: loses all data)
- Restart the application

### Issue: Virtual Environment Not Activating (Windows PowerShell)

**Solution:**
```powershell
# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.venv\Scripts\Activate.ps1
```

---

### Docker Issues

### Issue: Port 8501 Already in Use

**Solution:**
```bash
# Find process using port 8501
lsof -i :8501  # macOS/Linux
netstat -ano | findstr :8501  # Windows

# Change port in docker-compose.yml
ports:
  - "8502:8501"  # Use port 8502 on host
```

### Issue: Container Unhealthy

**Solution:**
```bash
# Check logs for errors
docker-compose logs kavihealthcare

# Restart container
docker-compose restart

# Check health status
docker inspect --format='{{.State.Health}}' kavihealthcare-app
```

### Issue: Database Not Persisting

**Solution:**
```bash
# Verify volume is mounted
docker inspect kavihealthcare-app | grep Mounts -A 20

# Check data directory exists
ls -la data/

# Manually create if missing
mkdir -p data
chmod 755 data
```

### Issue: Docker Build Fails

**Solution:**
```bash
# Clean Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check Docker disk space
docker system df
```

### Issue: Permission Denied on data/ Directory

**Solution:**
```bash
# Fix permissions (Linux/macOS)
sudo chown -R $USER:$USER data/
chmod -R 755 data/

# Or run with proper user mapping
docker-compose down
docker-compose up -d
```

### Issue: Cannot Connect to Container

**Solution:**
```bash
# Check if container is running
docker ps

# Check network connectivity
docker exec kavihealthcare-app ping -c 1 localhost

# Check firewall settings
# Ensure port 8501 is not blocked
```

## � Docker Features

### Production-Ready Configuration

The Dockerfile includes several production best practices:

✅ **Security:**
- Runs as non-root user (UID 1000)
- Minimal base image (python:3.11-slim)
- No unnecessary packages installed

✅ **Performance:**
- Multi-stage builds possible
- Efficient layer caching
- No cache directories

✅ **Reliability:**
- Health checks configured
- Automatic restart policy
- Proper signal handling

✅ **Monitoring:**
- Built-in health endpoint
- Structured logging
- Resource limits configurable

### Docker Environment Variables

Configure in `docker-compose.yml` or pass to `docker run`:

```yaml
environment:
  - DB_PATH=/app/data/patients.db          # Database location
  - STREAMLIT_THEME_BASE=light             # Theme: light/dark
  - STREAMLIT_THEME_PRIMARY_COLOR=#FF4B4B  # Primary color
```

### Docker Volumes

```yaml
volumes:
  - ./data:/app/data              # Database persistence
  - ./src:/app/src                # Live code reload (dev only)
```

## �🔐 Security Considerations

⚠️ **Important**: This is a development application. For production use:

### Already Implemented in Docker:
- ✅ Non-root user execution
- ✅ Minimal attack surface (slim image)
- ✅ Health checks for monitoring
- ✅ Resource isolation

### Still Required for Production:
1. **Add Authentication**: Implement user login system
2. **Encrypt Database**: Use SQLCipher or similar
3. **HTTPS**: Configure reverse proxy (nginx/traefik) with SSL
4. **Access Control**: Role-based permissions
5. **Audit Logging**: Track all data modifications
6. **Backup Strategy**: Automated database backups
7. **HIPAA Compliance**: If handling real patient data
8. **Rate Limiting**: Prevent abuse
9. **Network Isolation**: Use Docker networks
10. **Secrets Management**: Use Docker secrets or vault

See `PRODUCTION.md` for detailed production deployment guide.

## 📈 Future Enhancements

Potential features to add:
- [ ] User authentication and authorization
- [ ] Appointment scheduling
- [ ] Medical history tracking
- [ ] Prescription management
- [ ] Multi-clinic support
- [ ] Advanced reporting and analytics
- [ ] Patient portal access
- [ ] SMS/Email notifications
- [ ] Data backup/restore functionality
- [ ] API endpoints for integration

## 🤝 Contributing

To contribute or modify:

1. **Add New Features**: Extend `kavihealthcare.py`
2. **Database Changes**: Modify `database/operations.py`
3. **Add Tests**: Update `tests/test_kavihealthcare.py`
4. **Run Tests**: Ensure all tests pass before committing

## 📄 License

This project is for educational purposes.

## 👤 Author

KaviHealthCare App Development Team

## 📞 Support

For issues or questions:
1. Check this README
2. Review `README_TESTS.md` for testing help
3. Check the troubleshooting section
4. Verify all dependencies are installed

---

## 📋 Quick Reference Commands

### Local Development
```bash
# Setup
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run Application
streamlit run src/kavihealthcare.py

# Run Tests
pytest tests/test_kavihealthcare.py -v

# Stop Application
# Press Ctrl+C in terminal

# Deactivate Virtual Environment
deactivate
```

### Docker Deployment
```bash
# Build & Start
docker-compose up -d

# View Logs
docker-compose logs -f

# Stop
docker-compose stop

# Restart
docker-compose restart

# Remove (keeps data)
docker-compose down

# Rebuild
docker-compose build --no-cache
docker-compose up -d

# Backup Database
cp data/patients.db backups/patients_$(date +%Y%m%d).db

# Enter Container
docker exec -it kavihealthcare-app sh

# Check Health
docker inspect --format='{{.State.Health.Status}}' kavihealthcare-app
```

## 📚 Additional Documentation

- **Testing Guide**: See `README_TESTS.md`
- **Production Deployment**: See `PRODUCTION.md`
- **Docker Configuration**: See `Dockerfile` and `docker-compose.yml`

## 🌐 Accessing the Application

| Method | URL | Use Case |
|--------|-----|----------|
| Local Dev | http://localhost:8501 | Development |
| Docker | http://localhost:8501 | Production |
| Custom Port | http://localhost:XXXX | When 8501 is busy |
| Network | http://YOUR_IP:8501 | Access from other devices |

**Happy Healthcare Managing! 🏥✨**

# Production Configuration for KaviHealthCare App

## Environment Variables

Create a `.env` file in the project root for production configuration:

```env
# Database Configuration
DB_PATH=/app/data/patients.db

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Theme Configuration (optional)
STREAMLIT_THEME_BASE=light
STREAMLIT_THEME_PRIMARY_COLOR=#FF4B4B
STREAMLIT_THEME_BACKGROUND_COLOR=#FFFFFF
STREAMLIT_THEME_SECONDARY_BACKGROUND_COLOR=#F0F2F6
STREAMLIT_THEME_TEXT_COLOR=#262730

# Security (add for production)
# STREAMLIT_SERVER_ENABLE_CORS=false
# STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=true
```

## Production Checklist

### Before Deployment

- [ ] Update `DB_PATH` in `src/database/connection.py` to use environment variable
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Set up backup schedule for database
- [ ] Implement authentication system
- [ ] Enable logging and monitoring
- [ ] Set resource limits (CPU, memory)
- [ ] Configure reverse proxy (nginx/traefik)
- [ ] Set up health monitoring
- [ ] Review and update security settings

### Security Hardening

1. **Database Security**
   - Use volume encryption for persistent data
   - Regular automated backups
   - Implement database access controls

2. **Network Security**
   - Use HTTPS only (configure reverse proxy)
   - Restrict container network access
   - Implement rate limiting

3. **Application Security**
   - Add user authentication
   - Implement role-based access control
   - Enable audit logging
   - Input sanitization (already implemented)

4. **Container Security**
   - Regularly update base image
   - Scan for vulnerabilities
   - Run as non-root user (already configured)
   - Limit container capabilities

### Monitoring & Logging

```yaml
# Add to docker-compose.yml for logging
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Backup Strategy

```bash
# Backup database
docker exec kavihealthcare-app cp /app/data/patients.db /app/data/backup_$(date +%Y%m%d_%H%M%S).db

# Or from host
cp data/patients.db backups/patients_$(date +%Y%m%d_%H%M%S).db
```

### Resource Limits

Add to docker-compose.yml:
```yaml
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 512M
        reservations:
          cpus: '0.5'
          memory: 256M
```

## Load Balancing (Multiple Instances)

For high availability, use Docker Swarm or Kubernetes with shared database volume.

## Health Monitoring

The Dockerfile includes a health check. Monitor with:
```bash
docker inspect --format='{{.State.Health.Status}}' kavihealthcare-app
```

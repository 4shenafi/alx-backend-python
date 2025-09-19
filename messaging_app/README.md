# Messaging App - Docker Setup

This Django messaging application is containerized using Docker and Docker Compose for easy deployment and development.

## Project Structure

```
messaging_app/
├── Dockerfile              # Docker configuration for the Django app
├── docker-compose.yml      # Multi-container setup with Django + MySQL
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in git)
├── .gitignore             # Git ignore rules
├── manage.py              # Django management script
├── messaging_app/         # Django project settings
│   ├── settings.py        # Updated for MySQL support
│   └── ...
└── chats/                 # Django app
    ├── models.py          # User, Conversation, Message models
    └── ...
```

## Features

- **Docker Containerization**: Python 3.10 base image with optimized layers
- **Multi-Container Setup**: Django web app + MySQL database
- **Environment Configuration**: Secure environment variable management
- **Data Persistence**: MySQL data persisted using Docker volumes
- **Production Ready**: Non-root user, proper security practices

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git (to clone the repository)

### Setup Instructions

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd messaging_app
   ```

2. **Create environment file**:
   ```bash
   cp .env.example .env
   # Edit .env with your preferred values
   ```

3. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

4. **Access the application**:
   - Django app: http://localhost:8000
   - MySQL database: localhost:3306

### Environment Variables

The `.env` file contains the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Configuration
MYSQL_DATABASE=messaging_db
MYSQL_USER=messaging_user
MYSQL_PASSWORD=messaging_password
MYSQL_ROOT_PASSWORD=root_password
DB_HOST=db
DB_PORT=3306
```

## Docker Commands

### Build and Run
```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Database Operations
```bash
# Run Django migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access MySQL shell
docker-compose exec db mysql -u messaging_user -p messaging_db
```

### Development
```bash
# Run Django shell
docker-compose exec web python manage.py shell

# Run tests
docker-compose exec web python manage.py test

# Collect static files
docker-compose exec web python manage.py collectstatic
```

## Database Configuration

The application automatically detects the environment:
- **Docker/Production**: Uses MySQL database with environment variables
- **Local Development**: Falls back to SQLite if no `DB_HOST` is set

## Data Persistence

MySQL data is persisted using Docker volumes:
- Volume name: `mysql_data`
- Data location: `/var/lib/mysql` in the container
- Survives container restarts and rebuilds

## Security Features

- Non-root user in Docker container
- Environment variables for sensitive data
- `.env` file excluded from git
- MySQL native password authentication
- Proper Django security settings

## API Endpoints

The messaging app provides REST API endpoints for:
- User authentication (JWT)
- User management
- Conversation management
- Message handling

See the Postman collection in `post_man-Collections/` for API documentation.

## Troubleshooting

### Common Issues

1. **Port conflicts**: Ensure ports 8000 and 3306 are available
2. **Permission issues**: Check Docker daemon is running
3. **Database connection**: Verify environment variables in `.env`
4. **Build failures**: Check Docker and Docker Compose versions

### Logs and Debugging

```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs web
docker-compose logs db

# Follow logs in real-time
docker-compose logs -f web
```

## Production Deployment

For production deployment:

1. Update environment variables in `.env`
2. Set `DEBUG=False`
3. Use a proper secret key
4. Configure proper `ALLOWED_HOSTS`
5. Use a reverse proxy (nginx) for static files
6. Set up SSL certificates
7. Use a managed database service if needed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker Compose
5. Submit a pull request

## License

This project is part of the ALX Backend Python curriculum.

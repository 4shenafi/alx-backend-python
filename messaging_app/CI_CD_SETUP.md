# CI/CD Pipeline Setup Guide

This document provides instructions for setting up the Continuous Integration and Continuous Deployment (CI/CD) pipeline for the Django Messaging Application.

## Overview

The CI/CD pipeline includes:
- **Jenkins**: Automated testing, Docker image building, and pushing to Docker Hub
- **GitHub Actions**: Testing, linting, code coverage, and Docker image deployment
- **Docker**: Containerization of the Django application

## Prerequisites

1. Docker and Docker Compose installed
2. Jenkins server access
3. GitHub repository with Actions enabled
4. Docker Hub account

## Jenkins Setup

### 1. Install Jenkins

Run Jenkins in a Docker container:

```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

### 2. Access Jenkins Dashboard

1. Open your browser and navigate to `http://localhost:8080`
2. Follow the setup wizard to configure Jenkins
3. Install the following plugins:
   - Git Plugin
   - Pipeline Plugin
   - ShiningPanda Plugin
   - Docker Pipeline Plugin

### 3. Configure Credentials

1. Go to **Manage Jenkins** → **Manage Credentials**
2. Add Docker Hub credentials:
   - Kind: Username with password
   - ID: `dockerhub-credentials`
   - Username: Your Docker Hub username
   - Password: Your Docker Hub password/token

### 4. Create Pipeline

1. Click **New Item** → **Pipeline**
2. Name: `messaging-app-pipeline`
3. In Pipeline section:
   - Definition: Pipeline script from SCM
   - SCM: Git
   - Repository URL: Your GitHub repository URL
   - Credentials: Add GitHub credentials if needed
   - Script Path: `messaging_app/Jenkinsfile`

## GitHub Actions Setup

### 1. Repository Secrets

Add the following secrets to your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add these repository secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password/token

### 2. Workflow Files

The following workflow files are already configured:

- `.github/workflows/ci.yml`: Runs tests, linting, and coverage on push/PR
- `.github/workflows/dep.yml`: Builds and pushes Docker images on main branch

## Testing

### Local Testing

Run tests locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html

# Run linting
flake8 .
```

### Pipeline Testing

1. **Jenkins**: Trigger the pipeline manually or on code changes
2. **GitHub Actions**: Automatically runs on push/PR to main/develop branches

## Docker Commands

### Build Image

```bash
docker build -t messaging-app .
```

### Run Container

```bash
docker run -p 8000:8000 messaging-app
```

### Push to Docker Hub

```bash
docker tag messaging-app your-username/messaging-app:latest
docker push your-username/messaging-app:latest
```

## Monitoring

### Jenkins

- View build logs in Jenkins dashboard
- Check test results and coverage reports
- Monitor Docker image build and push status

### GitHub Actions

- View workflow runs in **Actions** tab
- Download coverage reports as artifacts
- Check build status on pull requests

## Troubleshooting

### Common Issues

1. **MySQL Connection Issues**: Ensure MySQL service is running and accessible
2. **Docker Build Failures**: Check Dockerfile and dependencies
3. **Test Failures**: Verify test database configuration
4. **Permission Issues**: Check file permissions and Docker access

### Logs

- Jenkins: Check build console output
- GitHub Actions: View workflow logs
- Docker: Use `docker logs <container_name>`

## Security Notes

- Never commit sensitive credentials to version control
- Use environment variables and secrets management
- Regularly rotate API keys and passwords
- Enable branch protection rules on main branch

## Next Steps

1. Set up Kubernetes deployment
2. Add security scanning (Snyk, Trivy)
3. Implement rolling updates
4. Add monitoring and alerting
5. Set up staging environment

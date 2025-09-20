import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from collections import defaultdict
import threading

# Configure logging for requests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('requests.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Thread-safe storage for rate limiting
rate_limit_storage = defaultdict(list)
rate_limit_lock = threading.Lock()


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log user requests with timestamp, user, and path.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def __call__(self, request):
        # Log the request information
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware(MiddlewareMixin):
    """
    Middleware that restricts access to the messaging app during certain hours.
    Denies access outside 9PM and 6PM (21:00 to 06:00).
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def __call__(self, request):
        current_time = datetime.now().time()
        
        # Define restricted hours: 21:00 (9PM) to 06:00 (6AM)
        start_restriction = time(21, 0)  # 9PM
        end_restriction = time(6, 0)     # 6AM
        
        # Check if current time is within restricted hours
        if current_time >= start_restriction or current_time <= end_restriction:
            return HttpResponseForbidden("Access denied: Chat is only available between 6AM and 9PM")
        
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware(MiddlewareMixin):
    """
    Middleware that implements rate limiting for chat messages.
    Limits users to 5 messages per minute based on IP address.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def __call__(self, request):
        # Only apply rate limiting to POST requests (chat messages)
        if request.method == 'POST':
            client_ip = self.get_client_ip(request)
            current_time = datetime.now()
            
            with rate_limit_lock:
                # Clean old entries (older than 1 minute)
                rate_limit_storage[client_ip] = [
                    timestamp for timestamp in rate_limit_storage[client_ip]
                    if (current_time - timestamp).total_seconds() < 60
                ]
                
                # Check if user has exceeded the limit (5 messages per minute)
                if len(rate_limit_storage[client_ip]) >= 5:
                    return JsonResponse({
                        'error': 'Rate limit exceeded. Maximum 5 messages per minute allowed.'
                    }, status=429)
                
                # Add current request timestamp
                rate_limit_storage[client_ip].append(current_time)
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Get the client's IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolepermissionMiddleware(MiddlewareMixin):
    """
    Middleware that checks user roles and restricts access to admin/moderator only.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def __call__(self, request):
        # Check if user is authenticated and has admin or moderator role
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Check if user has admin or moderator role
            # Assuming the User model has a role field or is_staff/is_superuser
            if not (request.user.is_staff or request.user.is_superuser or 
                   (hasattr(request.user, 'role') and request.user.role in ['admin', 'moderator'])):
                return HttpResponseForbidden("Access denied: Admin or moderator role required")
        
        response = self.get_response(request)
        return response

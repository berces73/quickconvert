# Gunicorn configuration file
import multiprocessing

# Bind to all interfaces
bind = "0.0.0.0:8000"

# Worker configuration
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Logging
accesslog = "-"  # stdout
errorlog = "-"   # stderr
loglevel = "info"

# Process naming
proc_name = "nexus-convert"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (for production with certificates)
# keyfile = '/path/to/key.pem'
# certfile = '/path/to/cert.pem'

# Performance
preload_app = True
max_requests = 1000
max_requests_jitter = 100

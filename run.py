import uvicorn
import logging
import socket
import sys
from contextlib import closing

def verify_dependencies():
    """Verify required dependencies are installed"""
    dependencies = [
        ('dotenv', 'python-dotenv'),
        ('fastapi', 'fastapi'),
        ('sqlalchemy', 'sqlalchemy'),
        ('uvicorn', 'uvicorn'),
        ('psutil', 'psutil'),
        ('requests', 'requests')
    ]
    
    missing = []
    for module, package in dependencies:
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("Missing required dependencies:")
        for package in missing:
            print(f"  - {package}")
        print("\nPlease install required dependencies: pip install -r requirements.txt")
        return False
    return True

def check_port_available(host, port):
    """Check if a port is available and kill any existing processes"""
    import psutil
    import time
    
    # First try to kill any process using the port
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.connections():
                if hasattr(conn.laddr, 'port') and conn.laddr.port == port:
                    proc.kill()
                    proc.wait(timeout=5)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
            continue
    
    # Give system time to release the port
    time.sleep(1)
    
    # Now try to bind to port
    for _ in range(3):  # Try up to 3 times
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind((host, port))
                sock.close()
                return True
        except socket.error:
            time.sleep(1)  # Wait before retrying
    return False

def setup_database_directory():
    """Ensure database directory exists with proper permissions"""
    import os
    try:
        # Create necessary directories with full permissions
        os.makedirs('data', mode=0o777, exist_ok=True)
        
        # Set database path
        db_path = os.path.join('data', 'security.db')
        
        # Update environment variable with absolute path
        abs_db_path = os.path.abspath(db_path)
        os.environ['SQLALCHEMY_DATABASE_URL'] = f'sqlite:///{abs_db_path}'
        
        # Ensure parent directory is writable
        os.chmod('data', 0o777)
        return True
    except Exception as e:
        print(f"Error setting up database directory: {str(e)}")
        return False

def main():
    """Main application entry point"""
    import os
    from pathlib import Path

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

    try:
        # Load environment variables
        env_path = Path(__file__).parent / '.env'
        if env_path.exists():
            from dotenv import load_dotenv
            logger.info("Loading environment variables")
            load_dotenv(env_path, override=True)

        # Development environment setup
        os.environ.setdefault('ENVIRONMENT', 'development')
        os.environ.setdefault('HOST', '0.0.0.0')
        os.environ.setdefault('PORT', '8000')

        # Dependency check
        if not verify_dependencies():
            raise RuntimeError("Missing required dependencies")

        # Database directory setup
        if not setup_database_directory():
            raise RuntimeError("Failed to setup database directory")

        # Server configuration
        host = os.getenv('HOST', '0.0.0.0')
        port = int(os.getenv('PORT', '8000'))
        
        # First verify port is available
        if not check_port_available(host, port):
            raise RuntimeError(f"Port {port} is not available")

        logger.info(f"Starting FastAPI server at http://{host}:{port}")
        
        # Start server with basic configuration
        logger.info("Starting FastAPI application...")
        uvicorn.run(
            "system.main:app",
            host=host,
            port=port,
            reload=False,  # Disable reload to avoid duplicate processes
            workers=1,
            access_log=True,
            log_level="info"
        )

    except Exception as e:
        logger.error(f"Server startup failed: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)
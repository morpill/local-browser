import sys
import config

def get_url() -> bool:
    return sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else None

def proxy_only() -> bool:
    return sys.argv[1].lower() == '--proxy' if len(sys.argv) > 1 else None

def should_cache():
    config.config['CACHING'] = not '--no-cache' in sys.argv

def start_example() -> bool:
    return sys.argv[1].lower() == '--run-example' if len(sys.argv) > 1 else None 
    
should_cache()
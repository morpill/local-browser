from core.proxy import start as start_proxy
from cli.tools import proxy_only, get_url, start_example
import webview as wv
import sys
from requests.exceptions import ConnectionError
import subprocess

def display(proxy_url: str):
    if proxy_url:
        window = wv.create_window('Preview', url=proxy_url)
        wv.start()
    
def process(address: str):
    if address.lower().strip() == '/exit':
        sys.exit(0)
    if address.lower().strip() == '/run-proxy':
        start_proxy()
        return None
    identifier, path = address.split('/', 1)
    return f'http://{identifier}.localhost:5000/{path}'

def browser(): 
    
    if start_example():
        try:
            subprocess.run(['python', '-m', 'http.server', '-d', './MyApp', '7777'])
        except KeyboardInterrupt:
            sys.exit(0)
        finally:
            sys.exit(0)
    
    start_proxy()
    
      
    if not proxy_only():
       
        argv_url = get_url()
        
        if argv_url:
            display(process(argv_url))
            sys.exit(0)
        
        while True:
            try:
                address = str(input('Enter address: '))
                display(process(address))
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(e)
                
    else:
        try:
            input('Press [ENTER] or [CMD]+[C] to kill the proxy. ')
            
        except ConnectionError:
            print('We could not connect to the target.')
        
        except KeyboardInterrupt:
            pass

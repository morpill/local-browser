from api.build_app import App

MyApp = App('MyApp', 'moritzpillmann')
MyApp.manifest['settings'] = {
    'CACHE': False
}
MyApp._save_manifest()
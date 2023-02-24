from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'
    def ready(self):
        # importowanie procedur do obsługi sygnałów
        import images.signals

#!/usr/bin/env python
import os
import sys

def main():
    """Run the Tereza RAG chat interface."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tereza_online.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Executa o comando run_tereza diretamente
    print("Iniciando interface de chat da Tereza...")
    sys.argv = ['manage.py', 'run_tereza']
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

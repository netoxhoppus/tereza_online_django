
from django.core.management.base import BaseCommand
from core.services.rag_service import TerezaAgent
import uuid

class Command(BaseCommand):
    help = 'Interage com a Tereza Bicuda pelo terminal'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Iniciando sessão com Tereza Bicuda...'))
        self.stdout.write(self.style.WARNING('Digite "sair" para encerrar.'))
        
        agent = TerezaAgent()
        session_id = str(uuid.uuid4())
        
        self.stdout.write(self.style.MIGRATE_HEADING(f'Sessão ID: {session_id}'))
        
        while True:
            try:
                user_input = input("\nVocê: ")
                if user_input.lower() in ['sair', 'exit', 'quit']:
                    self.stdout.write(self.style.SUCCESS('Tereza virou as costas e sumiu na neblina...'))
                    break
                
                if not user_input.strip():
                    continue
                    
                self.stdout.write("Tereza está pensando... (consultando o além)")
                response = agent.process_message(session_id, user_input)
                
                self.stdout.write(self.style.ERROR(f"\nTereza: {response}"))
                
            except KeyboardInterrupt:
                self.stdout.write(self.style.SUCCESS('\nEncerrando à força...'))
                break
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro: {e}'))

from django.apps import AppConfig

class FuelV2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'modules.fuelv2'
    verbose_name = 'Gestão de Abastecimento em Lote (V2)'

    def ready(self):
        """
        Este método é executado uma única vez quando o Django inicializa.
        É o local correto para importar os subscribers e registrar os receptores de eventos.
        """
        try:          
            print("✅ [FuelV2] Subscribers de eventos carregados com sucesso.")
        except ImportError as e:
            # Log de erro preventivo para debug de inicialização
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"❌ [FuelV2] Erro ao carregar subscribers: {e}")

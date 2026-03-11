import logging
from django.utils import timezone
from shared.events.django_dispatcher import receiver

logger = logging.getLogger(__name__)

# ==============================================================================
# 1. SUBSCRIBERS DE CRIAÇÃO (LOG & NOTIFICAÇÃO DE GESTÃO)
# ==============================================================================

@receiver("fuel.bulk_request_created_2")
def handle_bulk_created(bulk_id=None, requester_id=None, total_items=None, **kwargs):
    """
    Acionado quando um novo lote é criado.
    Ação: Logar criação e notificar gestores para aprovação.
    """
    # LOG DE SISTEMA (Para Debug/Monitoramento)
    logger.info(f"[BULK_V2] Novo lote #{bulk_id} criado por User {requester_id} com {total_items} viaturas.")


# ==============================================================================
# 2. SUBSCRIBERS DE PROCESSAMENTO (REQUISITO 4)
# ==============================================================================

@receiver("fuel.item_approve_2")
def handle_item_approved(item_id=None, bulk_id=None, **kwargs):
    """Notifica o motorista/requerente que uma viatura específica foi aprovada."""
    logger.info(f"[BULK_V2] Item {item_id} do lote {bulk_id} APROVADO.")
    # NotificationService.send_to_user(kwargs.get('requester_id'), f"Viatura no lote {bulk_id} aprovada!")


@receiver("fuel.item_reject_2")
def handle_item_rejected(item_id=None, reason='Sem motivo especificado', **kwargs):
    """Log de segurança para rejeições e notificação de erro."""
    logger.warning(f"[BULK_V2] Item {item_id} REJEITADO. Motivo: {reason}")


@receiver("fuel.item_fueled_2")
def handle_item_fueled(item_id=None, **kwargs):
    """
    Acionado quando o frentista confirma o abastecimento.
    Ação: Pode disparar a baixa de stock ou integração com financeiro.
    """
    logger.info(f"[BULK_V2] Abastecimento concluído para o Item {item_id}.")


# ==============================================================================
# 3. SUBSCRIBERS DE ESTADO GLOBAL (SINCRONISMO)
# ==============================================================================

@receiver("fuel.bulk_status_changed_2")
def handle_bulk_status_sync(bulk_id=None, new_bulk_status=None, **kwargs):
    """
    Acionado quando o sync_status da Entidade muda o estado do Pai.
    Útil para fechar processos financeiros do lote inteiro.
    """
    if new_bulk_status == "PROCESSED":
        logger.info(f"[BULK_V2] Lote #{bulk_id} foi totalmente processado e arquivado.")
    
    elif new_bulk_status == "CANCELLED":
        logger.error(f"[BULK_V2] Lote #{bulk_id} foi cancelado integralmente.")


# ==============================================================================
# 4. TRATAMENTO DE ERROS / EXCEÇÕES (AUDITORIA)
# ==============================================================================

@receiver("fuel.bulk_conflict_error_2")
def handle_concurrency_conflict(bulk_id=None, admin_id=None, **kwargs):
    """Loga tentativas de alteração simultânea (Optimistic Locking falhou)."""
    logger.error(f"[CONCURRENCY] Conflito de versão no lote {bulk_id} pelo Admin {admin_id}.")

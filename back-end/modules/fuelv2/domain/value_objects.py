from enum import Enum

class BulkStatus(Enum):
    PENDING = "PENDING"     # Acabou de ser criado
    PROCESSED = "PROCESSED" # Teve pelo menos um item aprovado/rejeitado/abastecido
    CANCELLED = "CANCELLED" # Lote foi cancelado (pelo admin ou auto)
    COMPLETED = "COMPLETED" # Todos os itens foram finalizados ou abastecidos

class BulkItemStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    FUELED = "FUELED"       # O item foi fisicamente abastecido

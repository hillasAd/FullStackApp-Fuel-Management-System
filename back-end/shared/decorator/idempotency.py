from rest_framework.response import Response
from ..models import IdempotencyKey
import functools

def clean_idempotency(view_func):
    @functools.wraps(view_func)
    def _wrapped_view(view_instance, request, *args, **kwargs):
        key = request.headers.get("X-Idempotency-Key")
        if not key:
            return view_func(view_instance, request, *args, **kwargs)

        # 🔎 1. Se já existe na DB, devolve o resultado anterior (O teu código!)
        existing = IdempotencyKey.objects.filter(key=key).first()
        if existing:
            print(f"Server: Idempotência via DB ativa para chave {key}")
            return Response(existing.response_body, status=existing.status_code)

        # 2. Executa a lógica real (UseCase, etc.)
        response = view_func(view_instance, request, *args, **kwargs)

        # 3. Se for sucesso (201), gravamos na tabela para a próxima vez
        if response.status_code == 201:
            IdempotencyKey.objects.create(
                key=key,
                user_id=request.user.id if request.user.is_authenticated else None,
                response_body=response.data,
                status_code=response.status_code
            )
        
        return response
    return _wrapped_view

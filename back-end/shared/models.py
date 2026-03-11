from django.db import models

class IdempotencyKey(models.Model):
    key = models.CharField(max_length=255, unique=True)
    user_id = models.IntegerField(null=True, blank=True)
    response_body = models.JSONField()
    status_code = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shared_idempotency_keys'
        indexes = [models.Index(fields=["key", "created_at"])]

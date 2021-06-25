from django.db import models
from tenant_schemas.models import TenantMixin

# Create your models here.

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True

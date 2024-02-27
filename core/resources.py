from import_export import resources
from .models import Property

class PropertyResource(resources.ModelResource):
    class Meta:
        model = Property
    
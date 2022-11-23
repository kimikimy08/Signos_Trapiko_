

from import_export import resources
from .models import IncidentGeneral, IncidentRemark, IncidentPerson,IncidentVehicle

        
class IncidentGeneraltResource(resources.ModelResource):
    class Meta:
        model = IncidentGeneral
    
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        for field_name in self.fields:
            col_name = self.fields[field_name].column_name
            if col_name not in dataset.headers:
                raise ValueError(f"'{col_name}' field not in data file")
        
class IncidentRemarkResources(resources.ModelResource):
    class Meta:
        model = IncidentRemark
    
    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        for field_name in self.fields:
            col_name = self.fields[field_name].column_name
            if col_name not in dataset.headers:
                raise ValueError(f"'{col_name}' field not in data file")
        
class IncidentPeopleResources(resources.ModelResource):
    class Meta:
        model = IncidentPerson

class IncidentVehicleResources(resources.ModelResource):
    class Meta:
        model = IncidentVehicle
from django.db import migrations

# Function to create default roles
def create_default_roles(apps, schema_editor):
    Role = apps.get_model('core_app', 'Role')
    
    # List of default roles and their descriptions
    roles = [
        ("Clinical Hypnotherapist", "Provides clinical hypnotherapy services"),
        ("Client Care Coordinator", "Coordinates client care"),
        ("NLP Practitioner", "Practices Neuro-Linguistic Programming"),
        ("Health and Wellness Coach", "Helps clients achieve health and wellness goals"),
    ]
    
    # Create the roles if they don't already exist
    for role_name, description in roles:
        Role.objects.get_or_create(name=role_name, description=description)
        
# Function to create default service types
def create_default_service_types(apps, schema_editor):
    ServiceType = apps.get_model('core_app', 'ServiceType')
    
    # List of default service types and their descriptions
    service_types = [
        ("Smoking Cessation", "Helps clients quit smoking"),
        ("Weight Loss", "Assists clients in losing weight"),
        ("Anxiety Management", "Provides strategies for managing anxiety"),
    ]
    
    # Create the service types if they don't already exist
    for service_name, description in service_types:
        ServiceType.objects.get_or_create(name=service_name, description=description)

class Migration(migrations.Migration):
    dependencies = [
        # Specify the dependencies for this migration if any
        ('core_app', '0003_role_servicetype_booking_customuser_roles'),  # Replace 'yourapp' with your actual app name
    ]

    # Operation to run the function that creates default roles
    operations = [
        migrations.RunPython(create_default_roles),
        migrations.RunPython(create_default_service_types)
    ]

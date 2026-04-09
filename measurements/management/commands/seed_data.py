import random
from django.core.management.base import BaseCommand
from variables.models import Project
from measurements.models import CostRecord

SERVICES = ['Amazon EC2', 'Amazon S3', 'Amazon RDS', 'AWS Lambda', 'Amazon CloudFront',
            'Amazon DynamoDB', 'Amazon ECS', 'Amazon SQS', 'Amazon Redshift']
REGIONS = ['us-east-1', 'us-west-2', 'eu-west-1', 'sa-east-1']
COMPANIES = ['Acme Corp', 'GlobalBank', 'MediHealth', 'RetailMax', 'EduTech']
PROJECT_NAMES = ['Web App', 'Mobile API', 'Data Pipeline', 'Auth Service', 'Analytics']

class Command(BaseCommand):
    help = 'Genera datos de prueba'

    def add_arguments(self, parser):
        parser.add_argument('--records', type=int, default=10000)

    def handle(self, *args, **options):
        n = options['records']

        self.stdout.write('Limpiando datos...')
        CostRecord.objects.all().delete()
        Project.objects.all().delete()

        projects = []
        for company in COMPANIES:
            for pname in random.sample(PROJECT_NAMES, 3):
                p = Project.objects.create(name=pname, company=company)
                projects.append(p)
                self.stdout.write('  {} - {}'.format(company, pname))

        self.stdout.write('Generando {} registros...'.format(n))
        records = []
        for i in range(n):
            records.append(CostRecord(
                project=random.choice(projects),
                service=random.choice(SERVICES),
                amount=round(random.uniform(0.5, 50.0), 2),
                region=random.choice(REGIONS),
            ))
            if len(records) >= 5000:
                CostRecord.objects.bulk_create(records)
                records = []

        if records:
            CostRecord.objects.bulk_create(records)

        self.stdout.write(self.style.SUCCESS(
            'Listo: {} proyectos, {} registros'.format(
                Project.objects.count(), CostRecord.objects.count())))

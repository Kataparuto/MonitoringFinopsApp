import json
import time
from django.conf import settings
from django.core.cache import cache
from django.db.models import Sum, Count
from ..models import CostRecord

def get_measurements():
    queryset = CostRecord.objects.all().order_by('-dateTime')[:10]
    return queryset

def create_measurement(form):
    measurement = form.save()
    measurement.save()
    return ()

def get_cost_report(company_name):
    """Reporte de costos por servicio. Usa cache si esta disponible."""
    cache_key = 'report:{}'.format(company_name)

    if settings.CACHE_ENABLED:
        cached = cache.get(cache_key)
        if cached:
            result = json.loads(cached)
            result['cache_hit'] = True
            return result

    start = time.time()

    by_service = list(
        CostRecord.objects.filter(project__company=company_name)
        .values('service')
        .annotate(total=Sum('amount'), count=Count('id'))
        .order_by('-total')
    )

    total = CostRecord.objects.filter(
        project__company=company_name
    ).aggregate(total=Sum('amount'), count=Count('id'))

    elapsed = (time.time() - start) * 1000

    result = {
        'company': company_name,
        'total_cost': float(total['total'] or 0),
        'total_records': total['count'] or 0,
        'by_service': by_service,
        'query_time_ms': round(elapsed, 2),
        'cache_hit': False,
    }

    if settings.CACHE_ENABLED:
        cache.set(cache_key, json.dumps(result), timeout=300)

    return result

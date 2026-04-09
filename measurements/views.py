import json
import socket
import time
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import MeasurementForm
from .logic import get_measurements, create_measurement, get_cost_report

# --- Vistas HTML (como el curso) ---

def measurement_list(request):
    measurements = get_measurements()
    context = {
        'measurement_list': measurements
    }
    return render(request, 'Measurement/measurements.html', context)

def measurement_create(request):
    if request.method == 'POST':
        form = MeasurementForm(request.POST)
        if form.is_valid():
            create_measurement(form)
            messages.add_message(request, messages.SUCCESS, 'Cost record created')
            return HttpResponseRedirect(reverse('measurementCreate'))
        else:
            print(form.errors)
    else:
        form = MeasurementForm()

    context = {
        'form': form,
    }
    return render(request, 'Measurement/measurementCreate.html', context)

# --- API endpoints (para JMeter) ---

def health_check(request):
    """GET /api/health/ - Health check para el Load Balancer"""
    return JsonResponse({
        'status': 'healthy',
        'hostname': socket.gethostname(),
    })

def api_report(request):
    """
    GET /api/reports/?company=Acme Corp

    ASR1 - Latencia: debe responder en menos de 100ms
    Tactica: caching con Redis
    """
    company = request.GET.get('company', 'Acme Corp')
    result = get_cost_report(company)
    result['hostname'] = socket.gethostname()
    return JsonResponse(result)

@csrf_exempt
def api_create(request):
    """
    POST /api/costs/

    ASR2 - Escalabilidad: soportar carga concurrente
    Endpoint para pruebas de escritura con JMeter
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Use POST'}, status=405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    from variables.models import Project
    try:
        project = Project.objects.get(id=body.get('project_id', 1))
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)

    from .models import CostRecord
    record = CostRecord.objects.create(
        project=project,
        service=body.get('service', 'Amazon EC2'),
        amount=body.get('amount', 10.0),
        region=body.get('region', 'us-east-1'),
    )

    return JsonResponse({
        'id': record.id,
        'service': record.service,
        'amount': record.amount,
        'hostname': socket.gethostname(),
    }, status=201)

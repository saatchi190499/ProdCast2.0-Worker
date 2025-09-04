from celery import shared_task
from .models import ScenarioClass, ScenarioLog
import time
from django.utils import timezone

server_name = "Server 1"

@shared_task(name="worker.run_scenario", bind=True)
def run_scenario(self, scenario_id: int, start_date: str, end_date: str):
    # self здесь нужен только если bind=True (для update_state)
    scenario = ScenarioClass.objects.get(scenario_id=scenario_id)
    scenario.status = "STARTED"
    scenario.server.server_name = self.request.hostname
    scenario.start_date = timezone.now()
    scenario.save()

    ScenarioLog.objects.create(
        scenario=scenario,
        message="Task started",
        progress=0
    )

    for i in range(0, 101, 10):
        # Симуляция прогресса
        time.sleep(5)
        ScenarioLog.objects.create(
            scenario=scenario,
            timestamp=timezone.now(),
            message=f"Progress: {i}%",
            progress=i
        )
        self.update_state(state="STARTED", meta={"progress": i})

    scenario.status = "SUCCESS"
    scenario.end_date = timezone.now()
    scenario.description = f"Calculated from {start_date} to {end_date}"
    scenario.save()

    ScenarioLog.objects.create(
        scenario=scenario,
        timestamp=timezone.now(),
        message="Task finished",
        progress=100
    )

    return {"status": "SUCCESS", "scenario_id": scenario_id}

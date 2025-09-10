import datetime, logging, os, random
import azure.functions as func
from azure.digitaltwins.core import DigitalTwinsClient
from azure.identity import DefaultAzureCredential

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().isoformat()
    logging.info(f"Timer executed at {utc_timestamp}")

    # Simulación de datos
    temperature = round(random.uniform(18, 35), 2)
    humidity = round(random.uniform(30, 80), 2)
    voltage = round(random.uniform(210, 230), 2)
    power = round(random.uniform(1000, 5000), 2)

    # Conexión a ADT
    adt_url = os.environ["ADT_SERVICE_URL"]
    cred = DefaultAzureCredential()
    client = DigitalTwinsClient(adt_url, cred)

    # Actualizar twin
    twin_id = "DataCenter1"
    patch = [
        {"op": "replace", "path": "/temperature", "value": temperature},
        {"op": "replace", "path": "/humidity", "value": humidity},
        {"op": "replace", "path": "/voltage", "value": voltage},
        {"op": "replace", "path": "/powerConsumption", "value": power}
    ]
    client.update_digital_twin(twin_id, patch)

    logging.info(
        f"Updated {twin_id} with T={temperature}, H={humidity}, V={voltage}, P={power}"
    )

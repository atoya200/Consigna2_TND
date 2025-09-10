import logging, os
import azure.functions as func
from azure.digitaltwins.core import DigitalTwinsClient
from azure.identity import DefaultAzureCredential

def main(checktimer: func.TimerRequest) -> None:
    logging.info("Executing control_devices function...")

    # Conexión a ADT
    adt_url = os.environ["ADT_SERVICE_URL"]
    cred = DefaultAzureCredential()
    client = DigitalTwinsClient(adt_url, cred)

    twin_id = "DataCenter1"

    # Leer estado actual
    twin = client.get_digital_twin(twin_id)
    temperature = twin.get("temperature")
    humidity = twin.get("humidity")

    logging.info(f"Current state: T={temperature}, H={humidity}")

    patch = []

    # Lógica de control
    if temperature is not None:
        patch.append({
            "op": "replace",
            "path": "/airConditioner",
            "value": temperature > 23
        })

    if humidity is not None:
        patch.append({
            "op": "replace",
            "path": "/dehumidifier",
            "value": humidity > 65
        })

    if patch:
        client.update_digital_twin(twin_id, patch)
        logging.info(f"Applied patch to {twin_id}: {patch}")
    else:
        logging.info("No updates needed.")

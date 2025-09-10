import datetime, logging, os, random
import azure.functions as func
from azure.digitaltwins.core import DigitalTwinsClient
from azure.identity import DefaultAzureCredential


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().isoformat()
    if getattr(mytimer, "past_due", False):
        logging.warning("El trigger del temporizador está retrasado.")
    logging.info(f"Timer executed at {utc_timestamp}")

    # Simulación de datos
    temperature = round(random.uniform(18, 35), 2)
    humidity = round(random.uniform(30, 80), 2)
    voltage = round(random.uniform(210, 230), 2)
    power = round(random.uniform(1000, 5000), 2)

    # Conexión a ADT
    adt_url = os.getenv("ADT_SERVICE_URL")
    if not adt_url:
        logging.error("ADT_SERVICE_URL no está establecido en las variables de entorno. Abortando actualización de ADT.")
        return

    twin_id = os.getenv("ADT_TWIN_ID", "DataCenter1")

    try:
        cred = DefaultAzureCredential()
        client = DigitalTwinsClient(adt_url, cred)

        # Actualizar twin
        patch = [
            {"op": "replace", "path": "/temperature", "value": temperature},
            {"op": "replace", "path": "/humidity", "value": humidity},
            {"op": "replace", "path": "/voltage", "value": voltage},
            {"op": "replace", "path": "/powerConsumption", "value": power},
        ]
        client.update_digital_twin(twin_id, patch)

        logging.info(
            f"Updated {twin_id} with T={temperature}, H={humidity}, V={voltage}, P={power}"
        )
    except Exception as e:
        logging.exception(f"Error actualizando el twin '{twin_id}' en ADT: {e}")

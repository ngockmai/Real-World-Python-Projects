import requests
from requests.auth import HTTPBasicAuth
import logging
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction, DatabaseError

# *** USER ACTION REQUIRED ***
# 1. Import your actual model(s) from devices.models
# Example: from devices.models import Device
# 2. Replace \'Device\' with your actual model name below
MODEL_NAME = \'Device\'
# 3. Define the mapping from API JSON keys to your Django model fields
# Example: API returns {\'serial\': \'123\', \'deviceName\': \'Cam1\', \'ip\': \'1.1.1.1\'}
#          Your model has fields: serial_number, name, ip_address
API_TO_MODEL_MAPPING = {
    \'serial\': \'serial_number\',
    \'deviceName\': \'name\',
    \'ip\': \'ip_address\',
    # Add other field mappings here
}
# 4. Specify the API field used to uniquely identify a device for updates/creation
UNIQUE_API_FIELD = \'serial\'
# ***************************

# Get the logger for the \'devices\' app (configured in settings.py)
logger = logging.getLogger(\'devices\')

class Command(BaseCommand):
    help = \'Fetches data from GVE API and syncs it to the local database.\'

    def handle(self, *args, **options):
        api_url = getattr(settings, \'GVE_API_URL\', None)
        api_username = getattr(settings, \'API_USERNAME\', None)
        api_password = getattr(settings, \'API_PASSWORD\', None)

        if not all([api_url, api_username, api_password]):
            logger.error("API URL or credentials not configured in settings.")
            self.stdout.write(self.style.ERROR("API URL or credentials not configured."))
            return

        try:
            self.stdout.write(f"Attempting to sync data from {api_url}...")
            response = requests.get(
                api_url,
                auth=HTTPBasicAuth(api_username, api_password),
                verify=False  # Consider setting verify=True with proper certificate handling in production
            )
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            api_data = response.json()
            logger.info(f"Successfully fetched data from API. Records received: {len(api_data)}")

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}", exc_info=True)
            self.stdout.write(self.style.ERROR(f"API request failed: {e}"))
            return
        except ValueError as e: # Includes JSONDecodeError
             logger.error(f"Failed to decode API response JSON: {e}", exc_info=True)
             self.stdout.write(self.style.ERROR(f"Failed to decode API response: {e}"))
             return

        if not isinstance(api_data, list):
             logger.error(f"API response was not a list as expected. Type: {type(api_data)}")
             self.stdout.write(self.style.ERROR("API response format unexpected (expected a list)."))
             return

        # Dynamically get the model class based on MODEL_NAME
        try:
            # Assuming models are in the \'devices\' app
            from devices.models import Device # Replace with your actual model import
            model_class = Device # Replace with your actual model class
            # Or dynamically:
            # from django.apps import apps
            # model_class = apps.get_model(\'devices\', MODEL_NAME)
        except (ImportError, LookupError):
            logger.error(f"Could not find model \'{MODEL_NAME}\' in app \'devices\'.")
            self.stdout.write(self.style.ERROR(f"Model \'{MODEL_NAME}\' not found."))
            return

        synced_count = 0
        updated_count = 0
        failed_count = 0

        try:
            with transaction.atomic(): # Process all updates/creates in one transaction
                for item in api_data:
                    if not isinstance(item, dict):
                        logger.warning(f"Skipping non-dictionary item in API data: {item}")
                        failed_count += 1
                        continue

                    unique_value = item.get(UNIQUE_API_FIELD)
                    if unique_value is None:
                         logger.warning(f"Skipping item due to missing unique identifier (\'{UNIQUE_API_FIELD}\'): {item}")
                         failed_count += 1
                         continue

                    defaults = {}
                    for api_key, model_field in API_TO_MODEL_MAPPING.items():
                        if api_key in item:
                            defaults[model_field] = item[api_key]
                        else:
                             logger.warning(f"API key \'{api_key}\' not found in item: {item}")

                    if not defaults:
                        logger.warning(f"No valid fields to update/create for item with unique value \'{unique_value}\'. Skipping.")
                        failed_count += 1
                        continue

                    try:
                        # Prepare lookup kwargs dynamically { \'model_field_for_unique_api_field\': unique_value }
                        lookup_kwargs = {API_TO_MODEL_MAPPING[UNIQUE_API_FIELD]: unique_value}

                        obj, created = model_class.objects.update_or_create(
                            defaults=defaults,
                            **lookup_kwargs
                        )
                        if created:
                            synced_count += 1
                        else:
                            updated_count += 1
                    except Exception as e:
                        logger.error(f"Failed to update/create DB record for item {unique_value}: {e}", exc_info=True)
                        failed_count += 1
                        # Continue processing other items even if one fails within the transaction

        except DatabaseError as e:
             logger.error(f"Database transaction failed: {e}", exc_info=True)
             self.stdout.write(self.style.ERROR(f"Database transaction failed: {e}"))
             return # Exit if the whole transaction fails
        except Exception as e: # Catch any other unexpected errors during processing
             logger.error(f"An unexpected error occurred during database sync: {e}", exc_info=True)
             self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
             return

        summary = f"Sync complete. Created: {synced_count}, Updated: {updated_count}, Failed/Skipped: {failed_count}."
        logger.info(summary)
        self.stdout.write(self.style.SUCCESS(summary)) 
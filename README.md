# quiz_master_v2
This is a project that includes making of a quiz app
## Running Celery Worker (Windows)

Because of multiprocessing issues on Windows, run Celery like this:

```bash
celery -A celery_utils.celery worker --loglevel=info --pool=solo

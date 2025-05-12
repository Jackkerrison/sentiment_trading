# redis:   redis-server

worker:  celery -A src.tasks worker --loglevel=info --pool=solo
beat:    celery -A src.tasks beat   --loglevel=info
api:     uvicorn src.api:app --reload --host=127.0.0.1 --port=8000
ui:      streamlit run ui/app.py

from app.tasks.crawl_tasks import celery_app
from app.tasks.ranking_tasks import daily_ranking_generation_task  # ensure it's imported for worker

if __name__ == "__main__":
    celery_app.start()

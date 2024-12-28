import json
import logging
from confluent_kafka import Consumer
from utils.helpers import load_config, send_email

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    config = load_config('config/config.json')

    conf_consumer = {
        'bootstrap.servers': config['kafka']['bootstrap_servers'],
        'group.id': config['kafka']['group_ids']['distributor'],
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(**conf_consumer)
    kafka_summarized_news_articles=config['kafka_summarized_news_articles']
    consumer.subscribe([kafka_summarized_news_articles])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                logger.error(f"Consumer error: {msg.error()}")
                continue

            summary = json.loads(msg.value().decode('utf-8'))
            email_body = f"Title: {summary['title']}\nSummary: {summary['summary']}\nRead more: {summary['url']}"
            for subscriber in config['subscribers']:
                send_email(config['smtp'], subscriber, "Daily News Summary", email_body)
                logger.info(f"Sent summary to {subscriber}")
    except Exception as e:
        logger.error(f"Error in distributor: {e}")

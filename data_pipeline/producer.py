import json
import logging
import requests
from confluent_kafka import Producer
from utils.helpers import load_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_news(api_key):
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['articles']


def produce_messages(producer, topic, messages):
    for message in messages:
        producer.produce(topic, key=message['title'], value=json.dumps(message))
    producer.flush()


if __name__ == "__main__":
    config = load_config('config/config.json')
    producer_conf = {'bootstrap.servers': config['kafka']['bootstrap_servers']}
    producer = Producer(**producer_conf)
    kafka_news_articles=config['kafka_news_articles']

    try:
        articles = fetch_news(config['newsapi_key'])
        logger.info(f"Fetched {len(articles)} articles")
        produce_messages(producer, kafka_news_articles, articles)
        logger.info(f"Successfully produced messages to topic : {kafka_news_articles}")
    except Exception as e:
        logger.error(f"Error in producer: {e}")

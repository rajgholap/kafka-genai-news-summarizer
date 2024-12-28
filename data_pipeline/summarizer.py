import json
import logging
import os
from confluent_kafka import Consumer, Producer
from generative_ai.summarization import get_summarizer, summarize_texts
from utils.helpers import load_config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

if __name__ == "__main__":
    config = load_config('config/config.json')
    os.environ['HF_API_TOKEN'] = config['huggingface_api_token']

    conf_consumer = {
        'bootstrap.servers': config['kafka']['bootstrap_servers'],
        'group.id': config['kafka']['group_ids']['summarizer'],
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(**conf_consumer)
    kafka_news_articles=config['kafka_news_articles']
    consumer.subscribe([kafka_news_articles])

    conf_producer = {'bootstrap.servers': config['kafka']['bootstrap_servers']}
    producer = Producer(**conf_producer)
    kafka_summarized_news_articles=config['kafka_summarized_news_articles']

    summarizer = get_summarizer()

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                logger.error(f"Consumer error: {msg.error()}")
                continue

            article = json.loads(msg.value().decode('utf-8'))
            content = article.get('content', '')
            if not content:
                logger.warning(f"Skipping empty article content: {article['title']}")
                continue

            summary = summarize_texts(summarizer, [content])[0]
            summary_data = {"title": article['title'], "summary": summary, "url": article['url']}
            producer.produce(kafka_summarized_news_articles, key=article['title'], value=json.dumps(summary_data))
            producer.flush()
            logger.info(f"Produced summary for article: {article['title']}")
    except Exception as e:
        logger.error(f"Error in summarizer: {e}")

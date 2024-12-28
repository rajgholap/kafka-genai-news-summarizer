# Kafka and Generative AI News Summarization Project

## Overview
This project fetches news articles, summarizes them using a generative AI model, and distributes the summaries via email to a list of subscribers. It utilizes Kafka for message queuing and transformers from Hugging Face for summarization.

## Project Structure

├── config │ 
└── config.json 
├── kafka │ 
├── producer.py │ 
├── summarizer.py │ 
└── distributor.py 
├── logs │ 
└── .gitkeep 
├── utils │ 
└── helpers.py 
├── requirements.txt 
└── README.md
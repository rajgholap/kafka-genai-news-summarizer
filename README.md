# Kafka and Generative AI News Summarization Project

## Overview
This project fetches news articles, summarizes them using a generative AI model, and distributes the summaries via email to a list of subscribers. It utilizes Kafka for message queuing and transformers from Hugging Face for summarization.

## Project Structure

Project Structure
├── config
│   └── config.json           # Configuration file containing API keys, Kafka, and SMTP settings
├── kafka
│   ├── producer.py           # Fetches news articles and publishes them to Kafka
│   ├── summarizer.py         # Summarizes articles and republishes to Kafka
│   └── distributor.py        # Distributes summarized articles via email
├── logs
│   └── .gitkeep              # Placeholder for log files
├── utils
│   └── helpers.py            # Utility functions for configuration loading and email sending
├── requirements.txt          # Python dependencies for the project
└── README.md                 # Project documentation

from transformers import pipeline


def get_summarizer(model_name="facebook/bart-large-cnn"):
    return pipeline("summarization", model=model_name)


def summarize_texts(summarizer, texts):
    return [summarizer(text, max_length=150, min_length=40, do_sample=False)[0]['summary_text'] for text in texts]

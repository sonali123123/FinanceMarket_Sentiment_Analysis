def aggregate_sentiments(sentiments: list) -> dict:
    """
    Aggregates sentiment results from multiple news items to produce an overall sentiment.
    
    This function counts the frequency of each label and computes the total confidence for each.
    If one label appears most frequently, that label is returned along with its average confidence.
    In case of a tie, the label with the highest total confidence is chosen.
    
    Returns a dictionary, e.g. {"label": "POSITIVE", "confidence": 0.62}.
    """
    if not sentiments:
        return {"label": "NEUTRAL", "confidence": 0.0}
    
    label_counts = {}
    label_confidence_sum = {}
    
    for sentiment in sentiments:
        label = sentiment.get("label", "NEUTRAL")
        score = sentiment.get("score", 0.0)
        label_counts[label] = label_counts.get(label, 0) + 1
        label_confidence_sum[label] = label_confidence_sum.get(label, 0.0) + score

    # Determine the maximum frequency
    max_count = max(label_counts.values())
    # Get all labels that have this frequency (in case of tie)
    candidates = [label for label, count in label_counts.items() if count == max_count]
    
    if len(candidates) == 1:
        chosen_label = candidates[0]
    else:
        # If tied, choose the label with the highest total confidence
        chosen_label = max(candidates, key=lambda l: label_confidence_sum[l])
    
    avg_confidence = label_confidence_sum[chosen_label] / label_counts[chosen_label]
    return {"label": chosen_label, "confidence": round(avg_confidence, 3)}

if __name__ == "__main__":
    # Example individual sentiment results
    sentiment_results = [
        {"label": "NEUTRAL", "score": 0.43},
        {"label": "POSITIVE", "score": 0.59},
        {"label": "NEGATIVE", "score": 0.76},
    ]
    
    overall = aggregate_sentiments(sentiment_results)
    print("Overall Aggregated Sentiment:", overall)

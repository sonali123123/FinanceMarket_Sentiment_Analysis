def aggregate_sentiments(sentiments: list) -> dict:
    """
    Aggregates sentiment results from multiple news items to produce an overall sentiment.
    
    This function counts the frequency of each sentiment label (e.g., POSITIVE, NEGATIVE, NEUTRAL)
    from the provided list of sentiment dictionaries and calculates the cumulative confidence for each.
    The overall sentiment is determined based on the following criteria:
      - If one label occurs most frequently, that label is chosen and its average confidence is computed.
      - In case of a tie (i.e., multiple labels share the highest frequency), the label with the highest 
        total confidence is selected.
    
    Parameters:
        sentiments (list): A list of dictionaries, each containing sentiment analysis results with keys
                           "label" (a string) and "score" (a float).
    
    Returns:
        dict: A dictionary with the overall sentiment label and its average confidence, rounded to three decimals.
              Example: {"label": "POSITIVE", "confidence": 0.62}.
    """
    # Return a neutral sentiment if the input list is empty.
    if not sentiments:
        return {"label": "NEUTRAL", "confidence": 0.0}
    
    # Initialize dictionaries to store counts and cumulative confidence scores for each sentiment label.
    label_counts = {}
    label_confidence_sum = {}
    
    # Iterate through each sentiment result in the input list.
    for sentiment in sentiments:
        # Retrieve the sentiment label; default to "NEUTRAL" if not present.
        label = sentiment.get("label", "NEUTRAL")
        # Retrieve the confidence score; default to 0.0 if not present.
        score = sentiment.get("score", 0.0)
        # Increment the count for the sentiment label.
        label_counts[label] = label_counts.get(label, 0) + 1
        # Add the score to the cumulative confidence for this label.
        label_confidence_sum[label] = label_confidence_sum.get(label, 0.0) + score

    # Determine the maximum frequency among the sentiment labels.
    max_count = max(label_counts.values())
    # Identify all labels that have the maximum frequency (handle possible ties).
    candidates = [label for label, count in label_counts.items() if count == max_count]
    
    if len(candidates) == 1:
        # If there is a single candidate, it is chosen as the overall sentiment.
        chosen_label = candidates[0]
    else:
        # In case of a tie, select the label with the highest cumulative confidence.
        chosen_label = max(candidates, key=lambda l: label_confidence_sum[l])
    
    # Calculate the average confidence for the chosen sentiment label.
    avg_confidence = label_confidence_sum[chosen_label] / label_counts[chosen_label]
    # Return the overall sentiment and its average confidence, rounded to three decimal places.
    return {"label": chosen_label, "confidence": round(avg_confidence, 3)}

def find_relevant_context(query: str, session_history: list, top_n: int = 3) -> list:
    """
    Find the top_n most similar message pairs to the query.
    
    Args:
        query: The current user message
        session_history: List of message pair dicts with embeddings
        top_n: Number of results to return
    
    Returns:
        List of the most relevant message pairs
    """
    # Step 1: Get embedding for the query
    query_embedding = get_embedding(query)
    
    # Step 2: Compute similarity for each message pair
    similarities = []
    for pair in session_history:
        # TODO: compute similarity between query_embedding and pair's embedding
        # TODO: store (similarity_score, pair) somewhere
        pass
    
    # Step 3: Sort by similarity and return top_n
    # TODO: sort similarities, take top N, return the pairs
    pass
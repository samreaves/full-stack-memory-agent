from models.message import Message
import numpy as np

def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    # Convert to numpy arrays
    a = np.array(vec1)
    b = np.array(vec2)

    # Calculate cosine similarity
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


async def find_relevant_context(message: Message, session_history: list[Message], top_n: int = 3) -> list[Message]:
    """
    Find the top_n most similar messages and their conversational pairs.
    """
    similarities = []

    for i, stored_message in enumerate(session_history):
        similarity_score = cosine_similarity(message.embedding, stored_message.embedding)
        similarities.append((similarity_score, i, stored_message))

    # Sort and get top N
    similarities.sort(key=lambda x: x[0], reverse=True)

    # Now grab pairs
    relevant_messages = []
    used_indices = set()

    for score, index, msg in similarities[:top_n]:
        if index in used_indices:
            continue

        # If it's a user message, grab it + next assistant message
        if msg.role == "user" and index + 1 < len(session_history):
            relevant_messages.append(session_history[index])
            relevant_messages.append(session_history[index + 1])
            used_indices.add(index)
            used_indices.add(index + 1)

        # If it's an assistant message, grab previous user + this assistant
        elif msg.role == "assistant" and index > 0:
            relevant_messages.append(session_history[index - 1])
            relevant_messages.append(session_history[index])
            used_indices.add(index - 1)
            used_indices.add(index)

    # Sort chronologically before returning
    relevant_messages.sort(key=lambda m: session_history.index(m))

    return relevant_messages
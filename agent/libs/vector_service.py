from schemas.message import Message
from sqlalchemy.orm import Session
from sqlalchemy.sql import text


async def find_relevant_context_from_db(
    db: Session,
    query_embedding: list[float],
    top_n: int = 3) -> list[Message]:
    """
    Find the top_n most similar messages and their conversational pairs.
    """
    # Get similar messages with their conversation context using a CTE
    query = text("""
        WITH similar_msgs AS (
            SELECT
                id,
                conversation_id,
                role,
                content,
                created_at,
                embedding <=> :query_embedding AS distance,
                LAG(id) OVER (PARTITION BY conversation_id ORDER BY created_at) AS prev_id,
                LEAD(id) OVER (PARTITION BY conversation_id ORDER BY created_at) AS next_id
            FROM messages
            ORDER BY distance
            LIMIT :top_n
        ),
        pairs AS (
            SELECT DISTINCT m.id
            FROM similar_msgs sm
            JOIN messages m ON (
                m.id = sm.id OR
                (sm.role = 'user' AND m.id = sm.next_id) OR
                (sm.role = 'assistant' AND m.id = sm.prev_id)
            )
        )
        SELECT m.* FROM messages m
        JOIN pairs p ON m.id = p.id
        ORDER BY m.created_at;
    """)

    result = db.execute(query, {
        "query_embedding": str(query_embedding),
        "top_n": top_n
    })

    # Convert to Message objects
    messages = [Message(**dict(row)) for row in result]
    return messages
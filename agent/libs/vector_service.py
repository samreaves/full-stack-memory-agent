from schemas.message import Message
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import json


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
                embedding <=> CAST(:query_embedding AS vector) AS distance,
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

    result = db.execute(
        query,
        {
            # Pass embedding as a string representation and cast to vector in SQL
            "query_embedding": str(query_embedding),
            "top_n": top_n,
        },
    )

    # Convert to Message objects; use RowMapping to avoid dict(...) issues
    messages = []
    for row in result:
        row_dict = dict(row._mapping)
        # Parse embedding from string to list if needed
        if isinstance(row_dict.get('embedding'), str):
            row_dict['embedding'] = json.loads(row_dict['embedding'])
        messages.append(Message(**row_dict))
    return messages
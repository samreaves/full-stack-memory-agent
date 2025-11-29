const API_PROTOCOL = import.meta.env.API_PROTOCOL || 'http';
const API_HOST = import.meta.env.API_HOST || 'localhost';
const API_PORT = import.meta.env.API_PORT || '8000';
const API_BASE_URL = `${API_PROTOCOL}://${API_HOST}:${API_PORT}`;

import type { Conversation } from '../interfaces/Conversation';
import type { ChatRequest, ChatResponse } from '../interfaces/ChatDTO';

/**
 * Create a new conversation with a title based on the first message
 */
export async function createConversation(message: string): Promise<Conversation> {
	const response = await fetch(`${API_BASE_URL}/conversations`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ message: message.trim() }),
	});

	if (!response.ok) {
		throw new Error(`Failed to create conversation: ${response.statusText}`);
	}

	return response.json();
}

/**
 * Get all conversations
 */
export async function getConversations(): Promise<Conversation[]> {
	const response = await fetch(`${API_BASE_URL}/conversations`);

	if (!response.ok) {
		throw new Error(`Failed to get conversations: ${response.statusText}`);
	}

	return response.json();
}

/**
 * Get a conversation by ID with all messages
 */
export async function getConversationById(id: string): Promise<Conversation> {
	const response = await fetch(`${API_BASE_URL}/conversations/${id}`);

	if (!response.ok) {
		if (response.status === 404) {
			throw new Error('Conversation not found');
		}
		throw new Error(`Failed to get conversation: ${response.statusText}`);
	}

	return response.json();
}

/**
 * Send a message and stream the response
 * Returns an async generator that yields tokens as they arrive
 */
export async function* sendMessage(
	conversationId: string,
	message: string
): AsyncGenerator<ChatResponse, void, unknown> {
	const chatRequest: ChatRequest = {
		conversation_id: conversationId,
		message: message.trim(),
	};
	const response = await fetch(`${API_BASE_URL}/chat`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify(chatRequest),
	});

	if (!response.ok) {
		throw new Error(`Failed to send message: ${response.statusText}`);
	}

	const reader = response.body?.getReader();
	if (!reader) {
		throw new Error('Response body is not readable');
	}

	const decoder = new TextDecoder();

	try {
		while (true) {
			const { done, value } = await reader.read();
			if (done) break;

			const chunk = decoder.decode(value);
			const lines = chunk.split('\n');

			for (const line of lines) {
				if (line.startsWith('data: ')) {
					try {
						const data = JSON.parse(line.slice(6));
						yield data;
					} catch (e) {
						// Skip invalid JSON
						continue;
					}
				}
			}
		}
	} finally {
		reader.releaseLock();
	}
}


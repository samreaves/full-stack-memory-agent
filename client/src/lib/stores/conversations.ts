import { writable, derived, get } from 'svelte/store';
import type { Conversation } from '../../interfaces/Conversation';
import type { Message } from '../../interfaces/Message';

export const conversations = writable<Record<string, Conversation>>({});
export const currentConversationId = writable<string | null>(null);


/**
 * Derived store for the current conversation
 */
export const currentConversation = derived(
	[conversations, currentConversationId],
	([$conversations, $currentConversationId]) => {
		if (!$currentConversationId) return null;
		return $conversations[$currentConversationId] || null;
	}
);

/**
 * Derived store for the list of conversations as an array
 */
export const conversationsList = derived(conversations, ($conversations) => {
	return Object.values($conversations).sort((a, b) => {
		// Sort by title or ID (simple sorting)
		return a.title.localeCompare(b.title);
	});
});

/**
 * Set all conversations
 */
export function setConversations(newConversations: Conversation[]) {
	const conversationsMap: Record<string, Conversation> = {};
	newConversations.forEach((conv) => {
		conversationsMap[conv.id] = conv;
	});
	conversations.set(conversationsMap);
}

/**
 * Add or update a conversation
 */
export function upsertConversation(conversation: Conversation) {
	conversations.update((conversationMap) => {
		conversationMap[conversation.id] = conversation;
		return conversationMap;
	});
}

/**
 * Update messages for a conversation
 */
export function updateConversationMessages(conversationId: string, messages: Message[]) {
	conversations.update((conversationMap) => {
		if (conversationMap[conversationId]) {
			conversationMap[conversationId].messages = messages;
		}
		return conversationMap;
	});
}

/**
 * Add a message to the current conversation
 */
export function addMessageToCurrentConversation(message: Message) {
	conversations.update((conversationMap) => {
		const currentIdValue = get(currentConversationId);
		
		if (currentIdValue && conversationMap[currentIdValue]) {
			if (!conversationMap[currentIdValue].messages) {
				conversationMap[currentIdValue].messages = [];
			}
			conversationMap[currentIdValue].messages!.push(message);
		}
		return conversationMap;
	});
}

/**
 * Update the last message in the current conversation (for streaming)
 */
export function updateLastMessage(content: string) {
	conversations.update((conversationMap) => {
		const currentIdValue = get(currentConversationId);
		
		if (currentIdValue && conversationMap[currentIdValue]?.messages) {
			const messages = conversationMap[currentIdValue].messages!;
			if (messages.length > 0) {
				const lastMessage = messages[messages.length - 1];
				if (lastMessage.role === 'assistant') {
					lastMessage.content = content;
				}
			}
		}
		return conversationMap;
	});
}


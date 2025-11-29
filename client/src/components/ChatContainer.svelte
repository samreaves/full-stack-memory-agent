<script lang="ts">
	import MessageList from './MessageList.svelte';
	import MessageInput from './MessageInput.svelte';
	import ConversationList from './ConversationList.svelte';
	import {
		conversations,
		currentConversationId,
		currentConversation,
		setConversations,
		upsertConversation,
		addMessageToCurrentConversation,
		updateLastMessage,
		removeLastAssistantMessageFromCurrentConversation
	} from '$lib/stores/conversations';
	import { createConversation, getConversations, getConversationById, sendMessage } from '$lib/api';
	import { onMount } from 'svelte';
	import { get } from 'svelte/store';

let isLoading = false;
let isAwaitingFirstToken = false;
let showSidebar = true;

	onMount(async () => {
		// Load all conversations on mount
		try {
			const allConversations = await getConversations();
			setConversations(allConversations);
		} catch (error) {
			console.error('Error loading conversations:', error);
		}
	});

	// Get messages for current conversation
	$: messages = $currentConversation?.messages || [];

	async function handleSendMessage(messageText: string) {
		const trimmedMessage = messageText.trim();
		if (!trimmedMessage || isLoading) return;

		isLoading = true;

		let conversationId = get(currentConversationId);
		const hasRealConversation =
			!!conversationId && !conversationId.toString().startsWith('temp-');
		let tempConversationId: string | null = null;

		try {
			// If there is no conversation at all yet, create a temporary one
			if (!conversationId) {
				tempConversationId = `temp-${Date.now()}`;

				const title =
					trimmedMessage.length > 40
						? `${trimmedMessage.slice(0, 40)}...`
						: trimmedMessage || 'New conversation';

				upsertConversation({
					id: tempConversationId,
					title,
					messages: []
				});

				currentConversationId.set(tempConversationId);
				conversationId = tempConversationId;
			}

			// Add user message to UI immediately
			addMessageToCurrentConversation({
				role: 'user',
				content: trimmedMessage
			});

			// Add placeholder for assistant response
			addMessageToCurrentConversation({
				role: 'assistant',
				content: ''
			});

			// Show inline loader in the assistant bubble until the first token arrives
			isAwaitingFirstToken = true;

			// Ensure there is a real backend conversation ID before streaming
			if (!hasRealConversation) {
				const newConversation = await createConversation(trimmedMessage);

				// If we started with a temporary conversation, migrate its messages
				if (tempConversationId) {
					conversations.update((conversationMap) => {
						const tempConversation = conversationMap[tempConversationId!];
						const messages = tempConversation?.messages ?? [];

						conversationMap[newConversation.id] = {
							...newConversation,
							messages
						};

						delete conversationMap[tempConversationId!];

						return conversationMap;
					});
				} else {
					upsertConversation(newConversation);
				}

				currentConversationId.set(newConversation.id);
				conversationId = newConversation.id;
			}

			// Stream the response
			let fullResponse = '';
			try {
				for await (const chunk of sendMessage(conversationId as string, trimmedMessage)) {
					if (chunk.token) {
						// First token has arrived; hide the inline loader
						if (isAwaitingFirstToken) {
							isAwaitingFirstToken = false;
						}

						fullResponse += chunk.token;
						updateLastMessage(fullResponse);
					}

					if (chunk.done) {
						break;
					}

					if (chunk.error) {
						updateLastMessage(`Error: ${chunk.error}`);
						break;
					}
				}

				// Reload conversation to get updated messages from server
				if (conversationId) {
					const updatedConversation = await getConversationById(conversationId as string);
					upsertConversation(updatedConversation);
				}
			} catch (error) {
				console.error('Error sending message:', error);
				updateLastMessage(
					`Error: ${error instanceof Error ? error.message : 'Unknown error'}`
				);
			}
		} catch (error) {
			console.error('Error in handleSendMessage:', error);

			// Clean up the assistant placeholder/loader on error
			removeLastAssistantMessageFromCurrentConversation();
		} finally {
			isLoading = false;
			// Ensure loader is cleared even if no tokens arrive
			isAwaitingFirstToken = false;
		}
	}

	function toggleSidebar() {
		showSidebar = !showSidebar;
	}
</script>

<div class="app-container">
	{#if showSidebar}
		<ConversationList />
	{/if}
	<div class="chat-container">
		<div class="chat-header">
			<button class="sidebar-toggle" on:click={toggleSidebar}>☰</button>
			<span>AI Chat with Memory - Phase 3</span>
		</div>
		<MessageList messages={messages} isAwaitingFirstToken={isAwaitingFirstToken} />
		<MessageInput onSend={handleSendMessage} disabled={isLoading} />
	</div>
</div>

<style>
	.app-container {
		display: flex;
		height: 100vh;
		width: 100vw;
		background: #f5f5f5;
	}

	.chat-container {
		flex: 1;
		display: flex;
		flex-direction: column;
		background: white;
		overflow: hidden;
	}

	.chat-header {
		padding: 20px;
		background: #4a90e2;
		color: white;
		font-size: 18px;
		font-weight: 600;
		display: flex;
		align-items: center;
		gap: 12px;
	}

	.sidebar-toggle {
		background: rgba(255, 255, 255, 0.2);
		border: none;
		color: white;
		padding: 8px 12px;
		border-radius: 4px;
		cursor: pointer;
		font-size: 16px;
		transition: background 0.2s;
	}

	.sidebar-toggle:hover {
		background: rgba(255, 255, 255, 0.3);
	}
</style>


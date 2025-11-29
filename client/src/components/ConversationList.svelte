<script lang="ts">
	import { conversationsList, currentConversationId, upsertConversation } from '$lib/stores/conversations';
	import { getConversationById } from '$lib/api';

	async function selectConversation(conversationId: string) {
		if ($currentConversationId === conversationId) return;

		try {
			// Load full conversation with messages
			const conversation = await getConversationById(conversationId);
			upsertConversation(conversation);
			currentConversationId.set(conversationId);
		} catch (error) {
			console.error('Error loading conversation:', error);
		}
	}

	function startNewConversation() {
		if ($currentConversationId === null) return;
		currentConversationId.set(null);
	}
</script>

<div class="conversation-list">
	<h3 class="list-header">
		<span>Conversations</span>
		<button class="new-conversation" on:click={startNewConversation} aria-label="Start new conversation">
			+
		</button>
	</h3>
	<div class="conversations">
		{#each $conversationsList as conversation}
			<button
				class="conversation-item {$currentConversationId === conversation.id ? 'active' : ''}"
				on:click={() => selectConversation(conversation.id)}
			>
				{conversation.title}
			</button>
		{/each}
		{#if $conversationsList.length === 0}
			<div class="empty">No conversations yet</div>
		{/if}
	</div>
</div>

<style>
	.conversation-list {
		width: 250px;
		background: #f8f9fa;
		border-right: 1px solid #e0e0e0;
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}

	.list-header {
		padding: 20px;
		margin: 0;
		font-size: 18px;
		font-weight: 600;
		color: #333;
		border-bottom: 1px solid #e0e0e0;
		background: white;
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 12px;
	}

	.new-conversation {
		width: 32px;
		height: 32px;
		border-radius: 50%;
		border: none;
		background: #4a90e2;
		color: white;
		font-size: 20px;
		cursor: pointer;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		font-weight: 600;
		transition: background 0.2s;
	}

	.new-conversation:hover {
		background: #357abd;
	}

	.conversations {
		flex: 1;
		overflow-y: auto;
		padding: 8px;
	}

	.conversation-item {
		width: 100%;
		padding: 12px 16px;
		text-align: left;
		border: none;
		background: white;
		border-radius: 8px;
		margin-bottom: 4px;
		cursor: pointer;
		transition: background 0.2s;
		font-family: inherit;
		font-size: 14px;
		color: #333;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.conversation-item:hover {
		background: #e9ecef;
	}

	.conversation-item.active {
		background: #4a90e2;
		color: white;
	}

	.empty {
		padding: 20px;
		text-align: center;
		color: #888;
		font-style: italic;
	}
</style>


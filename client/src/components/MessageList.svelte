<script lang="ts">
	import type { Message } from '$lib/api';
	import { onMount } from 'svelte';

	export let messages: Message[] = [];

	let messagesContainer: HTMLDivElement;

	// Auto-scroll to bottom when messages change
	$: if (messagesContainer && messages.length > 0) {
		setTimeout(() => {
			messagesContainer.scrollTop = messagesContainer.scrollHeight;
		}, 0);
	}

	onMount(() => {
		if (messagesContainer) {
			messagesContainer.scrollTop = messagesContainer.scrollHeight;
		}
	});
</script>

<div class="messages-container" bind:this={messagesContainer}>
	{#each messages as message}
		<div class="message {message.role}">
			{message.content}
		</div>
	{/each}
</div>

<style>
	.messages-container {
		flex: 1;
		overflow-y: auto;
		padding: 20px;
		display: flex;
		flex-direction: column;
		gap: 12px;
	}

	.message {
		max-width: 70%;
		padding: 12px 16px;
		border-radius: 12px;
		line-height: 1.4;
		word-wrap: break-word;
	}

	.message.user {
		align-self: flex-end;
		background: #4a90e2;
		color: white;
	}

	.message.assistant {
		align-self: flex-start;
		background: #e9ecef;
		color: #333;
	}
</style>


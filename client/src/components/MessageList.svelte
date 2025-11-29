<script lang="ts">
	import type { Message } from '$lib/api';
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import LoadingIndicator from './LoadingIndicator.svelte';

	export let messages: Message[] = [];
	export let isAwaitingFirstToken: boolean = false;

	let messagesContainer: HTMLDivElement;
	let lastAssistantIndex = -1;

	// Track the index of the last assistant message so we know which one is streaming
	$: {
		lastAssistantIndex = -1;
		messages.forEach((message, index) => {
			if (message.role === 'assistant') {
				lastAssistantIndex = index;
			}
		});
	}

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
	{#each messages as message, index (message.role + '-' + index)}
		{#if message.role === 'user'}
			<div class="message user">
				{message.content}
			</div>
		{:else}
			<div class="message assistant" in:fade={{ duration: 300 }}>
				{#if isAwaitingFirstToken && index === lastAssistantIndex && !message.content}
					<LoadingIndicator />
				{:else}
					<span class="assistant-text">{message.content}</span>
				{/if}
			</div>
		{/if}
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
		line-height: 1.6;
		word-wrap: break-word;
	}

	.message.user {
		align-self: flex-end;
		max-width: 70%;
		padding: 12px 16px;
		border-radius: 12px;
		background: #4a90e2;
		color: white;
	}

	.message.assistant {
		align-self: flex-start;
		max-width: 100%;
		padding: 0;
		color: #333;
	}

	.assistant-text {
		display: inline;
		opacity: 1;
		transition: opacity 0.15s ease-in-out;
	}
</style>


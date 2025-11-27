<script lang="ts">
	export let disabled: boolean = false;
	export let onSend: (message: string) => void;

	let messageInput: HTMLInputElement;
	let message = '';

	function handleSend() {
		const trimmed = message.trim();
		if (!trimmed || disabled) return;
		
		onSend(trimmed);
		message = '';
		messageInput?.focus();
	}

	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'Enter' && !event.shiftKey) {
			event.preventDefault();
			handleSend();
		}
	}
</script>

<div class="input-container">
	<input
		type="text"
		bind:this={messageInput}
		bind:value={message}
		on:keypress={handleKeyPress}
		placeholder="Type your message..."
		autocomplete="off"
		disabled={disabled}
	/>
	<button on:click={handleSend} disabled={disabled}>
		Send
	</button>
</div>

<style>
	.input-container {
		padding: 20px;
		border-top: 1px solid #e0e0e0;
		display: flex;
		gap: 12px;
	}

	input {
		flex: 1;
		padding: 12px 16px;
		border: 1px solid #ddd;
		border-radius: 24px;
		font-size: 14px;
		outline: none;
		transition: border-color 0.2s;
		font-family: inherit;
	}

	input:focus {
		border-color: #4a90e2;
	}

	input:disabled {
		opacity: 0.6;
		cursor: not-allowed;
	}

	button {
		padding: 12px 24px;
		background: #4a90e2;
		color: white;
		border: none;
		border-radius: 24px;
		font-size: 14px;
		font-weight: 600;
		cursor: pointer;
		transition: background 0.2s;
		font-family: inherit;
	}

	button:hover:not(:disabled) {
		background: #357abd;
	}

	button:disabled {
		background: #ccc;
		cursor: not-allowed;
	}
</style>


<script lang="ts">
	import ChatContainer from '$components/ChatContainer.svelte';
</script>

<svelte:head>
	<title>AI Chat with Memory</title>
</svelte:head>

<ChatContainer />

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		box-sizing: border-box;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu,
			Cantarell, sans-serif;
	}

	:global(*),
	:global(*::before),
	:global(*::after) {
		box-sizing: inherit;
	}
</style>


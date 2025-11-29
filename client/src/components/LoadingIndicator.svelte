<div class="loading-indicator">
	<span class="dot"></span>
	<span class="dot"></span>
	<span class="dot"></span>
</div>

<style>
	.loading-indicator {
		display: inline-flex;
		align-items: center;
		gap: 4px;
		padding: 2px 0;
		height: 1.6em;
	}

	.dot {
		width: 6px;
		height: 6px;
		border-radius: 50%;
		background-color: #888;
		animation: typing 1.2s infinite ease-in-out;
		opacity: 0.3;
	}

	.dot:nth-child(1) {
		animation-delay: 0s;
	}

	.dot:nth-child(2) {
		animation-delay: 0.2s;
	}

	.dot:nth-child(3) {
		animation-delay: 0.4s;
	}

	@keyframes typing {
		0%, 60%, 100% {
			opacity: 0.3;
			transform: scale(1);
		}
		30% {
			opacity: 1;
			transform: scale(1.2);
		}
	}
</style>


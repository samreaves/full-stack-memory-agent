export interface ChatRequest {
	conversation_id: string;
	message: string;
}

export interface ChatResponse {
	token?: string;
	done?: boolean;
	error?: string;
}
import { useState, useRef, useEffect } from "react";
import { sendMessage } from "../services/api";
import Message from "./Message";

function ChatBox({
    messages,
    setMessages,
    conversationId,
    setConversationId,
    pendingMediaId,
    setPendingMediaId
}) {
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, loading]);

    const handleSend = async () => {
        if (!input.trim() || loading) return;

        const userMessage = { role: "user", content: input };
        setMessages((prev) => [...prev, userMessage]);

        const messageText = input;
        setInput("");
        setLoading(true);

        try {
            const data = await sendMessage(messageText, conversationId, pendingMediaId);
            setConversationId(data.conversation_id);
            setPendingMediaId(null);
            setMessages((prev) => [
                ...prev,
                { role: "bot", content: data.reply }
            ]);
        } catch {
            setMessages((prev) => [
                ...prev,
                { role: "bot", content: "Something went wrong. Please try again." }
            ]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="chat-box">
            <div className="messages">
                {messages.map((message, index) => (
                    <Message key={index} message={message} />
                ))}
                {loading && (
                    <div className="message-wrapper bot">
                        <div className="message-bubble bot-bubble">
                            <div className="message-role">Mechanic</div>
                            <p className="message-content">Thinking...</p>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="chat-input-wrapper">
                <textarea
                    className="chat-input-textarea"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Describe your car problem..."
                    rows={Math.min(4, input.split("\n").length || 1)}
                />
                <button
                    className="send-btn"
                    onClick={handleSend}
                    disabled={loading || !input.trim()}
                >
                    Send
                </button>
            </div>
        </div>
    );
}

export default ChatBox;
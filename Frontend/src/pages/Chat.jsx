import { useState } from "react";
import ChatBox from "../components/ChatBox";
import MediaUpload from "../components/MediaUpload";
import DiagnosisCard from "../components/DiagnosisCard";
import BookingForm from "../components/BookingForm";
import Navbar from "../components/Navbar";
import { getDiagnosis, getMediaUrl } from "../services/api";

function Chat() {
    const [messages, setMessages] = useState([]);
    const [conversationId, setConversationId] = useState(null);
    const [diagnosis, setDiagnosis] = useState(null);
    const [showBooking, setShowBooking] = useState(false);
    const [loadingDiagnosis, setLoadingDiagnosis] = useState(false);
    const [pendingMediaId, setPendingMediaId] = useState(null);

    const handleNewChat = () => {
        setMessages([]);
        setConversationId(null);
        setDiagnosis(null);
        setShowBooking(false);
        setPendingMediaId(null);
    };

    const handleMediaUploaded = (data) => {
        const mediaUrl = getMediaUrl(data.file);
        const mediaType = data.media_type?.includes("/")
            ? data.media_type
            : `${data.media_type}/uploaded`;

        setMessages((prev) => [
            ...prev,
            {
                role: "user",
                content: "Uploaded a file.",
                media: {
                    type: mediaType,
                    url: mediaUrl,
                }
            },
            {
                role: "bot",
                content: "I have received your file. Please describe the problem you're experiencing.",
            }
        ]);
        setPendingMediaId(data.id);
        if (data.conversation_id && !conversationId) {
            setConversationId(data.conversation_id);
        }
    };

    const createDiagnosis = async () => {
        if (!conversationId || messages.length === 0) return;

        const userMessages = messages
            .filter((message) => message.role === "user")
            .map((message) => message.content)
            .join("\n");
            
        const problem = userMessages;
        setLoadingDiagnosis(true);

        try {
            const data = await getDiagnosis(conversationId, problem);
            setDiagnosis(data);
        } catch {
            alert("Could not generate diagnosis. Please try again.");
        } finally {
            setLoadingDiagnosis(false);
        }
    };

    return (
        <div className="chat-page">
            <Navbar onNewChat={handleNewChat} />
            <main className="chat-main">
                <div className="chat-container">
                    <ChatBox
                        messages={messages}
                        setMessages={setMessages}
                        conversationId={conversationId}
                        setConversationId={setConversationId}
                        pendingMediaId={pendingMediaId}
                        setPendingMediaId={setPendingMediaId}
                    />
                    <div className="chat-actions">
                        <MediaUpload 
                            conversationId={conversationId} 
                            onMediaUploaded={handleMediaUploaded} 
                        />
                        <button
                            className="diagnosis-btn"
                            onClick={createDiagnosis}
                            disabled={loadingDiagnosis || messages.length === 0}
                        >
                            {loadingDiagnosis ? "Analyzing..." : "Generate Diagnosis"}
                        </button>
                    </div>
                </div>

                {(diagnosis || showBooking) && (
                    <div className="sidebar-container">
                        {!showBooking ? (
                            <DiagnosisCard
                                diagnosis={diagnosis}
                                onBook={() => setShowBooking(true)}
                                onClose={() => {
                                    setDiagnosis(null);
                                    setShowBooking(false);
                                }}
                            />
                        ) : (
                            <BookingForm
                                problem={diagnosis?.problem}
                                onClose={() => setShowBooking(false)}
                                onBooked={() => {
                                    // Let the form show confirmation
                                }}
                            />
                        )}
                    </div>
                )}
            </main>
        </div>
    );
}

export default Chat;
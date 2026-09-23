import React from "react";

const Message = ({ message }) => {
    const isUser = message.role === "user";

    const renderMedia = () => {
        if (!message.media) return null;
        
        const { type, url } = message.media;
        
        if (type.startsWith("image/")) {
            return <img src={url} alt="Uploaded media" className="message-media" />;
        }
        if (type.startsWith("video/")) {
            return (
                <video controls className="message-media">
                    <source src={url} type={type} />
                    Your browser does not support the video tag.
                </video>
            );
        }
        if (type.startsWith("audio/")) {
            return (
                <audio controls className="message-media">
                    <source src={url} type={type} />
                    Your browser does not support the audio element.
                </audio>
            );
        }
        
        return <a href={url} target="_blank" rel="noopener noreferrer">View Attachment</a>;
    };

    return (
        <div className={`message-wrapper ${isUser ? "user" : "bot"}`}>
            <div className={`message-bubble ${isUser ? "user-bubble" : "bot-bubble"}`}>
                <div className="message-role">{isUser ? "You" : "Mechanic"}</div>
                {message.content && <p className="message-content">{message.content}</p>}
                {renderMedia()}
                {message.timestamp && <span className="message-time">{message.timestamp}</span>}
            </div>
        </div>
    );
};

export default Message;

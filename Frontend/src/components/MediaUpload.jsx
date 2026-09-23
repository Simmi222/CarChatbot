import { useState } from "react";
import { uploadMedia } from "../services/api";

function MediaUpload({ conversationId, onMediaUploaded }) {
    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState({ text: "", type: "" });

    const handleUpload = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        setUploading(true);
        setMessage({ text: "", type: "" });

        try {
            const data = await uploadMedia(file, conversationId);
            setMessage({ text: "Media uploaded successfully.", type: "success" });
            if (onMediaUploaded) {
                onMediaUploaded(data);
            }
        } catch (error) {
            setMessage({ text: "Media upload failed.", type: "error" });
        } finally {
            setUploading(false);
            event.target.value = null;
        }
    };

    return (
        <div className="media-upload">
            <label className="media-upload-label">
                📎 Attach Media
                <input
                    type="file"
                    accept="image/*,audio/*,video/*"
                    onChange={handleUpload}
                    hidden
                />
            </label>
            {uploading && <span className="upload-status uploading"> Uploading...</span>}
            {message.text && (
                <span className={`upload-status ${message.type}`}>
                    {message.text}
                </span>
            )}
        </div>
    );
}

export default MediaUpload;
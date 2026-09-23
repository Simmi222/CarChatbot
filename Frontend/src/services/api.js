import axios from "axios";

const API = axios.create({
    baseURL:
        import.meta.env.VITE_API_URL ||
        (import.meta.env.PROD ? "/api" : "http://127.0.0.1:8000/api"),
});

export const getMediaUrl = (path) => {
    if (!path || path.startsWith("http")) return path;
    const origin = import.meta.env.VITE_API_URL
        ? new URL(import.meta.env.VITE_API_URL).origin
        : window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
            ? "http://127.0.0.1:8000"
            : window.location.origin;
    return new URL(path, origin).toString();
};

export const sendMessage = async (
    message,
    conversationId = null,
    mediaId = null
) => {

    const response = await API.post(
        "/chat/",
        {
            message,
            conversation_id: conversationId,
            media_id: mediaId,
        }
    );

    return response.data;
};


export const uploadMedia = async (file, conversationId = null) => {

    const formData = new FormData();

    formData.append("file", file);
    if (conversationId) {
        formData.append("conversation_id", conversationId);
    }

    const response = await API.post(
        "/upload/",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data",
            },
        }
    );

    return response.data;
};


export const getDiagnosis = async (
    conversationId,
    problem
) => {

    const response = await API.post(
        "/diagnosis/",
        {
            conversation_id: conversationId,
            problem,
        }
    );

    return response.data;
};


export const bookMechanic = async (data) => {

    const response = await API.post(
        "/booking/",
        data
    );

    return response.data;
};


export const getBooking = async (id) => {

    const response = await API.get(
        `/booking/${id}/`
    );

    return response.data;
};
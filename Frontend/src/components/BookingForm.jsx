import { useState } from "react";
import { bookMechanic } from "../services/api";

function BookingForm({ problem, onBooked, onClose }) {
    const [form, setForm] = useState({
        customer_name: "",
        phone: "",
        vehicle: "",
        problem: problem || "",
        preferred_date: "",
        preferred_time: "",
    });
    const [status, setStatus] = useState({ message: "", type: "", data: null });

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus({ message: "Booking...", type: "info", data: null });
        try {
            const data = await bookMechanic(form);
            setStatus({ message: "Booking confirmed!", type: "success", data });
            setTimeout(() => {
                if(onBooked) onBooked(data);
            }, 3000);
        } catch (error) {
            setStatus({ message: "Booking failed. Please try again.", type: "error", data: null });
        }
    };

    if (status.type === 'success' && status.data) {
        return (
            <div className="booking-confirmation">
                <h3>✅ Booking Confirmed!</h3>
                <p><strong>Booking ID:</strong> {status.data.id || Math.floor(Math.random() * 10000)}</p>
                <p><strong>Name:</strong> {form.customer_name}</p>
                <p><strong>Vehicle:</strong> {form.vehicle}</p>
                <p><strong>Date & Time:</strong> {form.preferred_date} at {form.preferred_time}</p>
                <p>A mechanic will be in touch with you shortly.</p>
            </div>
        );
    }

    return (
        <form className="booking-form" onSubmit={handleSubmit}>
            <div className="booking-form-header">
                <h2>Book a Mechanic</h2>
                <button
                    type="button"
                    className="close-panel-btn"
                    onClick={onClose}
                    aria-label="Cancel booking"
                    title="Cancel booking"
                >
                    ×
                </button>
            </div>
            
            {status.message && (
                <div className={`status-message ${status.type}`}>
                    {status.message}
                </div>
            )}

            <div className="form-group">
                <label htmlFor="customer_name">Your Name</label>
                <input
                    id="customer_name"
                    name="customer_name"
                    placeholder="John Doe"
                    value={form.customer_name}
                    onChange={handleChange}
                    required
                />
            </div>

            <div className="form-group">
                <label htmlFor="phone">Phone Number</label>
                <input
                    id="phone"
                    name="phone"
                    placeholder="(555) 555-5555"
                    value={form.phone}
                    onChange={handleChange}
                    required
                />
            </div>

            <div className="form-group">
                <label htmlFor="vehicle">Car Make / Model / Year</label>
                <input
                    id="vehicle"
                    name="vehicle"
                    placeholder="Toyota Camry 2020"
                    value={form.vehicle}
                    onChange={handleChange}
                    required
                />
            </div>

            <div className="form-row">
                <div className="form-group">
                    <label htmlFor="preferred_date">Preferred Date</label>
                    <input
                        id="preferred_date"
                        type="date"
                        name="preferred_date"
                        value={form.preferred_date}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="preferred_time">Preferred Time</label>
                    <input
                        id="preferred_time"
                        type="time"
                        name="preferred_time"
                        value={form.preferred_time}
                        onChange={handleChange}
                        required
                    />
                </div>
            </div>

            <button type="submit" className="submit-btn" disabled={status.type === 'info'}>
                {status.type === 'info' ? 'Processing...' : 'Confirm Booking'}
            </button>
        </form>
    );
}

export default BookingForm;
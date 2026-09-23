function DiagnosisCard({ diagnosis, onBook, onClose }) {
    if (!diagnosis) return null;

    const getSeverityColor = (severity) => {
        const s = severity?.toLowerCase() || '';
        if (s.includes('high')) return 'red';
        if (s.includes('medium')) return 'orange';
        if (s.includes('low')) return 'green';
        return 'inherit';
    };

    return (
        <div className="diagnosis-card">
            <div className="diagnosis-card-header">
                <h2><span aria-hidden="true">🔧</span> Diagnosis</h2>
                <button
                    type="button"
                    className="close-panel-btn"
                    onClick={onClose}
                    aria-label="Close diagnosis"
                    title="Close diagnosis"
                >
                    ×
                </button>
            </div>
            <p><strong>Problem:</strong> {diagnosis.problem}</p>
            <p><strong>Diagnosis:</strong> {diagnosis.diagnosis}</p>
            <p><strong>Recommendation:</strong> {diagnosis.recommendation}</p>
            <p>
                <strong>Severity:</strong>{" "}
                <span style={{ color: getSeverityColor(diagnosis.severity), fontWeight: 'bold' }}>
                    {diagnosis.severity}
                </span>
            </p>
            <button className="book-btn cta-btn" onClick={onBook}>
                Book Mechanic
            </button>
        </div>
    );
}

export default DiagnosisCard;
const Navbar = ({ onNewChat }) => {
    return (
        <nav className="navbar">
            <div className="navbar-brand">
                <span className="brand-mark" aria-hidden="true">
                    <span className="brand-wheel left" />
                    <span className="brand-wheel right" />
                </span>
                <span className="brand-copy">
                    <strong>AutoAid</strong>
                    <small>AI CAR MECHANIC</small>
                </span>
            </div>
            <button className="new-chat-btn" onClick={onNewChat}>
                <span aria-hidden="true">+</span> New chat
            </button>
        </nav>
    );
};

export default Navbar;

const LoginForm = ({
    onSubmit,
    email,
    setEmail,
    password,
    setPassword,
    showPassword,
    togglePassword,
    action
}) => {
    return (
        <form className="auth-form" onSubmit={onSubmit}>

            <h2 className="auth-title">{action}</h2>

            <div className="form-group">
                <label>Email</label>
                <input
                    type="email"
                    required
                    value={email}
                    placeholder="Enter your email"
                    onChange={e => setEmail(e.target.value)}
                />
            </div>

            <div className="form-group">
                <label>Password</label>

                <div className="password-row">
                    <input
                        type={showPassword ? 'text':'password'}
                        required
                        value={password}
                        placeholder="Enter your password"
                        onChange={e => setPassword(e.target.value)}
                    />
                    <button
                        type="button"
                        className="secondary-btn"
                        onClick={togglePassword}
                    >
                        {showPassword ? "Hide":"Show"}
                    </button>
                </div>
            </div>
            <button
                className="primary-btn"
                type="submit"
            >
                {action}
            </button>
        </form>
    )
}

export default LoginForm
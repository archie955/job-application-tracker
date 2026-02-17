const LoginForm = (props) => {
    return (
        <form onSubmit={props.loginFunction}>
            <div>
                <h2>{props.action}</h2>
            </div>
            <div>
                email: <input
                    value={props.email}
                    placeholder="Enter your email"
                    onChange={e => props.setEmail(e.target.value)}
                    />
            </div>
            <div>
                password: <input
                    type={props.showPassword ? 'text':'password'}
                    value={props.password}
                    placeholder="Enter your password"
                    onChange={e => props.setPassword(e.target.value)}/>
                <button type="button" onClick={props.setShowPassword}>{props.showPassword ? "Hide":"Show"}</button>
            </div>
            <button type="submit">{props.action}</button>
        </form>
    )
}

export default LoginForm
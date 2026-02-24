import { Routes, Route } from "react-router-dom"
import Login from "./pages/Login"
import Register from "./pages/Register"
import Home from "./pages/Home"
import { AuthProvider } from "./components/AuthProvider"
import ProtectedRoute from "./components/ProtectedRoute"

const App = () => {
    return(
        <AuthProvider>
            <Routes>
                <Route path="/login" element={<Login />} />
                <Route path="/" element={<Register />} />
                <Route path="/home" element={
                    <ProtectedRoute>
                        <Home />
                    </ProtectedRoute>
                    } />
            </Routes>
        </AuthProvider>
    )
}

export default App
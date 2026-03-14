import { Routes, Route } from "react-router-dom"
import Login from "./pages/Login"
import Register from "./pages/Register"
import Home from "./pages/Home"
import { AuthProvider } from "./components/AuthProvider"
import ProtectedRoute from "./components/ProtectedRoute"
import './styling/styles.css'

const App = () => {
    return(
        <AuthProvider>
            <Routes>
                <Route index element={<Login />} />
                <Route path="/register" element={<Register />} />
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
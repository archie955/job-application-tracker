import axios from "axios"

const BASEURL = import.meta.env.VITE_BASEURL


const api = axios.create({
    baseURL: BASEURL,
    withCredentials: true
})

export const setAuthToken = (token) => {
    if (token) {
        api.defaults.headers.common["Authorization"] = `Bearer ${token}`
    } else {
        delete api.defaults.headers.common["Authorization"]
    }
}

export default api
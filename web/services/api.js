import axios from "axios"

const BASEURL = import.meta.env.VITE_BASEURL


const api = axios.create({
    baseURL: BASEURL,
    withCredentials: true
})

export const setupInterceptors = (getAccessToken, setAccessToken) => {
    api.interceptors.request.use((config) => {
        const token = getAccessToken()
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    })

    api.interceptors.response.use(
        (response) => response,
        async (error) => {
            const originalRequest = error.config

            if (error.response?.status === 401 && 
                !originalRequest._retry && 
                !originalRequest.url.includes("/users/refresh") && 
                !originalRequest.url.includes("/users/login")
            ) {
                originalRequest._retry = true

                try {
                    const res = await api.post("/users/refresh")
                    const newAccess = res.data.access_token

                    setAccessToken(newAccess)

                    originalRequest.headers.Authorization = `Bearer ${newAccess}`

                    return api(originalRequest)
                } catch (err) {
                    setAccessToken(null)
                    return Promise.reject(err)
                }
            }

            return Promise.reject(error)
        }
    )
}

export default api
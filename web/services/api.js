import axios from "axios"

const BASEURL = import.meta.env.VITE_BASEURL


const api = axios.create({
    baseURL: BASEURL,
    withCredentials: true
})

export default api
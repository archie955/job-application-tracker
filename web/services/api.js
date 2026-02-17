require('dotenv').config()
import axios from "axios"



const api = axios.create({
    baseURL: process.env.BASEURL,
    withCredentials: true
})

export default api
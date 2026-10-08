import axios from 'axios'

const request = axios.create({
    baseURL: '/api',        // 所有请求自动加 /api 前缀
    timeout: 10000,
})

// 响应拦截：统一处理错误
request.interceptors.response.use(
    (res) => res.data,
    (err) => {
        console.error('请求失败:', err)
        return Promise.reject(err)
    }
)

export default request
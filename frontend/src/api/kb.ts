import request from './request'

// 获取知识库列表
export function getKbList() {
    return request.get('/kb')
}

// 新建知识库
export function createKb(data: { name: string; description?: string }) {
    return request.post('/kb', data)
}

// 删除知识库
export function deleteKb(id: string) {
    return request.delete(`/kb/${id}`)
}
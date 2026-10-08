import request from './request'

export interface Doc {
    id: string
    filename: string
    size: number
    status: 'processing' | 'ready' | 'failed'
    chunks: number
    uploaded_at: string
}

// 获取某知识库的文档列表
export function getDocList(kbId: string) {
    return request.get<Doc[]>(`/kb/${kbId}/docs`)
}

// 上传文档
export function uploadDoc(kbId: string, file: File) {
    const formData = new FormData()
    formData.append('file', file)
    return request.post<Doc>(`/kb/${kbId}/docs`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
    })
}

// 删除文档
export function deleteDoc(kbId: string, docId: string) {
    return request.delete(`/kb/${kbId}/docs/${docId}`)
}
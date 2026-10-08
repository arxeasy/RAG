import request from './request'

export interface ChatSession {
    id: string
    kb_id: string
    title: string
    created_at: string
}

export function getSessionList(kbId: string) {
    return request.get<ChatSession[]>(`/kb/${kbId}/sessions`)
}

export function createSession(kbId: string, title?: string) {
    return request.post<ChatSession>(`/kb/${kbId}/sessions`, {
        title: title ?? '新对话',
    })
}

// 删除session
export function deleteSession(kbId: string, sessionId: string) {
    return request.delete(`/kb/${kbId}/sessions/${sessionId}`)
}
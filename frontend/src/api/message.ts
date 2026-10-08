import request from './request'

export interface Message {
    id: string
    session_id: string
    role: 'user' | 'assistant'
    content: string
    created_at: string
}

// 获取会话的历史消息
export function getHistoryMessage(kbId: string, sessionId: string) {
    return request.get<Message[]>(`/kb/${kbId}/sessions/${sessionId}/messages`)
}

// 发送消息（普通，一次性返回）
export function sendMessage(
    kbId: string,
    sessionId: string,
    content: string,
    useKb: boolean = true,
) {
    return request.post<Message>(`/kb/${kbId}/sessions/${sessionId}/messages`, {
        content,
        use_kb: useKb,
    })
}
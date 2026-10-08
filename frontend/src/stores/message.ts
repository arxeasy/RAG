import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getHistoryMessage, sendMessage, type Message } from '@/api/message'

export const useMessageStore = defineStore('message', () => {
    const list = ref<Message[]>([])
    const sending = ref(false)

    async function fetchList(kbId: string, sessionId: string) {
        list.value = await getHistoryMessage(kbId, sessionId)
    }

    async function send(kbId: string, sessionId: string, content: string, useKb: boolean) {
        sending.value = true
        try {
            // 1. 先乐观添加用户消息（可选）
            const userMsg: Message = {
                id: `temp-${Date.now()}`,
                session_id: sessionId,
                role: 'user',
                content,
                created_at: new Date().toISOString(),
            }
            list.value.push(userMsg)

            // 2. 调后端
            const aiMsg = await sendMessage(kbId, sessionId, content, useKb)

            // 3. 追加 AI 回复
            list.value.push(aiMsg)
        } finally {
            sending.value = false
        }
    }

    return { list, sending, fetchList, send }
})
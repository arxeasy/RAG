import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
    getSessionList,
    createSession as createSessionApi,
    deleteSession as deleteSessionApi,
    type ChatSession,
} from '@/api/session'

export const useSessionStore = defineStore('session', () => {
    const list = ref<ChatSession[]>([])

    async function fetchList(kbId: string) {
        list.value = await getSessionList(kbId)
    }

    async function create(kbId: string, title?: string) {
        const session = await createSessionApi(kbId, title)
        list.value.unshift(session)   // 新会话放前面
        return session
    }

    async function remove(kbId: string, sessionId: string) {
        await deleteSessionApi(kbId, sessionId)
        list.value = list.value.filter((s) => s.id !== sessionId)
    }

    return { list, fetchList, create, remove }
})
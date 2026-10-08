import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getKbList } from '@/api/kb'
import { createKb as createKbApi } from '@/api/kb'

export const useKbStore = defineStore('kb', () => {
    const list = ref<{ id: string; name: string }[]>([])

    async function fetchList() {
        const res = await getKbList()
        list.value = res as unknown as { id: string; name: string }[]
    }

    async function createKb(data: { name: string }) {
        //发给后端，让后端真正创建
        await createKbApi(data)
        await fetchList()
    }

    return { list, fetchList, createKb }
})
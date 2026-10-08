import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getDocList, uploadDoc, deleteDoc, type Doc } from '@/api/doc'

export const useDocStore = defineStore('doc', () => {
    const list = ref<Doc[]>([])
    const loading = ref(false)

    // 拉取某知识库的文档
    async function fetchList(kbId: string) {
        loading.value = true
        try {
            list.value = await getDocList(kbId)
        } finally {
            loading.value = false
        }
    }

    // 上传文档
    async function upload(kbId: string, file: File) {
        await uploadDoc(kbId, file)
        await fetchList(kbId)   // 上传后刷新
    }

    // 删除文档
    async function remove(kbId: string, docId: string) {
        await deleteDoc(kbId, docId)
        await fetchList(kbId)
    }

    return { list, loading, fetchList, upload, remove }
})
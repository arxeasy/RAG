<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useChatStore } from '@/stores/chat'
import { useDocStore } from '@/stores/doc'

const chatStore = useChatStore()
const docStore = useDocStore()
const { list: docs } = storeToRefs(docStore)

// 辅助函数：字节数转可读大小
function formatSize(bytes: number): string {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
    return (bytes / 1024 / 1024).toFixed(1) + ' MB'
}

// 进入知识库时拉取文档
onMounted(() => {
    if (chatStore.currentKbId) {
        docStore.fetchList(chatStore.currentKbId)
    }
})

// 切换知识库时重新拉取
watch(
    () => chatStore.currentKbId,
    (kbId) => {
        if (kbId) docStore.fetchList(kbId)
    }
)

// 上传
function handleUpload() {
    const input = document.createElement('input')
    input.type = 'file'
    input.onchange = async (e) => {
        const file = (e.target as HTMLInputElement).files?.[0]
        if (!file || !chatStore.currentKbId) return
        await docStore.upload(chatStore.currentKbId, file)
    }
    input.click()
}

// 进入对话
function handleEnterChat() {
    chatStore.enterChat()
}
</script>

<template>
    <div class="kb-detail">
        <div v-if="!chatStore.currentKbId" class="empty">
            <div class="empty-title">请选择一个知识库</div>
        </div>

        <template v-else>
            <header class="kb-header">
                <h2>{{ chatStore.currentKbName }}</h2>
            </header>

            <div class="doc-list">
                <div v-if="docStore.loading" class="loading">加载中...</div>

                <div v-else-if="docs.length === 0" class="empty-docs">
                    还没有文件，点击右下角上传
                </div>

                <div v-else v-for="doc in docs" :key="doc.id" class="doc-item">
                    <span class="doc-name">📄 {{ doc.filename }}</span>
                    <span class="doc-size">{{ formatSize(doc.size) }}</span>
                    <span class="doc-status">{{ doc.status }}</span>
                </div>
            </div>

            <button class="capsule" @click="handleEnterChat">
                <span>开始对话</span>
                <span class="capsule-plus" @click.stop="handleUpload">＋</span>
            </button>
        </template>
    </div>
</template>

<style scoped>
.kb-detail {
    position: relative;
    /* 让胶囊绝对定位 */
    height: 100%;
    padding: 24px;
    overflow-y: auto;
}

.kb-header h2 {
    margin: 0 0 24px;
    font-size: 20px;
}

.doc-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 16px;
    border-radius: 12px;
    background: #f9f9f9;
    margin-bottom: 8px;
}

/* 右下角胶囊 */
.capsule {
    position: absolute;
    right: 24px;
    bottom: 24px;

    display: flex;
    align-items: center;
    gap: 12px;

    padding: 8px 8px 8px 20px;
    border: 1px solid #e5e5e5;
    border-radius: 999px;
    background: #ffffff;

    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
    transition: all 0.2s ease;
}

.capsule:hover {
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.capsule-text {
    font-size: 14px;
    color: #1a1a1a;
}

/* 圆形 + 号 */
.capsule-plus {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #1a73e8;
    color: #ffffff;
    font-size: 18px;

    cursor: pointer;
    transition: background 0.15s ease;
}

.capsule-plus:hover {
    background: #1557b0;
}
</style>
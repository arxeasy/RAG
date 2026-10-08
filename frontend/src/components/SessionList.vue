<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { storeToRefs } from 'pinia'
import { useChatStore } from '@/stores/chat'
import { useSessionStore } from '@/stores/session'

const chatStore = useChatStore()
const sessionStore = useSessionStore()
const { list: sessions } = storeToRefs(sessionStore)

// 通知父组件：用户选中了某个会话
const emit = defineEmits<{
    (e: 'select', id: string): void
}>()

onMounted(() => {
    if (chatStore.currentKbId) {
        sessionStore.fetchList(chatStore.currentKbId)
    }
})

watch(
    () => chatStore.currentKbId,
    (kbId) => {
        if (kbId) sessionStore.fetchList(kbId)
    }
)

// 新建会话
async function handleCreate() {
    if (!chatStore.currentKbId) return
    const session = await sessionStore.create(chatStore.currentKbId)
    // 创建后自动选中
    if (session) {
        chatStore.currentSessionId = session.id
        emit('select', session.id)
    }
}

// 点击会话
function handleSelect(id: string) {
    chatStore.currentSessionId = id
    emit('select', id)
}
</script>

<template>
    <div class="session-list-wrapper">
        <button class="new-chat" :disabled="!chatStore.currentKbId" @click="handleCreate">
            + 新对话
        </button>

        <nav class="session-items">
            <div v-for="s in sessions" :key="s.id" class="session-item"
                :class="{ active: s.id === chatStore.currentSessionId }" @click="handleSelect(s.id)">
                {{ s.title }}
            </div>
        </nav>
    </div>
</template>

<style scoped>
.new-chat {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    /* 图标和文字的间距 */

    width: 100%;
    /* 撑满侧栏宽度 */
    padding: 10px 16px;

    font-size: 14px;
    color: #1a1a1a;

    background: #ffffff;
    /* 白底 */
    border: 1px solid #e5e5e5;
    /* 细边框 */
    border-radius: 999px;
    /* 胶囊形，关键 */

    cursor: pointer;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    transition: all 0.2s ease;
}

.session-items {
    padding: 12px 0px 8px 0px;
}

.session-item {
    display: flex;
    align-items: center;
    justify-content: space-between;

    padding: 10px 12px;
    border-radius: 12px;
    /* 圆角关键 */
    cursor: pointer;

    font-size: 14px;
    color: #1a1a1a;
    background: transparent;

    transition: background 0.15s ease, color 0.15s ease;

    border-radius: 8px;

}

.session-item.active {
    background: #e8f0fe;
    color: #1a73e8;
}

.session-item:hover {
    background: #f0f0f0;
}

.new-chat:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);

}
</style>
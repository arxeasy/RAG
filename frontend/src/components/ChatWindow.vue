<script setup lang="ts">
import { onMounted, watch, nextTick, ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useChatStore } from '@/stores/chat'
import { useMessageStore } from '@/stores/message'
import MessageInput from './MessageInput.vue'

const chatStore = useChatStore()
const messageStore = useMessageStore()
const { list: messages, sending } = storeToRefs(messageStore)

const listRef = ref<HTMLElement | null>(null)

// 加载历史消息
async function loadHistory() {
    if (!chatStore.currentKbId || !chatStore.currentSessionId) return
    await messageStore.fetchList(
        chatStore.currentKbId,
        chatStore.currentSessionId,
    )
    scrollToBottom()
}

// 切换会话时重新加载
onMounted(() => {
    if (chatStore.currentSessionId) loadHistory()
})

watch(
    () => chatStore.currentSessionId,
    (id) => {
        if (id) loadHistory()
    },
)

// 接收 MessageInput 的事件
async function handleSend(text: string, useKb: boolean) {
    if (!chatStore.currentKbId || !chatStore.currentSessionId) return

    await messageStore.send(
        chatStore.currentKbId,
        chatStore.currentSessionId,
        text,
        useKb,
    )

    scrollToBottom()
}

// 滚动到底部
function scrollToBottom() {
    nextTick(() => {
        listRef.value?.scrollTo({
            top: listRef.value.scrollHeight,
            behavior: 'smooth',
        })
    })
}
</script>

<template>
    <div class="chat-window">
        <!-- 未选知识库 -->
        <div v-if="!chatStore.currentKbId" class="empty">
            请选择一个知识库
        </div>

        <!-- 已选知识库，未选会话 -->
        <div v-else-if="!chatStore.currentSessionId" class="empty">
            请选择或新建一个对话
        </div>

        <!-- 已选会话：显示聊天 -->
        <template v-else>
            <div ref="listRef" class="message-list">
                <div v-for="msg in messages" :key="msg.id" class="message-item" :class="msg.role">
                    <div class="bubble">
                        {{ msg.content }}
                    </div>
                </div>

                <!-- 加载中 -->
                <div v-if="sending" class="message-item assistant">
                    <div class="bubble loading">思考中...</div>
                </div>
            </div>

            <div class="message-input">
                <MessageInput @send="handleSend" />
            </div>
        </template>
    </div>
</template>

<style scoped>
.chat-window {
    display: flex;
    flex-direction: column;
    height: 100%;
    overflow: hidden;
}

.empty {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #b0b0b0;
    font-size: 16px;
}

.message-list {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.message-item {
    display: flex;
}

.message-item.user {
    justify-content: flex-end;
}

.message-item.assistant {
    justify-content: flex-start;
}

.bubble {
    max-width: 70%;
    padding: 12px 16px;
    border-radius: 12px;
    line-height: 1.6;
    font-size: 15px;
    white-space: pre-wrap;
    word-break: break-word;
}

.message-item.user .bubble {
    background: #eff6ff;
    color: #1a1a1a;
}

.message-item.assistant .bubble {
    background: #f7f7f8;
    color: #1a1a1a;
}

.bubble.loading {
    color: #999;
    font-style: italic;
}

.message-input {
    flex-shrink: 0;
    display: flex;
    justify-content: center;
    padding: 16px 24px;
}

.message-input>* {
    width: 100%;
    max-width: 800px;
}
</style>

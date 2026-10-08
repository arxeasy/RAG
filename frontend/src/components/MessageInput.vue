<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
    (e: 'send', text: string, useKb: boolean): void
}>()

const text = ref('')
const useKb = ref(true)

function toggleKb() {
    useKb.value = !useKb.value
}

function handleSend() {
    const content = text.value.trim()
    if (!content) return
    emit('send', content, useKb.value)
    text.value = ''
}

function handleKeydown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault()
        handleSend()
    }
}
</script>

<template>
    <div class="input-wrapper">
        <textarea v-model="text" class="input-textarea" placeholder="发送消息" rows="1"
            @keydown="handleKeydown" />

        <div class="input-toolbar">
            <!-- 左下：链接知识库切换 -->
            <button class="kb-toggle" :class="{ active: useKb }" @click="toggleKb">
                <span class="icon">🔗</span>
                <span>链接知识库</span>
            </button>

            <!-- 右下：附件 + 发送 -->
            <div class="actions">
                <button class="icon-btn">📎</button>
                <button class="send-btn" @click="handleSend">↑</button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.input-wrapper {
    display: flex;
    flex-direction: column;
    width: 70%;
    border: 1px solid #e5e5e5;
    border-radius: 24px;
    background: #ffffff;
    padding: 12px 16px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

/* 文本域 */
.input-textarea {
    width: 100%;
    min-height: 48px;
    max-height: 200px;
    border: none;
    outline: none;
    resize: none;

    font-size: 15px;
    line-height: 1.6;
    color: #1a1a1a;
    background: transparent;
}

.input-textarea::placeholder {
    color: #a0a0a0;
}

/* 底部工具栏 */
.input-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 8px;
}

/* 左下：链接知识库 */
.kb-toggle {
    display: flex;
    align-items: center;
    gap: 6px;

    padding: 6px 12px;
    font-size: 13px;
    color: #1a1a1a;

    background: #f7f7f8;
    border: 1px solid #e5e5e5;
    border-radius: 999px;
    cursor: pointer;
    transition: all 0.15s ease;
}

.kb-toggle:hover {
    background: #efefef;
}

/* 开启状态 */
.kb-toggle.active {
    background: #e8f0fe;
    color: #1a73e8;
    border-color: #c2d7fb;
}

/* 右下动作区 */
.actions {
    display: flex;
    align-items: center;
    gap: 8px;
}

.icon-btn {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 32px;
    height: 32px;
    border: none;
    border-radius: 50%;
    background: transparent;
    cursor: pointer;
    font-size: 16px;
    color: #555;
}

.icon-btn:hover {
    background: #f0f0f0;
}

/* 发送按钮 */
.send-btn {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 32px;
    height: 32px;
    border: none;
    border-radius: 50%;

    background: #d4d4d4;
    /* 默认灰色（未输入） */
    color: #ffffff;
    font-size: 16px;
    cursor: pointer;
    transition: background 0.15s ease;
}

.send-btn:hover {
    background: #bfbfbf;
}

/* 有内容时变蓝（可配合 :disabled 逻辑） */
.input-wrapper:focus-within .send-btn {
    background: #1a73e8;
}
</style>
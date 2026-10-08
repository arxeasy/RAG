<script setup lang="ts">
import { computed } from 'vue'
import { useChatStore } from '@/stores/chat'
import KbList from '@/components/KbList.vue'
import SessionList from '@/components/SessionList.vue'

defineProps<{ collapsed: boolean }>()
const emit = defineEmits<{ (e: 'toggle'): void }>()

const chatStore = useChatStore()

// 标题：根据 sidebarMode 计算
const headerTitle = computed(() =>
  chatStore.sidebarMode === 'kb-list' ? '知识库' : chatStore.currentKbName
)

// 点击知识库：只记录当前知识库，不切侧栏
function handleSelectKb(id: string, name: string) {
  chatStore.selectKb(id, name)
}

function handleSelectSession(id: string) {
  chatStore.currentSessionId = id
}

// 返回知识库列表
function goBack() {
  chatStore.goBackToKbList()
}
</script>

<template>
  <div class="sidebar">
    <header class="sidebar-header">
      <!-- 返回按钮：只有会话模式才显示 -->
      <button class="btuo" v-if="chatStore.sidebarMode === 'sessions' && !collapsed" @click="goBack">
        ←
      </button>

      <span class="title" v-show="!collapsed">{{ headerTitle }}</span>

      <button class="btus" @click="emit('toggle')">=</button>
    </header>

    <div class="sidebar-body" v-show="!collapsed">
      <Transition name="slide" mode="out-in">
        <KbList v-if="chatStore.sidebarMode === 'kb-list'" key="kb" @select="handleSelectKb" />
        <SessionList v-else key="session" @select="handleSelectSession" />
      </Transition>
    </div>

    <footer class="sidebar-footer">
      <div class="user-info" v-show="!collapsed">
        <img class="avatar" />
        <span class="username">用户名</span>
      </div>
    </footer>
  </div>
</template>


<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  width: 100%;
  /* ← 撑满父容器 <aside>，不再自己定宽 */
  height: 100%;
  background: #f9f9f9;
  overflow: hidden;
  /* ← 收起时内容不溢出 */
  padding: 16px 12px;
  box-sizing: border-box;
  --dsw-alias-brand-primary: #0aa24e;
}

.sidebar-header {
  display: flex;
  flex-shrink: 0;
  width: 100%;
  padding: 4px;
  justify-content: space-between;
  align-items: center;
}

.sidebar-body {
  flex: 1;
  width: 100%;
  margin: 16px 0;
  /* ← 去掉左右 margin，避免撑破 */
  overflow: hidden;
  position: relative;
  padding: 4px;
}

.sidebar-footer {
  flex-shrink: 0;
  padding: 12px;
}

.btus {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  border: none;
  border-radius: 999px;
  background: transparent;
  cursor: pointer;
}

.btus:hover {
  background: #e9e9e9;
  transition: all 0.2s ease;
}

.btuo {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #1a1a1a;
  background: #ffffff;
  border: 1px solid #e5e5e5;
  border-radius: 999px;
  cursor: pointer;
  padding: 4px 10px;
  transition: all 0.2s ease;
}

.btuo:hover {
  background: #f5f5f5;
}

/* 过渡动画 */
.slide-enter-active {
  transition: transform 0.35s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.slide-leave-active {
  transition: transform 0.3s cubic-bezier(0.4, 0, 1, 1);
}

.slide-enter-from {
  transform: translateX(100%);
}

.slide-leave-to {
  transform: translateX(-100%);
}
</style>

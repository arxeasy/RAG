<script setup lang="ts">
import Sidebar from '@/components/Sidebar.vue';
import ChatWindow from '@/components/ChatWindow.vue';
import { ref } from 'vue';
import { useChatStore } from '@/stores/chat'
import KbDetail from '@/components/KbDetail.vue'


const chatStore = useChatStore()
const isCollapsed = ref(false)

function toggleSidebar() {
  isCollapsed.value = !isCollapsed.value
}
</script>

<template>
  <div class="container">
    <aside :class="{ collapsed: isCollapsed }">
      <Sidebar :collapsed="isCollapsed" @toggle="toggleSidebar" />
    </aside>
    <main>
      <Transition name="fade" mode="out-in">
        <KbDetail v-if="chatStore.mainMode === 'kb-detail'" key="detail" />
        <ChatWindow v-else key="chat" />
      </Transition>
    </main>
  </div>
</template>

<style>
.container {
  display: flex;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.container>aside {
  flex-shrink: 0;
  width: 260px;
  height: 100%;
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.container>aside.collapsed {
  width: 60px;
}

.container>main {
  flex: 1;
  min-width: 0;
}
</style>

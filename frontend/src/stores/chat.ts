import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useChatStore = defineStore('chat', () => {
  // 侧栏模式：知识库列表 / 会话列表
  const sidebarMode = ref<'kb-list' | 'sessions'>('kb-list')

  // 右侧主区模式：知识库详情 / 对话
  const mainMode = ref<'kb-detail' | 'chat'>('kb-detail')

  // 当前知识库
  const currentKbId = ref<string | null>(null)
  const currentKbName = ref('')

  // 当前会话
  const currentSessionId = ref<string | null>(null)

  // 点击知识库：右侧显示详情，侧栏保持知识库列表
  function selectKb(id: string, name: string) {
    currentKbId.value = id
    currentKbName.value = name
    mainMode.value = 'kb-detail'
    // sidebarMode 保持 'kb-list'
  }

  // 点击胶囊：进入对话
  function enterChat() {
    mainMode.value = 'chat'
    sidebarMode.value = 'sessions'   // 侧栏切换到会话列表
  }

  // 返回知识库列表
  function goBackToKbList() {
    sidebarMode.value = 'kb-list'
    mainMode.value = 'kb-detail'
    currentKbId.value = null
    currentKbName.value = ''
    currentSessionId.value = null
  }

  return {
    sidebarMode,
    mainMode,
    currentKbId,
    currentKbName,
    currentSessionId,
    selectKb,
    enterChat,
    goBackToKbList,
  }
})
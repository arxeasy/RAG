<script setup lang="ts">
import { useKbStore } from '@/stores/kb';
import { onMounted, ref } from 'vue';
import { storeToRefs } from 'pinia'

const emit = defineEmits<{
    (e: 'select', id: string, name: string): void
}>()

const kbStore = useKbStore()
const { list: kbs } = storeToRefs(kbStore)
// 控制弹窗显示
const showDialog = ref(false)
const newKbName = ref('')

function handleAddKb() {
    showDialog.value = true
}

async function confirmAddKb() {
    showDialog.value = false
    if (!newKbName.value.trim()) return
    await kbStore.createKb({ name: newKbName.value })
    newKbName.value = ''
 
}

onMounted(() => {
    kbStore.fetchList()
})

</script>

<template>
    <div class="kb-list-wrapper">
        <button class="new-kb" @click="handleAddKb">+ 添加知识库</button>
        <div v-if="showDialog" class="dialog">
            <input v-model="newKbName" placeholder="输入知识库名称" />
            <button @click="confirmAddKb">确定</button>
            <button @click="showDialog = false">取消</button>
        </div>
        <nav class="kb-list">
            <div v-for="kb in kbs" :key="kb.id" class="kb-item" @click="emit('select', kb.id, kb.name)">
                {{ kb.name }}
            </div>
        </nav>

    </div>
</template>

<style scoped>
.kb-list {
    padding: 12px 0px 8px 0px;
}

.kb-item {
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

.kb-item.active {
    background: #e8f0fe;
    color: #1a73e8;
}

.kb-item:hover {
    background: #f0f0f0;
}

.new-kb {
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

.new-kb:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);

}
</style>
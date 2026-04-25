import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useKnowledgeStore = defineStore('knowledge', () => {
  // State
  const documents = ref<string[]>([])
  const lastUploadTime = ref<Date | null>(null)
  const isProcessing = ref(false)

  // Actions
  function addDocument(filename: string) {
    documents.value.push(filename)
    lastUploadTime.value = new Date()
  }

  function removeDocument(filename: string) {
    const index = documents.value.indexOf(filename)
    if (index > -1) {
      documents.value.splice(index, 1)
    }
  }

  function setProcessing(status: boolean) {
    isProcessing.value = status
  }

  function clearDocuments() {
    documents.value = []
    lastUploadTime.value = null
  }

  return {
    documents,
    lastUploadTime,
    isProcessing,
    addDocument,
    removeDocument,
    setProcessing,
    clearDocuments,
  }
})

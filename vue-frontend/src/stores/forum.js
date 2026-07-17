import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getTopicList, getTopicDetail, createTopic, getPosts, createPost } from '@/api/forum'

export const useForumStore = defineStore('forum', () => {
  const topics = ref([])
  const currentTopic = ref(null)
  const posts = ref([])
  const loading = ref(false)

  const fetchTopics = async () => {
    loading.value = true
    try {
      const res = await getTopicList()
      topics.value = res.data.results || res.data
    } finally {
      loading.value = false
    }
  }

  const fetchTopicDetail = async (id) => {
    loading.value = true
    try {
      const res = await getTopicDetail(id)
      currentTopic.value = res.data
    } finally {
      loading.value = false
    }
  }

  const fetchPosts = async (topicId) => {
    loading.value = true
    try {
      const res = await getPosts(topicId)
      posts.value = res.data.results || res.data
    } finally {
      loading.value = false
    }
  }

  const handleCreateTopic = async (data) => {
    const res = await createTopic(data)
    await fetchTopics()
    return res.data
  }

  const handleCreatePost = async (topicId, data) => {
    const res = await createPost(topicId, data)
    await fetchPosts(topicId)
    return res.data
  }

  return {
    topics,
    currentTopic,
    posts,
    loading,
    fetchTopics,
    fetchTopicDetail,
    fetchPosts,
    handleCreateTopic,
    handleCreatePost
  }
})

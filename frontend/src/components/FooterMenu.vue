<script setup>
import { Search, Heart, FileText, MessageCircle, User } from 'lucide-vue-next'
</script>

<template>
  <div class="footer-menu">
    <div class="tabbar-items">
      <button class="tabbar-button">
        <Search :size="24" />
        <span class="tabbar-title">Поиск</span>
      </button>
      <button class="tabbar-button">
        <Heart :size="24" />
        <span class="tabbar-title">Избранное</span>
      </button>
      <button class="tabbar-button">
        <FileText :size="24" />
        <span class="tabbar-title">Объявления</span>
      </button>
      <button class="tabbar-button">
        <MessageCircle :size="24" />
        <span class="tabbar-title">Сообщения</span>
      </button>
      <button class="tabbar-button">
        <User :size="24" />
        <span class="tabbar-title">Профиль</span>
      </button>
    </div>
  </div>
</template>

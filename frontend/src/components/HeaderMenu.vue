<script setup>
import { Home, SlidersHorizontal, ShoppingCart } from 'lucide-vue-next'
</script>

<template>
  <div class="header-menu">
    <div class="search-box">
      <Home :size="24" />
      <input type="text" placeholder="Поиск" class="search-input" />
      <SlidersHorizontal :size="24" />
    </div>
  </div>
</template>

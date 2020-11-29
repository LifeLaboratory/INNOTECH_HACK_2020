<template>
  <a-layout id="components-layout-demo-top" class="layout">
    <a-layout-header>
      <a-menu
        theme="dark"
        mode="horizontal"
        :style="{ lineHeight: '64px' }"
      >
        <a-menu-item key="1" @click="goTo('/photo')">
          Поиск по фотографии
        </a-menu-item>
        <a-menu-item key="2" @click="goTo('/url')">
          Добавление по URL
        </a-menu-item>
      </a-menu>
    </a-layout-header>
    <a-layout-content style="padding: 0 50px">
      <div :style="{ background: '#fff', padding: '24px', minHeight: '100vh' }">
        <router-view />
      </div>
    </a-layout-content>
  </a-layout>
</template>
<script>
export default {
  methods: {
    goTo(link) {
      this.$router.push({path: link})
    }
  }
}
</script>
<style>
#components-layout-demo-top .logo {
  width: 120px;
  height: 31px;
  background: rgba(255, 255, 255, 0.2);
  margin: 16px 24px 16px 0;
  float: left;
}
</style>
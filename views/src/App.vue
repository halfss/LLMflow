<script setup lang="ts">
import { NConfigProvider } from 'naive-ui'
import { NaiveProvider } from '@/components/common'
import { useTheme } from '@/hooks/useTheme'
import { useLanguage } from '@/hooks/useLanguage'

const { theme, themeOverrides } = useTheme()
const { language } = useLanguage()
</script>

<template>
  <div class="local-mind-bg" />
  <NConfigProvider
    class="h-full"
    :theme="theme"
    :theme-overrides="themeOverrides"
    :locale="language"
  >
    <NaiveProvider>
      <RouterView />
    </NaiveProvider>
  </NConfigProvider>
</template>

<style>
#app{
  overflow: hidden;
}
.local-mind-bg{
  width: 100%;
  height: 100%;
  background-image: url(./assets/bg12.jpeg);
  filter: blur(40px);
  z-index: 1;
  transform: scale(1.2)
}
.n-config-provider {
  width: 100%;
  position: absolute;
  z-index: 2;
  top: 0;
  left: 0;
}
.footer-style{
  background-color: rgba(0, 0, 0, 0.8);
  color: #fff;
}
#app .n-radio-group .n-radio-button{
  color: #fff;
}
#app .n-radio-group .n-radio-button.n-radio-button--checked{
  color: rgb(180 187 196);
}
.session-style{
  color: #fff !important;
}
.n-button{
  color: #fff !important;
}
.padding0{
  padding: 0 !important;
}
.padding1{
  padding: 1rem;
}
.scrollbar{
  scrollbar-width:none;
  -ms-overflow-style:none;
}
.scrollbar::-webkit-scrollbar{display:none}
</style>

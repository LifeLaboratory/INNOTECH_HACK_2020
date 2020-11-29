<template>
  <div class="about">
    Введите ссылку на страницу профиля VK
     <a-input placeholder="" v-model="link" style="margin-left: 50px; margin-rigth: 50px; margin-top: 20px; margin-bottom: 20px"/>
     <a-button type="primary" @click="sendLink">
      Поиск
    </a-button>
    <div class="marigin"></div>
    <div v-if="responseStatus === true">
        Ссылка принята в обработку, обработка в течение минуты
    </div>
    <div v-if="responseStatus === false" class="errorMessage">
        Ошибка 
    </div>
  </div>
</template>
<script>
import axios from "axios"
export default {
    data() {
        return {
            link: '', 
            responseStatus: null
        }
    },
    methods: {
        sendLink() {
            axios.post("http://46.148.224.125:5000/api/add_organization", {
                vk_link: this.link
            })
            .then( () => {
                this.responseStatus=true
            }
            )
            .catch( () => {
                this.responseStatus=false
            }
            )
        }
    }
}
</script>

<style scoped>
.errorMessage{
    color: red;
}
.marigin{
    margin-top: 15px;
}
</style>

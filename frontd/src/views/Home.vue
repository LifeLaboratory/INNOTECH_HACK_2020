<template>
  <div>
    <a-upload-dragger
      name="image"
      :multiple="true"
      action="http://46.148.224.125:5000/api/upload_image"
      @change="handleChange"
    >
      <p class="ant-upload-drag-icon">
        <a-icon type="inbox" />
      </p>
      <p class="ant-upload-text">
        Нажимите или перетащите файл с рабочего стола
      </p>
    </a-upload-dragger>
    <div v-if="status">
       <div class="leftAlign">
         <div> {{response.surname}} {{response.name}} {{response.patronymic}} </div>
         <div> Национальность: {{response.nationality}} </div>
         <div> Страна: {{response.country}} </div>
         <div> ИНН: {{response.inn}} </div> 
         <div> ВК: {{response.link_vk}} </div>
         <div> Пол: <span v-if="response.sex == 2">Муж.</span> <span v-if="response.sex == 1">Жен.</span>  </div>
         <div> Телефон: {{response.phone}} </div>
         <div> Дата рождения: {{response.bday}} </div>
         <div> Сайт: {{response.site}} </div>
         <div> Город: {{response.city}} </div>
         <div v-for="(el, key) in response.organizations" :key=key>
            <div>Организация:{{el.organization_name}}</div>
            <div>Ссылка на оргицизацию {{el.organization_url}}</div>
            <div>Статус организации: {{el.organization_status}}</div>
            <div>Владелец организации: {{el.organization_leader}}</div>
            <div>Дата регистрации организации: {{el.organization_date_reg}}</div>
            <div>ИНН организации: {{el.organization_inn}}</div>
            <div>Идентификатор клиента: {{el.client_id}}</div>
            <div>Статус клиента: {{el.status_client}}</div>
         </div>
         <div v-for="(el, key) in response.interests" :key=key>
          <div>
              Интересы: {{el.interest_name}}
          </div>
         </div>
       </div>
    </div>
  </div>
</template>
<script>
import TableCustom from "@/components/Table"
export default {
  components: {
    TableCustom
  },
  data() {
    return {
      status: false,
      response: {}
    }
  },
  methods: {
    handleChange(info) {
      const status = info.file.status;
      if (status !== 'uploading') {
        console.log(info.file.response)
        this.response = info.file.response
      }
      if (status === 'done') {
        this.$message.success(`${info.file.name} файл успешно загружен.`)
        this.status = true
      } else if (status === 'error') {
        this.$message.error(`${info.file.name} ошибка загруки файла.`)
      }
    },
  },
};
</script>

<style scoped>
.leftAlign {
  text-align: left;
}
</style>
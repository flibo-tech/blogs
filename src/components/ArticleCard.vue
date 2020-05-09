<template>
  <div>
    <v-card class="mx-auto" max-width="350" min-width="350">
      <a :href="url"
        ><v-img
          class="white--text align-end"
          height="200px"
          :src="image"
        >
        </v-img
      ></a>

      <v-card-title>
        <a :href="url">{{ title }}</a>
      </v-card-title>
      <!-- <v-card-subtitle class="pb-0">Number 10</v-card-subtitle> -->

      <v-card-text class="text--primary">
        <div>
          {{ description }}
        </div>
      </v-card-text>

      <v-card-actions>
        <v-btn text color="primary" :to="url">
          Read
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "ArticleCard",
  props: ["title", "image", "description", "url"]
};
</script>

<style lang="scss" scoped>
a {
  text-decoration: none;
  color: #212121 !important;
}
</style>

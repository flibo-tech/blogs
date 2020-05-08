<template>
  <div class="home">
    <v-container class="fill-height">
      <v-row>
        <v-col>
          <!-- FEATURED ARTICLES -->
          <div class="featured-slider">
            <v-carousel
              cycle
              height="500"
              hide-delimiter-background
              show-arrows-on-hover
            >
              <v-carousel-item
                v-for="(slide, i) in featured"
                :key="i"
                :src="require(`../assets/images/${slide.image}`)"
              >
                <div class="featured-slider-content">
                  <div class="featured">
                    <span>FEATURED {{country}}</span>
                    <p>{{ slide.title }}</p>
                  </div>
                </div>
              </v-carousel-item>
            </v-carousel>
          </div>

          <!-- == -->
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Home",
  components: {},
  data: function() {
    return {
      country: null,
      featured: [
        {
          title:
            "Top 10 awesome shows like Young Sheldon that you will enjoy watching",
          image: "young-sheldon.jpg"
        },
        {
          title:
            "Top 10 awesome shows like The Office that you will enjoy watching",
          image: "the-office.jpg"
        },
        {
          title: "Panchayat",
          image: "panchayat.jpg"
        }
      ]
    };
  },
  created() {
    var self = this;
    axios
        .get('https://ipinfo.io/?token=a354c067e1fef5')
        .then(function(response) {
            if ([200].includes(response.status)) {
              self.country = response.data.country;
              document.dispatchEvent(new Event("x-app-rendered"));
            }
        });
  }
};
</script>

<style lang="scss" scoped>
.featured-slider-content {
  position: relative;
  width: 100%;
  height: 100%;
  background-image: url(../assets/images/gradient.png);
  background-position: bottom;
  background-repeat: repeat-x;
}
.featured {
  position: absolute;
  bottom: 10px;
  color: #ffffff;
  padding: 2rem 4rem;
}
.featured span {
  font-size: 1rem;
}
.featured p {
  font-size: 3rem;
  line-height: 120%;
}

.featured-slider {
  border-radius: 21px;
  overflow: hidden;
}
</style>

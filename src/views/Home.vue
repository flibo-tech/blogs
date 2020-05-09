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
                :src="slide.image.replace('/w500/', '/w1280/')"
                :to="((slide.type=='movie') ? 'movies' : 'shows')+'-like-'+slide.title.replace(/[^a-z0-9]+/gi,'-').toLowerCase()"
              >
                <div class="featured-slider-content">
                  <div class="featured">
                    <span>FEATURED {{country}}</span>
                    <p>{{ ((slide.type=='movie') ? 'Movies' : 'Shows')+' like '+slide.title }}</p>
                  </div>
                </div>
              </v-carousel-item>
            </v-carousel>
          </div>

          <!-- == -->
        </v-col>
      </v-row>
      <!-- == ARTICLES -->
      <v-row>
        <v-col>
          <h2>Articles</h2>
          <v-row>
            <v-col v-for="article in articles" :key="article.id">
              <ArticleCard
                :title="article.title"
                :description="'Top '+article.similar_content_count+' awesome '+((article.type=='movie') ? 'movies' : 'shows')+' like '+article.title+' that you will enjoy watching'"
                :image="article.image"
                :url="((article.type=='movie') ? 'movies' : 'shows')+'-like-'+article.title.replace(/[^a-z0-9]+/gi,'-').toLowerCase()"
              />
            </v-col>
          </v-row>
        </v-col>
      </v-row>
      <div class="articles-contaier"></div>

      <!--  -->
    </v-container>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue";
import ArticleCard from "@/components/ArticleCard";
import axios from "axios";

export default {
  name: "Home",
  components: {
    ArticleCard
  },
  data: function() {
    return {
      country: null,
      featured: [],
      articles: [],
      min_popularity: null,
      fetching_incremental: false,
      api_host: 'https://yzal-dev-app.flibo.ai/'
    };
  },
  created() {
    var self = this;

    axios
        .post(self.api_host + 'blogs_contents', {
                popularity: null
            })
        .then(function(response) {
            if (response.status==200) {
                self.featured = response.data.blogs.slice(0,3);
                self.articles = response.data.blogs.slice(3,);
                self.min_popularity = response.data.min_popularity;
                document.dispatchEvent(new Event("x-app-rendered"));
            }
          });

    axios
        .get('https://ipinfo.io/?token=a354c067e1fef5')
        .then(function(response) {
            if ([200].includes(response.status)) {
              self.country = response.data.country;
            }
        });
  },
  mounted () {
      window.addEventListener('scroll', this.watchScroll)
  },
  methods: {
    watchScroll() {
        var self = this;
        var scroll_completion = window.scrollY/(document.documentElement.scrollHeight-document.documentElement.clientHeight);
        if (document.documentElement.scrollHeight == document.documentElement.clientHeight) {
            scroll_completion = 1
        };
        if ((scroll_completion > 0.8)
            &&
            (!self.fetching_incremental)
            &&
            (self.articles.length < 20000)) {
              self.fetching_incremental = true;
              axios
                .post(self.api_host + 'blogs_contents', {
                        popularity: self.min_popularity
                    })
                .then(function(response) {
                    if (response.status==200) {
                        self.articles.push(...response.data.blogs);
                        self.min_popularity = response.data.min_popularity;
                        self.fetching_incremental = false;
                    }
                  })
                .catch(function(error) {
                  self.fetching_incremental = false;
                });
        }
    }
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

<template>
  <div class="home">
    <v-container class="fill-height">
      <v-row>
        <v-col>
          <!-- FEATURED ARTICLES -->
          <div class="featured-slider">
            <v-carousel
              height="500"
              hide-delimiter-background
              show-arrows-on-hover
            >
              <v-carousel-item
                v-for="(slide, i) in featured"
                :key="i"
                :src="slide.image.replace('/w500/', '/w780/')"
                @click="
                  openArticle(
                    (slide.type == 'movie' ? 'movies' : 'shows') +
                      '-like-' +
                      slide.title.replace(/[^a-z0-9]+/gi, '-').toLowerCase()
                  )
                "
              >
                <div class="featured-slider-content">
                  <div class="featured">
                    <span>FEATURED {{ country }}</span>
                    <p>
                      {{
                        (slide.type == "movie" ? "Movies" : "Shows") + " like "
                      }}
                      <strong>
                        {{ slide.title }}
                      </strong>
                    </p>
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
          <h1 style="font-size: 1.5rem">Discover Movies &amp; TV Shows</h1>
          <v-row>
            <v-col v-for="article in articles" :key="article.id">
              <ArticleCard
                :title="article.title"
                :description="
                  'Top ' +
                  article.similar_content_count +
                  ' awesome ' +
                  (article.type == 'movie' ? 'movies' : 'shows') +
                  ' like ' +
                  article.title +
                  ' that you will enjoy watching'
                "
                :image="article.image"
                :url="
                  (article.type == 'movie' ? 'movies' : 'shows') +
                  '-like-' +
                  article.title.replace(/[^a-z0-9]+/gi, '-').toLowerCase()
                "
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
    ArticleCard,
  },
  metaInfo() {
    return {
      title: "Discover Movies & TV Shows",
      meta: [
        {
          vmid: "description",
          name: "description",
          content:
            "You have so many streaming subscriptions but still cannot decide what to watch? We are here to help you personalize all your streaming apps. Swipe your way through clutter.",
        },
        {
          "http-equiv": "Content-Type",
          content: "text/html; charset=UTF-8",
        },
        {
          vmid: "viewport",
          name: "viewport",
          content: "width=device-width, initial-scale=1",
        },
        {
          vmid: "og:title",
          property: "og:title",
          content: "Discover Movies & TV Shows",
        },
        {
          vmid: "og:description",
          property: "og:description",
          content:
            "You have so many streaming subscriptions but still cannot decide what to watch? We are here to help you personalize all your streaming apps. Swipe your way through clutter.",
        },
        {
          vmid: "og:url",
          property: "og:url",
          content: this.store.blog_host + this.$route.path,
        },
        {
          vmid: "og:type",
          property: "og:type",
          content: "website",
        },
        {
          vmid: "og:image",
          property: "og:image",
          content:
            "https://flibo-images.s3-us-west-2.amazonaws.com/covers/login-cover.jpg",
        },
        {
          vmid: "twitter:card",
          name: "twitter:card",
          content: "summary",
        },
        {
          vmid: "twitter:title",
          name: "twitter:title",
          content: "Discover Movies & TV Shows",
        },
        {
          vmid: "twitter:description",
          name: "twitter:description",
          content:
            "You have so many streaming subscriptions but still cannot decide what to watch? We are here to help you personalize all your streaming apps. Swipe your way through clutter.",
        },
        {
          vmid: "twitter:url",
          name: "twitter:url",
          content: this.store.blog_host + this.$route.path,
        },
        {
          vmid: "twitter:image",
          name: "twitter:image",
          content:
            "https://flibo-images.s3-us-west-2.amazonaws.com/covers/login-cover.jpg",
        },
      ],
    };
  },
  data: function () {
    return {
      country: null,
      featured: [],
      articles: [],
      min_popularity: null,
      fetching: true,
      store: this.$store.state,
    };
  },
  created() {
    var self = this;
    axios
      .post(self.$store.state.api_host + "blogs_contents", {
        popularity: null,
      })
      .then(function (response) {
        if (response.status == 200) {
          self.featured = response.data.blogs.slice(0, 3);
          self.articles = response.data.blogs.slice(3);
          self.min_popularity = response.data.min_popularity;
          self.fetching = false;
          document.dispatchEvent(new Event("x-app-rendered"));
        }
      })
      .catch(function (error) {
        self.fetching = false;
      });
  },
  mounted() {
    window.addEventListener("scroll", this.watchScroll);
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.watchScroll);
  },
  methods: {
    watchScroll() {
      var self = this;
      var scroll_completion =
        window.scrollY /
        (document.documentElement.scrollHeight -
          document.documentElement.clientHeight);
      if (
        document.documentElement.scrollHeight ==
        document.documentElement.clientHeight
      ) {
        scroll_completion = 1;
      }

      if (
        scroll_completion > 0.8 &&
        !self.fetching &&
        self.articles.length < 20000 &&
        self.$route.path == "/"
      ) {
        self.fetching = true;
        axios
          .post(self.$store.state.api_host + "blogs_contents", {
            popularity: self.min_popularity,
          })
          .then(function (response) {
            if (response.status == 200) {
              self.articles.push(...response.data.blogs);
              self.min_popularity = response.data.min_popularity;
              self.fetching = false;
            }
          })
          .catch(function (error) {
            self.fetching = false;
          });
      }
    },
    openArticle(link) {
      window.open(link, "_self");
    },
  },
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
  // color: #212121;
  // padding: 0.2rem 0.5rem;
  // border-radius: 2px;
  // background-color: #f7e5a8;
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

<template>
  <div>
    <v-container class="fill-height">
      <v-row>
        <v-col>
          <v-img
            :src="require(`../assets/images/young-sheldon.jpg`)"
            alt=""
            aspect-ratio="2"
          ></v-img>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <h1>Article Title</h1>
          <p>
            Lorem ipsum, dolor sit amet consectetur adipisicing elit.
            Reprehenderit autem vel laudantium aliquid ea tenetur suscipit modi
            porro! Ipsa sit voluptatem magnam beatae in? Non ipsum at aperiam
            quidem incidunt.
          </p>
          <ol>
            <li>Anger Management</li>
            <li>Anger Management</li>
            <li>Anger Management</li>
            <li>Anger Management</li>
            <li>Anger Management</li>
          </ol>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "Article",
  data: function() {
    return {
      article: {
        title:
          "Top 10 awesome shows like Young Sheldon that you will enjoy watching",
        intro:
          "You just finished watching Young Sheldon and you can’t get over how good this show was. Now you want to watch more of such masterpieces. We have curated a list of similar shows which are created by the likes of Jaffar Mahmood, Iain Armitage and Zoe Perry . Here goes the list -",
        list: [
          {
            id: 1,
            title: "Movie Title",
            image: "young-sheldon.jpg",
            artists: ["Artist 1", "Artist 2"],
            description:
              "Lorem ipsum, dolor sit amet consectetur adipisicing elit.",
            watch: [
              {
                netflix: true,
                url: "netflix-url"
              },
              {
                prime: true,
                url: "prime-url"
              }
            ]
          }
        ]
      }
    };
  }
};
</script>

<style lang="scss" scoped>
ol {
  list-style: none;
  counter-reset: article-counter;
  //   columns: 2;
  //   -webkit-columns: 2;
  //   -moz-columns: 2;
}
ol li {
  position: relative;
  padding-left: 25px;
  counter-increment: article-counter;
  margin: 25px 0;
}
ol li::before {
  display: inline-block;
  content: counter(article-counter);
  position: absolute;
  width: 40px;
  height: 40px;
  text-align: center;
  padding: 1px;
  font-size: 1.6rem;
  font-weight: bold;
  top: -8px;
  left: -25px;
  border-radius: 50%;
  background-color: #e8e8e8;
}
</style>

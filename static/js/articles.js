$(document).ready(function(){

  $.ajax({ method: 'GET',
            url: 'https://newsapi.org/v2/top-headlines?' + 'sources=medical-news-today&' +'apiKey=46efe27f785143e59c8de8bd684a9a06',
          success: function(response){
      for (var i = 0; i < response.articles.length; i++) {
        let author = response.articles[i].author;
        let title = response.articles[i].title;
        let url = response.articles[i].url;
        let published = response.articles[i].publishedAt;
        let content = response.articles[i].content;
        $('.api-container').append(`
        <div class="box article-box is-one-third">
        <article class="media">   
          <div class="media-content">
            <div class="content">         
              <h1 class="title is-3 article-title">${title}</h1>
              <h3 class="author article-author">${author}</h3>
                <h3><a href="${url}">${url}</a></h3>
                <h4 class="time article-time">${published}</h4>
            </div>
            <nav class="level is-mobile">
              <div class="level-left">
                <a class="level-item" aria-label="reply">
                  <span class="icon is-small">
                    <i class="fas fa-reply" aria-hidden="true"></i>
                  </span>
                </a>
                <a class="level-item" aria-label="retweet">
                  <span class="icon is-small">
                    <i class="fas fa-retweet" aria-hidden="true"></i>
                  </span>
                </a>
                <a class="level-item" aria-label="like">
                  <span class="icon is-small">
                    <i class="fas fa-heart" aria-hidden="true"></i>
                  </span>
                </a>
              </div>
            </nav>
          </div>
        </article>
      </div>
        `);
        }      
      }});
  });

 
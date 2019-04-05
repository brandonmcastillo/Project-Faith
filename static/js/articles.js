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
        <div class="columns">
        <div class="column is-two-thirds">
        <h1 class="title">${title}</h1>
        <h3 class="author">${author}</h3>
        <h3><a href="${url}">${url}</a></h3>
        <h4 class="time">${published}</h4>

        </div>
        </div>
        `);
        }      
      }});
  });
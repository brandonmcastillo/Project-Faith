function randomQuote() {
    $.ajax({
        url: "https://api.forismatic.com/api/1.0/?",
        dataType: "jsonp",
        data: "method=getQuote&format=jsonp&lang=en&jsonp=?",
        success: function( response ) {
          $("#quotetag").html("<p id='quotetag' class='text-center'>" +
            '"' + response.quoteText +'"' + "<br/>&dash;" + response.quoteAuthor + "</p>");
        }
    });
  }
  

  
  $(function() {
    randomQuote();
  });
  
  $("button").click(function(){
    randomQuote();
  });
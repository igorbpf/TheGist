$(function() {
    $('button').click(function(event) {
        event.stopImmediatePropagation();
        $("#summary").empty()
        $("#summary").append("<img id='image' src='static/img/loading.gif' alt='loading...'>")
        // $("#summary").append("<img id='image' src='static/img/loading.gif' alt='loading...' width='42' height='42'>")
        $("button").hide();

        // Using promises
        var promised_firstajax = firstajax();
        promised_firstajax.done(function(response){
          var key = response.id;
           var ajaxtime = setInterval(function(){

            $.ajax({
              url: '/_summary/' + key,
              type: "GET",
              success: function(data, textStatus, xhr) {
                if (xhr.status === 202){
                //console.log(data);

              } else {

                //console.log(data);
                $("#image").remove();


                summary = data.summary;

                // $('#content').append('<h3 class="title">' + title + '</h3> <br> <br>');
                // $('html').width(3 * $('#content').width());
                $('#summary').append('<p class="news">' + summary + '</p>');
                $('textarea').val('');
                // $('html').height($('#content').width());
                // console.log(2 * $('#content').width());
                $("button").show();
                clearInterval(ajaxtime);
              }
              },
              error: function(error){
                //console.log(error);
                $('textarea').val('');
                $("#image").remove();
                $('#summary').append('<p class="error-message">No possible to summarize this text now! Sorry! Try again!</p>');
                $('textarea').val('');
                $("button").show();
                clearInterval(ajaxtime);
              }
            });
           }, 1000);

        });
        promised_firstajax.fail(function(error){
          //console.log(error)
        });
    });
});

function firstajax(){

  return $.ajax({
          url: '/_summary',
          data: $('form').serialize(),
          type: 'POST'

        })
}

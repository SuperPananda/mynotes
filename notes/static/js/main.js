$(document).ready(function() {
    $('#contpost').on("click", ".likebutton", function(){
        LikeButton($(this).attr("data_catid"));
    })

    $('#contpost').on("click", ".deletpost", function(){
        DeletePost($(this).attr("data_catid"));
    })

    $(document).on("change", "#sel",function (e){
        e.preventDefault();
        OrderBy($(this).val());
    })

    $(document).on("click", ".date",function (e){
        GetData($(this).attr("id"));
    })

    // $('.date').click(function(){
    //     GetData($(this).attr("id"));
    // })

    $('#izbranoe').click(function(){
        GetFavorite();
    })
    
    $('#formsearch').keyup(function(){
        Search($('#formsearch').val());
    })

    $('#selkat').change(function (e){
        e.preventDefault();
        GetCat($(this).val());
    })

})

function DeletePost(id)
{
    $.ajax( 
            { 
                type:"GET", 
                url: "delpost", 
                data:{ 
                    post_id: id 
                }, 
                success: function(json) 
                { 
                    redrawCard(json);
                    //window.history.pushState(null, null, 'notes/');
                
                } 
            }
        )
}

function Search(t)
{
    $.ajax(
        {
            type: "POST",
            url: '{% url "searchtitle" %}',
            data:
            {
                option:t,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                action: 'post',
            },
            success: function(json)
            {
                redrawCard(json);
                
            },
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        }
    )
}

function GetCat(ter)
{
    $.ajax(
        {
            type: "POST",
            url: '{% url "filtercategor" %}',
            data:
            {
                option:ter,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                action: 'post',
            },
            success: function(json)
            {
                redrawCard(json);
            },
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        }
    )
}

function GetData(id)
{
    $.ajax(
        {
            type: "POST",
            url: '{% url "filterdata" %}',
            data:
            {
                option:id,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                action: 'post',
            },
            success: function(json)
            {
                redrawCard(json);
            },
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        }
    )
}

function OrderBy(ter)
{
   $.ajax(
        {
            type: "POST",
            url: '{% url "search" %}',
            data:{
                option:ter,
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                action: 'post',
            },
            success: function(json)
            {
                redrawCard(json);               
            },
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        }
    )
    
}

function LikeButton(id)
{
    console.log("hello");
    if ($( '#like'+ id ).hasClass('added'))
    {
        $.ajax( 
            { 
                type:"GET", 
                url: "unlike", 
                data:{ 
                    post_id: id 
                }, 
                success: function( data ) 
                { 
                    $( '#like'+ id ).removeClass('btn btn-danger'); 
                    $( '#like'+ id ).removeClass('added');
                    $( '#like'+ id ).addClass('btn btn-outline-primary');
                    $( '#like'+ id ).text('Добавить в избраное'); 
                } 
            }
        )
    }
    else
    {
        $.ajax( 
            { 
                type:"GET", 
                url: "like", 
                data:{ 
                    post_id: id 
                }, 
                success: function( data ) 
                {  
                    $( '#like'+ id ).removeClass('btn btn-outline-primary'); 
                    $( '#like'+ id ).addClass('btn btn-danger');
                    $( '#like'+ id ).addClass('added');
                    $( '#like'+ id ).text('Избраное'); 
                } 
            }
        ) 
    }      
} 

function GetFavorite() {
    $.ajax( 
        { 
            type:"GET", 
            url: "filtration_favorit", 
            success: function( json ) 
            { 
                redrawCard(json);
            }

        }
    )
}

function redrawCard(json)
{
    console.log(json);
    $('.card').remove();  
    for (item in json)
    {
                    console.log(json[item]);
                    console.log(json[item].title);

                    var button_1 = 'post/' + json[item].slug;
                    var class_Like;
                    var id_Like = 'like' + json[item].slug;
                    var id_del = 'del'+ json[item].slug;
                    var data_catid_Like = json[item].slug;

                    var pref = 'https://www.facebook.com/sharer/sharer.php?u=http://127.0.0.1:8000/'+ json.url

                    if (json[item].favorite == true)
                    {
                        class_Like = 'likebutton btn btn-danger added';
                        text_Like = 'Избраное'                       
                    }
                    else
                    {
                        class_Like = 'likebutton btn btn-outline-primary'
                        text_Like = 'Добавить в избраное' 
                    }

                    $('<div>',{
                        class: 'card mb-4',
                        append: $('<h5>',{
                                    class: 'card-header',
                                    text: json[item].date,
                                    
                                 })
                                 .add($('<div>',{
                                     class: 'card-body',
                                     append: $('<h5>', {class: 'card-title', text: json[item].title})
                                        .add($('<p>', {class: 'card-text', text: json[item].body}))
                                        //.add($('<p>', {
                                            //class: 'card-text',
                                            //append: $('<small>', {class: 'text-muted', text: json[item].category})
                                            //}))
                                        .add($('<a>', {class: 'btn btn-primary', text: 'Go somewhere', href: json[item].url}))
                                        .add($('<a>', {class: 'btn btn-primary', text: 'Редактировать', href:  json[item].url_update}))
                                        .add($('<a>', {class: 'deletpost btn btn-danger', id: id_del, data_catid: data_catid_Like, text: 'Удалить' }))
                                        .add($('<br />'))
                                        .add($('<br />'))
                                        .add($('<a>', {class: class_Like, text: text_Like, id: id_Like, data_catid: data_catid_Like}))
                                        .add($('<a>', {class: 'btn btn-outline-primary',target: '_blank',text: 'like', rel: 'nofollow',
                                            onclick: "javascript:window.open(this.href, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=300,width=600');return false;",
                                            href: json[item].url
                                        }))
                                     }))
                                .add($('<div>',{
                                    class: 'card-footer text-muted',
                                    text: json[item].category
                                })) 

                    }).appendTo('#contpost')
    }    
}
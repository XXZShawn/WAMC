$('.active').removeClass('active');
$("#cycle").addClass("active");  
function validation(){
    inputs=document.getElementsByClassName("form-control");
    for (i=0;i<inputs.length;i++){
        if(!inputs[i].value){
            alert("ERROR: YOU NEED TO FILL ALL THE INPUTS");
            return false;
        }
    }
    return true;
};
$(function(){
    result = document.getElementById("cp-count").innerText;
    if (result == ""){
        $("#page").hide();
    };
    $(".col-8").on("click",function(){
        $(this).parent().siblings().slideToggle(); 
    });
    $(".close").on("click",function(){
        $(".modal").hide();
    });
    $(".view").on("click",function(){
        var data = $(this).parent().parent().siblings(".news-body").children("p").text();
        $.ajax({
            url:"/view/",
            type:"POST",
            data:{"cycle":data},  
            success:function (data) { 
                path = data["path"];
                $("#my_image").attr("src", path);
                $(".modal").show();
            } 
        })});
    $("#go").on("click",function(){
        page = "?page=" + $("#search-page").val();
        var p = document.createElement("a");
        p.setAttribute('href',page)
        p.setAttribute("id","p")
        document.body.appendChild(p)
        p.click();
        $("#p").remove();
        
    });
    $(".download").on("click",function(){
        var data = $(this).parent().parent().siblings(".news-body").children("p").text();
        $.ajax({
            url:"/downloadimage/",
            type:"POST",
            data:{"cycle":data},
            success:function(data){
                path = data["name"];
                path = '/media/image/' + path;
                var a = document.createElement("a");
                a.setAttribute('href',path);
                a.setAttribute("id","a");
                a.setAttribute("download","");
                document.body.appendChild(a);
                a.click();
                $("#a").remove();
                }
            })
    });
})
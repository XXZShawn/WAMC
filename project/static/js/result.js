$('.active').removeClass('active');
$("#cycle").addClass("active");
function page(){
    error_message = document.getElementById("cp-count").innerText;
    if (error_message == ""){
        $("#page").hide();
    }
};
$(".custom-file").on('change','input[type="file"]',function(){
    file_path = $(this).val();
    arr = file_path.split("\\");
    file_name = arr[arr.length-1];
    $("#file_label").html(file_name);
});
$("#reset").on("click",function(){
    $("#file_label").html("Choose File");
});
function validation(){
    inputs=document.getElementById("file");
    for (i=0;i<inputs.length;i++){
        if(!inputs[i].value){
            alert("ERROR: YOU NEED TO FILL THE FILE INPUT");
            return false;
        }
    };
    file_input=document.getElementById("file");
    pos = file_input.value.lastIndexOf(".");
    name = file_input.value.substring(pos+1);
    if (name !="txt"){
        alert("ERROR: PLEASE INPUT THE TXT FILE");
        return false;
    }
    return true;
};
$(function(){
    result = document.getElementById("cp-count").innerText;
    if (result == ""){
        $("#page").hide();
        $("#search").hide();
    };
    $("[data-toggle='tooltip']").tooltip();
    $(".all").on("click",function(){
        $(this).parent().siblings().slideToggle();
    });
    $(".close").on("click",function(){
        $(".modal").hide();
    });
    $("#go").on("click",function(){
        page = "?page=" + $("#search-page").val();
        var p = document.createElement("a");
        p.setAttribute('href',page)
        p.setAttribute("id","p")
        document.body.appendChild(p)
        p.click();
        $("#p").remove();
        
    });
    $(".view").on("click",function(){
        var data = $(this).parent().parent().siblings(".news-body").children("p").text();
        var button = $(this).val()
        $.ajax({
            url:"/view/",
            type:"POST",
            data:{"cycle":data,"button":button},  
            success:function (data) { 
                path = data["path"];
                $("#my_image").attr("src", path);
                $(".modal").show();
            } 
            })
    });
    $(".download").on("click",function(){
        var data = $(this).parent().parent().siblings(".news-body").children("p").text();
        var button = $(this).val()
        $.ajax({
            url:"/downloadimage/",
            type:"POST",
            data:{"cycle":data,"button":button},
            success:function(data){
                path = data["name"];
                path = '/media/image/' + path;
                var a = document.createElement("a");
                a.setAttribute('href',path)
                a.setAttribute("id","a")
                a.setAttribute("download","")
                document.body.appendChild(a)
                a.click();
                $("#a").remove();
            }
        })
    })
});
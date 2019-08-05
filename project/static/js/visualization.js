$('.active').removeClass('active');
$("#visualization").addClass("active");
$("a").mousedown(function () { 
    $(this).css("color","grey");
});

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
    inputs=document.getElementsByTagName("input");
    for (i=0;i<inputs.length;i++){
        if(!inputs[i].value){
            alert("ERROR: YOU NEED TO FILL ALL THE INPUTS");
            return false;
        }
    }
    file_input=document.getElementById("file");
    pos = file_input.value.lastIndexOf(".");
    name = file_input.value.substring(pos+1);
    if (name !="txt"){
        alert("ERROR: PLEASE INPUT THE TXT FILE");
        return false;
    }
    return true;
};

$(".card-header").hover(
    function(){
        $(this).css("background-color",'#e8ecef');
    },
    function(){
        $(this).css("background","#f7f7f7");
    }
);  
// 提示框
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip()
    search_result = document.getElementById("search_result").innerText;
    top_10 = document.getElementById("top_10").innerText;
    $("#accordion").hide();
    $("#hr").hide();
    $("#search_accordion").hide();
    if (top_10 != ''){
        $('#accordion').show();
        $("#hr").show()
    };
    if (search_result != ""){
        $("#search_accordion").show();
    };
    $("#jqzoom").jqzoom({
        zoomWidth:230,
        zoomHeight:230,
        zoomType:"reverse"
    })
});
$(".fa-remove").click(function (e) { 
    $(".fade").hide();
});


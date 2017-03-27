$(document).ready(function(){
	var is_private = 0;
	var small_num = 0;
	var medium_num = 0;
	var large_num = 0;
	var time = 0;

	$("#start").on("click",function()
	{
		$("#myModal").modal('show');
	});

	$("#createinstance").on("click",function()
	{
		small_num = parseInt($("#small_num").val());
		medium_num = parseInt($("#medium_num").val());
		large_num = parseInt($("#large_num").val());
		time = parseInt($("#time").val());
		if(isNaN(small_num)||isNaN(medium_num)||isNaN(large_num)||isNaN(time))
		{
			swal("输入参数不符合格式，请重新输入");
		}
		else
		{
			start_create(small_num,medium_num,large_num,time,is_private);
		}

	});
	$("#sure").on("click",function()
	{
		is_private = 1;
	});
	$("#refuse").on("click",function()
	{
		is_private = 0;
	});
})

function start_create()
{

	$.ajax({
		url:"/action/createAdvanceAction/",
		//async: false, //if we want to lock the screen
		data:{
			"small_num": arguments[0],
			"medium_num": arguments[1],
			"large_num": arguments[2],
			"time":arguments[3],
    		"is_private": arguments[4]
		},
		type:'POST',//action:post or get
		dataType:'json',
		beforeSend:function(){
			//alert("beforeSend!");
		},
		success:function(data){
			$.each(data,function(name,value){
				if("limits" == name){
				    swal(value);
				}
			}
			);
		},
		error:function(xhr,type){
			swal("服务器出现故障，请稍后再试");
		}
	});
}
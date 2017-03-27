function instanceAction(obj){
	var action = obj.value;//$(obj).val()
	var instanceId = $(obj).parent().parent().find("td").eq(0).html();
//	.eq(1).value;
	var cloudName = $(obj).parent().parent().find("td").eq(1).html();
	$.ajax({
		url:"/action/instanceActionsAction/",
		//async: false, //if we want to3 lock the screen
		data:{
			"cloud":cloudName,
			"actions":action,
			"serverid":instanceId,
		},
		type:'POST',//action:post or get
		dataType:'json',
		beforeSend:function(){
			//alert("beforeSend!");
		},
		success:function(data){
			//success
			swal("successed! please refresh");
//			location.reload(); //F5,refresh
		},
		error:function(xhr,type){
			//do nothing
			swal("status is already exist!");
		}
	});
}

function AliyunAction(obj){
	var action = obj.value;//$(obj).val()
	var instanceId = $(obj).parent().parent().find("td").eq(0).html();
//	.eq(1).value;
	$.ajax({
		url:"/action/AliyunActionsAction/",
		//async: false, //if we want to3 lock the screen
		data:{
			"instance_id":instanceId,
			"actions":action,
		},
		type:'POST',//action:post or get
		dataType:'json',
		beforeSend:function(){
			//alert("beforeSend!");
		},
		success:function(data){
			//success
			swal("successed! please refresh");
//			location.reload(); //F5,refresh
		},
		error:function(xhr,type){
			//do nothing
			swal("status is already exist!");
		}
	});
}



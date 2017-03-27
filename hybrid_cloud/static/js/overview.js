$(document).ready(function(){
	//get overview
//	swal("统计图生成需要几秒");
	getOverview("openstack");
})

function getOverview()
{
    var myname=new Array();
    myname[0]="instance";
    myname[1]="core";
    myname[2]="ram";
    myname[3]="volume";
    var cloudname= arguments[0]
	$.ajax({
		url:"/action/overviewAction/",
		//async: false, //if we want to lock the screen
		data:{
			"cloud":arguments[0]
		},
		type:'POST',//action:post or get
		dataType:'json',
		beforeSend:function(){
			//alert("beforeSend!");
		},
		success:function(data){
			$.each(data,function(name,value){
				if("limits" == name){
				    $.each(value,function(j,limit)
				    {
					    circle('#'+cloudname+'_container'+(j+1),limit,myname[j]);
					});
				}
			}
			);
		},
		error:function(xhr,type){
			swal("fail to get overview!");
		}
	});
}



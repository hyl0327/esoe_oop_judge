function close_message(index){
	var li = document.getElementById("close_li"+index);
	var btn = document.getElementById("close"+index);
	console.log("close_li"+index);
	li.style.display="none";
	btn.style.display="none";
}
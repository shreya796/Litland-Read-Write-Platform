<script>
function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    ev.target.appendChild(document.getElementById(data));
}
</script>




<script type="text/javascript">
	
	(function () {
		var dialog=document.getElementById('dialogue');
		document.getElementById('show').onclick=function () {
			dialog.show();
		};
		document.getElementById('hide').onclick=function(){
			dialog.close();
			};
		})();
</script>
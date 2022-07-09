$(function() {

	function winH(){
		let vh = window.innerHeight * 0.01;
		document.documentElement.style.setProperty('--vh', vh + "px");
	}
	winH();
	window.addEventListener('resize', () => {
		winH();
	});

	$("a, img").attr("draggable", "false");

	$(".user").on("click", function(e){
		$(".user._active").removeClass("_active");
		$(this).addClass("_active");
		$(".wrapper").addClass("chat-opened");
	});

	$(".top-panel__back").on("click", function(e){
		$(".wrapper").removeClass("chat-opened");
	});

	$(".messages-form").on("submit", function(e){
		e.preventDefault();
		let currentTime = new Date();
		let msgTime = currentTime.getHours() + ":" + currentTime.getMinutes();
		let msgText = $(".messages-form__field").val();
		let msgHtml = "<li class='messages__item'><p class='message'>"+ msgText +"<span class='message__time'>"+ msgTime +"</span></p></li>";
		$(this).find("textarea").val("");
		$(".messages__list").append(msgHtml);
	});


});
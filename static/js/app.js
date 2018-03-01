var $sidebarOverlay = $(".task-overlay");
$(".task-chat").on("click", function(e) {
	var $target = $($(this).attr("href"));
	if ($target.length) {
		$target.toggleClass("opened");
		$sidebarOverlay.toggleClass("opened");
		$("body").toggleClass("menu-opened");
		$sidebarOverlay.attr("data-reff", $(this).attr("href"))
	}
	e.preventDefault()
});
$sidebarOverlay.on("click", function(e) {
	var $target = $($(this).attr("data-reff"));
	if ($target.length) {
		$target.removeClass("opened");
		$("body").removeClass("menu-opened");
		$(this).removeClass("opened")
	}
	e.preventDefault()
});


var $sidebarOverlay = $(".sidebar-overlay");
$("#mobile_btn").on("click", function(e) {
	var $target = $($(this).attr("href"));
	if ($target.length) {
		$target.toggleClass("opened");
		$sidebarOverlay.toggleClass("opened");
		$("body").toggleClass("menu-opened");
		$sidebarOverlay.attr("data-reff", $(this).attr("href"))
	}
	e.preventDefault()
});
$sidebarOverlay.on("click", function(e) {
	var $target = $($(this).attr("data-reff"));
	if ($target.length) {
		$target.removeClass("opened");
		$("body").removeClass("menu-opened");
		$(this).removeClass("opened")
		$(".main-wrapper").removeClass("slide-nav-toggle");
	}
	e.preventDefault()
});





!function($) {
    'use strict';
	var topNavThemeClass = window.localStorage;
}(window.jQuery),  

$(function() {

	var headerColors = "theme-default theme-orange theme-dark theme-blue theme-maroon theme-light theme-purple";

	$(".themes-icon").click(function () {
		$('.themes').toggleClass("active");
		$('.main-wrapper').removeClass('open-msg-box');
	});

	$(document).ready(function () {
		var navColor = localStorage.getItem('navbar-color');
		if (navColor) {
			$('body').removeClass(headerColors).addClass(navColor);
		}
	});
	$('#theme-change span').click(function() {
		if ($(this).hasClass("theme-default")) {
			$('body').removeClass(headerColors).addClass('theme-default');
			localStorage.setItem('navbar-color','theme-default');
		}

		if ($(this).hasClass("theme-maroon")) {
			$('body').removeClass(headerColors).addClass('theme-maroon');
			localStorage.setItem('navbar-color', 'theme-maroon');
		}

		if ($(this).hasClass("theme-orange")) {
			$('body').removeClass(headerColors).addClass('theme-orange');
			localStorage.setItem('navbar-color', 'theme-orange');
		}

		if ($(this).hasClass("theme-blue")) {
			$('body').removeClass(headerColors).addClass('theme-blue');
			localStorage.setItem('navbar-color', 'theme-blue');
		}

		if ($(this).hasClass("theme-purple")) {
			$('body').removeClass(headerColors).addClass('theme-purple');
			localStorage.setItem('navbar-color', 'theme-purple');
		}

		if ($(this).hasClass("theme-orange")) {
			$('body').removeClass(headerColors).addClass('theme-orange');
			localStorage.setItem('navbar-color', 'theme-orange');
		}

		if ($(this).hasClass("theme-dark")) {
			$('body').removeClass(headerColors).addClass('theme-dark');
			localStorage.setItem('navbar-color', 'theme-dark');
		}

		if ($(this).hasClass("theme-light")) {
			$('body').removeClass(headerColors).addClass('theme-light');
			localStorage.setItem('navbar-color', 'theme-light');
		}
	});
});

!function($) {
    "use strict";

    var Sidemenu = function() {
        this.$menuItem = $("#sidebar-menu a")
    };

    Sidemenu.prototype.menuItemClick = function(e) {
        if($(this).parent().hasClass("submenu")) {
          e.preventDefault();
        }   
        if(!$(this).hasClass("subdrop")) {
          $("ul",$(this).parents("ul:first")).slideUp(350);
          $("a",$(this).parents("ul:first")).removeClass("subdrop");
          
          $(this).next("ul").slideDown(350);
          $(this).addClass("subdrop");
        }else if($(this).hasClass("subdrop")) {
          $(this).removeClass("subdrop");
          $(this).next("ul").slideUp(350);
        }
    },

    Sidemenu.prototype.init = function() {
      var $this  = this;
      $this.$menuItem.on('click', $this.menuItemClick);
      $("#sidebar-menu ul li.submenu a.active").parents("li:last").children("a:first").addClass("active").trigger("click");
    },
    $.Sidemenu = new Sidemenu, $.Sidemenu.Constructor = Sidemenu
    
}(window.jQuery),


//main app module
 function($) {
    "use strict";
    
    var App = function() {
        this.$body = $("body")
    };
    
    //initilizing 
    App.prototype.init = function() {
        var $this = this;
        $(document).ready($this.onDocReady);
        $.Sidemenu.init();
    },

    $.App = new App, $.App.Constructor = App

}(window.jQuery),

//initializing main application module
function($) {
    "use strict";
    $.App.init();
}(window.jQuery);




	$(document).ready(function() {
		if($('.select').length > 0 ){
			$('.select').select2({
				minimumResultsForSearch: -1,
				width: '100%'
			});
		}
	});
	$(document).ready(function() {
		if($('.modal').length > 0 ){
			var modalUniqueClass = ".modal";
			$('.modal').on('show.bs.modal', function(e) {
			  var $element = $(this);
			  var $uniques = $(modalUniqueClass + ':visible').not($(this));
			  if ($uniques.length) {
				$uniques.modal('hide');
				$uniques.one('hidden.bs.modal', function(e) {
				  $element.modal('show');
				});
				return false;
			  }
			});
		}
	});
	$(document).ready(function() {
		if($('.floating').length > 0 ){
			$('.floating').on('focus blur', function (e) {
			$(this).parents('.form-focus').toggleClass('focused', (e.type === 'focus' || this.value.length > 0));
			}).trigger('blur');
		}
	});	
	$(document).ready(function() {
		if($('.msg-list-scroll').length > 0 ){
			$('.msg-list-scroll').slimscroll({
				height:'100%',
				color: '#878787',
				disableFadeOut : true,
				borderRadius:0,
				size:'4px',
				alwaysVisible:false
			});
			var h=$(window).height()-124;
			$('.msg-list-scroll').height(h);
			$('.msg-sidebar .slimScrollDiv').height(h);  
			
			$(window).resize(function(){
				var h=$(window).height()-124;
				$('.msg-list-scroll').height(h);
				$('.msg-sidebar .slimScrollDiv').height(h);
			});
		}
	});
	$(document).ready(function(){
		if($('.slimscroll').length > 0 ){
			$('.slimscroll').slimScroll({
				height: 'auto',
				width: '100%',
				position: 'right',
				size: "7px",
				color: '#ccc',
				wheelStep: 5
			});
			var h=$(window).height()-60;
			$('.slimscroll').height(h);
			$('.sidebar .slimScrollDiv').height(h);
			
			$(window).resize(function(){
				var h=$(window).height()-60;
				$('.slimscroll').height(h);
				$('.sidebar .slimScrollDiv').height(h);
			});
		}
	});
	$(document).ready(function(){
		if($('.page-wrapper').length > 0 ){
			var height = $(window).height();	
			$(".page-wrapper").css("min-height", height);
		}
	});
	$(window).resize(function(){
		if($('.page-wrapper').length > 0 ){
			var height = $(window).height();
			$(".page-wrapper").css("min-height", height);
		}
	});
	$(function () {
		if($('.datetimepicker').length > 0 ){
			$('.datetimepicker').datetimepicker({
				format: 'DD/MM/YYYY'
			});
		}
	});
	$(document).ready(function() {
		if($('.datatable').length > 0 ){
			$('.datatable').DataTable({
				"bFilter": false,
			});
		}
	});
	$(document).ready(function() {
		if($('[data-toggle="tooltip"]').length > 0 ){
			$('[data-toggle="tooltip"]').tooltip();
		}
	});
	$(document).ready(function(){
		if($('.btn-toggle').length > 0 ){
			 $('.btn-toggle').click(function() {
				$(this).find('.btn').toggleClass('active');  
				if ($(this).find('.btn-success').size()>0) {
					$(this).find('.btn').toggleClass('btn-success');
				}
			});
		} 
	});
	$(document).ready(function() {
		if($('.main-wrapper').length > 0 ){
		var $wrapper = $(".main-wrapper");
			$(document).on('click', '#mobile_btn, #open_right_sidebar, #setting_panel_btn', function (e) {
				$(".dropdown.open > .dropdown-toggle").dropdown("toggle");
				return false;
			});
			$(document).on('click', '#mobile_btn', function (e) {
				$wrapper.removeClass('open-right-sidebar').toggleClass('slide-nav-toggle');
				return false;
			});
			$(document).on('click', '#open_msg_box', function (e) {
				$wrapper.toggleClass('open-msg-box').removeClass('');
				$('.themes').removeClass('active');
				return false;
			});
			$(document).on('click', '#close_msg_box', function (e) {
				$wrapper.toggleClass('close-msg-box').removeClass('open-msg-box');
				return false;
			});
			$(document).on('click', '#open_right_sidebar', function (e) {
				$wrapper.toggleClass('open-right-sidebar').removeClass('open-setting-panel');
				return false;
			});
			/*$(document).on('click', '#task_right_sidebar', function (e) {
				$wrapper.toggleClass('task-right-sidebar').removeClass('open-setting-panel');
				return false;
			});
			$(document).on('click', '#close_right_sidebar', function (e) {
				$wrapper.toggleClass('close-right-sidebar').removeClass('open-right-sidebar');
				return false;
			});*/
		}
	});	
	$(document).ready(function() {
		if($('.table-responsive').length > 0 ){
			if (screen.width >= 992) {
			$('.table-responsive').on('show.bs.dropdown', function () {
				 $('.table-responsive').css( "overflow", "inherit" );
			});

			$('.table-responsive').on('hide.bs.dropdown', function () {
				 $('.table-responsive').css( "overflow", "auto" );
			})
			}
		}
	});
	$(document).ready(function() {
		if($('.clickable-row').length > 0 ){
			$(".clickable-row").click(function() {
				window.location = $(this).data("href");
			});
		}
	});
	
/*$(document).ready(function() {
  $(".datatable").on('sorted', function(){
    var lastRow = $(".datatable").find("tbody tr:last");
      // Removing dropup class from the row which owned it
      $(".datatable").find("tbody tr .dropdown").addClass("dropup");
      // Adding dropup class to the current last row
      lastRow.addClass("dropup");
  });
});*/



